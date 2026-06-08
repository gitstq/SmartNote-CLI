.PHONY: install test lint format clean build dist upload

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=smartnote --cov-report=term-missing

lint:
	flake8 smartnote/ tests/
	black --check smartnote/ tests/

format:
	black smartnote/ tests/

clean:
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .coverage htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

dist: build

upload: dist
	twine upload dist/*

run:
	python -m smartnote.cli tui
