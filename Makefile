.PHONY: install test

install:
	poetry install

test:
	poetry run pytest -vv --cov=qarin tests/