
.PHONY: black mypy lint

black:
	poetry run isort app tests
	poetry run black app tests

mypy: black
	poetry run mypy app tests/*.py

lint: mypy
	poetry run flake8 app tests
	# poetry run doc8 -q docs
