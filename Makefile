.PHONY: build try test tests deploy help clean

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

build:
	uv run python build/build.py

try: build
	@echo "Starting server on http://localhost:8000"
	@echo "Press Ctrl+C to stop"
	cd output && python3 -m http.server 8000

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

.DEFAULT_GOAL := help
