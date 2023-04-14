
.PHONY: black mypy lint package unit sunit test clean clean-build clean-pyc clean-test

black:
	poetry run isort app tests
	poetry run black app tests

mypy: black
	poetry run mypy app tests/*.py

lint: mypy
	poetry run flake8 app tests
	# poetry run doc8 -q docs

package:
	poetry check
	poetry run pip check
	# re-enable when safety supports packaging ^22.0
	poetry run safety check -i 51499 --full-report

sunit:
	poetry run pytest -s tests

unit:
	poetry run pytest tests

test: lint package unit

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr docs/_build
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
