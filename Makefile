SRC=twiner/.

all: black isort pylint

.PHONY: black
black:
	-poetry run black -l 79 $(SRC)

.PHONY: isort
isort:
	-poetry run isort $(SRC)

.PHONY: pylint
pylint:
	-poetry run pylint $(SRC)
