import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_claude_md_references_exist():
    """Every .claude/-relative file referenced from CLAUDE.md must exist.

    Regression test: CLAUDE.md once pointed at .claude/how_to_be.md and
    .claude/codereview.md after both files were renamed/removed, silently
    breaking Claude Code's @-includes.
    """
    text = (REPO_ROOT / "CLAUDE.md").read_text()

    refs = set(re.findall(r"\.claude/[\w\-./]+\.md", text))
    assert refs, "expected CLAUDE.md to reference at least one .claude/ file"

    missing = [ref for ref in refs if not (REPO_ROOT / ref).exists()]
    assert not missing, f"CLAUDE.md references nonexistent files: {missing}"
