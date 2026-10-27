.PHONY: build try test tests deploy help clean factory factory-clean golden

help:
	@echo "Boston Robot Hackers Website — Available Commands:"
	@echo ""
	@echo "  make build    — Build the website to output/"
	@echo "  make try      — Build and start local server (http://localhost:8000)"
	@echo "  make test     — Run the full test suite"
	@echo "  make tests    — Alias for test"
	@echo "  make deploy   — Commit, push to GitHub (triggers GitHub Pages deploy)"
	@echo "  make clean    — Remove output/ directory"
	@echo ""
	@echo "  Factory (see .claude/process.md, factory lanes):"
	@echo "  make factory ISSUE=n        — Run issue n headless in its own worktree, open a PR"
	@echo "  make factory-clean ISSUE=n  — Remove that issue's worktree"
	@echo "  make golden [BASE=ref]      — Check the built site is unchanged vs ref (default origin/main)"
	@echo ""

build:
	uv run python build/build.py

try: build
	@echo "Stopping any existing server..."
	@pkill -f 'http.server' || true
	@sleep 1
	@echo "Starting server on http://localhost:8000"
	@cd output && python3 -m http.server 8000 > /dev/null 2>&1 &
	@sleep 2
	@echo "Opening browser..."
	@open http://localhost:8000 || xdg-open http://localhost:8000 || echo "Please visit http://localhost:8000 in your browser"
	@echo "Server running. Press Ctrl+C to stop."
	@wait

test tests:
	uv run pytest

deploy: test
	@echo "Building and pushing to GitHub..."
	uv run python build/build.py
	git add -A
	git commit -m "Update website" || true
	git push

clean:
	rm -rf output/

FACTORY_DIR = ../brh-factory-$(ISSUE)
FACTORY_TOOLS = Read Write Edit Glob Grep Agent \
	'Bash(gh *)' 'Bash(git *)' 'Bash(uv *)' 'Bash(tools/golden_diff.sh*)' \
	'Bash(ls *)' 'Bash(mv *)'

factory:
	@test -n "$(ISSUE)" || (echo "usage: make factory ISSUE=<number>" && exit 1)
	git fetch origin main
	git worktree add -B factory/issue-$(ISSUE) $(FACTORY_DIR) origin/main
	cd $(FACTORY_DIR) && git config core.hooksPath .githooks && uv sync -q
	cd $(FACTORY_DIR) && claude -p "/factory-run $(ISSUE)" \
		--permission-mode acceptEdits --allowedTools $(FACTORY_TOOLS)

factory-clean:
	@test -n "$(ISSUE)" || (echo "usage: make factory-clean ISSUE=<number>" && exit 1)
	git worktree remove --force $(FACTORY_DIR)

golden:
	tools/golden_diff.sh $(or $(BASE),origin/main)

.DEFAULT_GOAL := help
