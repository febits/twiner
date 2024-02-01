.PHONY: black
black:
	poetry run black -l 79 twiner/.

.PHONY: isort
isort:
	poetry run isort twiner/.

.PHONY: pylint
pylint:
	poetry run pylint twiner/.
