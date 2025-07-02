.PHONY: help install install-dev test format lint typecheck quality build clean publish publish-test docker docker-test bump-patch bump-minor bump-major inspector

help:
	@echo "Available commands:"
	@echo "  install       Install the package"
	@echo "  install-dev   Install with development dependencies"
	@echo "  test          Run tests"
	@echo "  format        Format code with Black"
	@echo "  lint          Lint code with Ruff"
	@echo "  typecheck     Type check with mypy"
	@echo "  quality       Run all code quality checks"
	@echo "  build         Build distribution packages"
	@echo "  clean         Clean build artifacts"
	@echo "  publish       Publish to PyPI"
	@echo "  publish-test  Publish to Test PyPI"
	@echo "  docker        Build Docker image"
	@echo "  docker-test   Run tests in Docker"
	@echo "  inspector     Run MCP Inspector"
	@echo "  bump-patch    Bump patch version"
	@echo "  bump-minor    Bump minor version"
	@echo "  bump-major    Bump major version"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	python tests/test_server.py

format:
	black src/ tests/

lint:
	ruff src/ tests/

typecheck:
	mypy src/

quality: format lint typecheck

build: clean
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete

publish: quality test build
	./scripts/publish.sh

publish-test: quality test build
	TEST_PYPI=1 ./scripts/publish.sh

docker:
	docker build -t pluggedin-random-number-generator-mcp-python .

docker-test:
	docker-compose --profile test up

bump-patch:
	python scripts/bump-version.py patch

bump-minor:
	python scripts/bump-version.py minor

bump-major:
	python scripts/bump-version.py major

# Development shortcuts
dev: install-dev

run:
	pluggedin-random-number-generator-mcp-python

# Docker shortcuts
docker-alpine:
	docker build -f Dockerfile.alpine -t pluggedin-random-number-generator-mcp-python:alpine .

docker-minimal:
	docker build -f Dockerfile.minimal -t pluggedin-random-number-generator-mcp-python:minimal .

docker-smithery:
	docker build -f Dockerfile.smithery -t pluggedin-random-number-generator-mcp-python:smithery .

# MCP Inspector
inspector:
	@echo "Starting MCP Inspector for Python server..."
	@echo "Server will be available at http://localhost:5173"
	@echo "Note: Make sure you have @modelcontextprotocol/inspector installed (npm install -g @modelcontextprotocol/inspector)"
	npx @modelcontextprotocol/inspector python3 scripts/run-inspector.py