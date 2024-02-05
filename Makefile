.PHONY: install test jupyter

install:
	poetry install

test:
	poetry run pytest -vv --cov=qarin tests/

jupyter:
	poetry run jupyter lab