.PHONY: install format lint test coverage clean docs help

help:
	@echo "Available commands:"
	@echo "  make install    - Install the package and development dependencies"
	@echo "  make format     - Format code using black and isort"
	@echo "  make lint       - Run linting tools"
	@echo "  make test       - Run tests"
	@echo "  make coverage   - Run tests with coverage report"
	@echo "  make clean      - Clean up build and temporary files"
	@echo "  make docs       - Build documentation"

install:
	pip install -e ".[dev]"

format:
	black .
	isort .

lint:
	flake8 shellsense tests
	mypy shellsense
	black . --check
	isort . --check

test:
	pytest

coverage:
	pytest --cov=shellsense --cov-report=term-missing --cov-report=html

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete

docs:
	cd docs && make html
