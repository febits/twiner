SRC=./twiner/
TEST=./tests/

.PHONY: all
all: black isort pylint test

.PHONY: black
black:
	-poetry run black -l 79 $(SRC) $(TEST)

.PHONY: isort
isort:
	-poetry run isort $(SRC) $(TEST)

.PHONY: pylint
pylint:
	-poetry run pylint $(SRC) $(TEST)

.PHONY: test
test:
	-poetry run pytest -vv
