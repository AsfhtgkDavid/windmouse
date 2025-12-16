.PHONY: test test-cov test-fast test-verbose lint format clean help install

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Install package in development mode with test dependencies
	pip install -e ".[test]"

test: ## Run tests with pytest
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html --cov-report=xml

test-fast: ## Run tests in parallel
	pytest tests/ -n auto

test-verbose: ## Run tests with maximum verbosity
	pytest tests/ -vv -s

lint: ## Run code quality checks
	black --check src/ tests/
	mypy src/ --ignore-missing-imports
	flake8 src/ tests/ --max-line-length=79 --extend-ignore=E203,W503

format: ## Format code with black
	black src/ tests/

clean: ## Clean up generated files
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf coverage.xml
	rm -rf .mypy_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docs: ## Build documentation
	cd docs && make html

docs-serve: ## Build and serve documentation locally
	cd docs && make html && python -m http.server --directory _build/html

all: clean format lint test-cov docs ## Run all checks and tests

