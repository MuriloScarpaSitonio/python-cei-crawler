.PHONY: clean test security-checker code-convention typing-checker pipeline

PROJECT_NAME := python-cei-crawler
PYTHON_VERSION := 3.8.10

.clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +


.clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +


.clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr reports/
	rm -fr .pytest_cache/


clean: .clean-build .clean-pyc .clean-test ## remove all build, test, coverage and Python artifacts


test:
	pytest


code-convention:
	pylint_runner
	black . --check


security-checker:
	bandit -r . --exclude=/tests,/.venv


typing-checker:
	mypy . --exclude=.venv --ignore-missing-imports


pipeline: test code-convention security-checker typing-checker
