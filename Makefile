
.PHONY: black mypy lint package unit sunit test

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

test: lint package # unit
