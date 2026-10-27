#!/usr/bin/env python3
# test_factory — Tests for the F19 software-factory plumbing
# Author: Pito Salas and Claude Code
# Version: 1
# Created: 2026-10-27
# Updated: 2026-10-27
# Open Source Under MIT license
"""Checks the parts of the factory that are code or config, not prompts.

The Stop hook, the factory guard and the golden diff are shell scripts, so
they are exercised as subprocesses with the JSON Claude Code would send them.
"""

import json
import re
import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS_DIR = REPO_ROOT / ".claude" / "hooks"
GOLDEN = REPO_ROOT / "tools" / "golden_diff.sh"


def load_settings() -> dict:
    return json.loads((REPO_ROOT / ".claude" / "settings.json").read_text())


def hook_commands(event: str) -> list[str]:
    return [
        hook["command"]
        for entry in load_settings()["hooks"].get(event, [])
        for hook in entry["hooks"]
    ]


def run_hook(script: Path, payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=cwd,
        env={"CLAUDE_PROJECT_DIR": str(cwd), "PATH": "/usr/bin:/bin"},
        check=False,
    )


def make_repo_on_branch(tmp_path: Path, branch: str) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", "-b", branch, str(repo)], check=True)
    return repo


# --- TF19.0: Stop hook ---


def test_stop_hook_is_registered():
    assert any("stop-verify.sh" in command for command in hook_commands("Stop"))


def test_stop_hook_yields_when_already_continuing():
    result = run_hook(
        HOOKS_DIR / "stop-verify.sh", {"stop_hook_active": True}, REPO_ROOT
    )
    assert result.returncode == 0


def test_stop_hook_ignores_clean_tree(tmp_path):
    repo = make_repo_on_branch(tmp_path, "main")
    result = run_hook(HOOKS_DIR / "stop-verify.sh", {"stop_hook_active": False}, repo)
    assert result.returncode == 0


# --- factory guard ---


def test_factory_guard_is_registered_for_bash():
    entries = load_settings()["hooks"]["PreToolUse"]
    assert any(
        entry["matcher"] == "Bash"
        and any("factory-guard.sh" in hook["command"] for hook in entry["hooks"])
        for entry in entries
    )


@pytest.mark.parametrize(
    "command",
    [
        "git push origin main",
        "git push origin HEAD:main",
        "gh pr merge 12 --squash",
        "gh issue close 7",
    ],
)
def test_factory_guard_blocks_on_factory_branch(tmp_path, command):
    repo = make_repo_on_branch(tmp_path, "factory/issue-7")
    payload = {"tool_input": {"command": command}}
    result = run_hook(HOOKS_DIR / "factory-guard.sh", payload, repo)
    assert result.returncode == 2
    assert "factory-guard" in result.stderr


def test_factory_guard_allows_feature_branch_push(tmp_path):
    repo = make_repo_on_branch(tmp_path, "factory/issue-7")
    payload = {"tool_input": {"command": "git push -u origin HEAD"}}
    result = run_hook(HOOKS_DIR / "factory-guard.sh", payload, repo)
    assert result.returncode == 0


def test_factory_guard_leaves_interactive_work_alone(tmp_path):
    repo = make_repo_on_branch(tmp_path, "main")
    payload = {"tool_input": {"command": "git push origin main"}}
    result = run_hook(HOOKS_DIR / "factory-guard.sh", payload, repo)
    assert result.returncode == 0


# --- TF19.1: CI ---


def test_ci_tests_and_lints_before_building():
    workflow = yaml.safe_load(
        (REPO_ROOT / ".github" / "workflows" / "deploy.yml").read_text()
    )
    test_steps = " ".join(
        step.get("run", "") for step in workflow["jobs"]["test"]["steps"]
    )
    assert "pytest" in test_steps
    assert "ruff check" in test_steps
    assert workflow["jobs"]["build"]["needs"] == "test"


# --- TF19.2: golden diff ---


def write_site(root: Path, index_html: str, dtstamp: str) -> Path:
    root.mkdir(parents=True)
    (root / "index.html").write_text(index_html)
    (root / "meetings.ics").write_text(f"BEGIN:VEVENT\nDTSTAMP:{dtstamp}\nEND:VEVENT\n")
    return root


def run_compare(site_a: Path, site_b: Path) -> int:
    return subprocess.run(
        [str(GOLDEN), "--compare", str(site_a), str(site_b)],
        capture_output=True,
        check=False,
    ).returncode


def test_golden_ignores_build_timestamps(tmp_path):
    site_a = write_site(tmp_path / "a", "<p>same</p>", "20261027T100000Z")
    site_b = write_site(tmp_path / "b", "<p>same</p>", "20261027T100500Z")
    assert run_compare(site_a, site_b) == 0


def test_golden_catches_real_changes(tmp_path):
    site_a = write_site(tmp_path / "a", "<p>same</p>", "20261027T100000Z")
    site_b = write_site(tmp_path / "b", "<p>changed</p>", "20261027T100000Z")
    assert run_compare(site_a, site_b) != 0


def test_dev_tools_are_not_published():
    assert not (REPO_ROOT / "scripts" / "golden_diff.sh").exists()


# --- TF19.4: issue forms ---


@pytest.mark.parametrize(
    ("form_name", "lane_label", "required_ids"),
    [
        (
            "speaker-confirmed.yml",
            "lane:content",
            {"meeting_date", "speaker", "topic", "blurb"},
        ),
        ("factory-refactor.yml", "lane:refactor", {"feature"}),
    ],
)
def test_issue_form_labels_and_required_fields(form_name, lane_label, required_ids):
    form = yaml.safe_load(
        (REPO_ROOT / ".github" / "ISSUE_TEMPLATE" / form_name).read_text()
    )
    assert set(form["labels"]) == {"factory", lane_label}
    required = {
        field["id"]
        for field in form["body"]
        if field.get("validations", {}).get("required")
    }
    assert required == required_ids


# --- TF19.5: Makefile ---


def test_every_make_target_is_in_help():
    makefile = (REPO_ROOT / "Makefile").read_text()
    phony = re.search(r"^\.PHONY:(.*)$", makefile, re.MULTILINE).group(1).split()
    help_text = makefile[makefile.index("help:") : makefile.index("build:")]
    missing = [
        target
        for target in phony
        if target not in {"help", "tests"} and f"make {target}" not in help_text
    ]
    assert missing == []
