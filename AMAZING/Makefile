PYTHON      = python3
MAIN        = a_maze_ing.py
CONFIG      = config.txt
VENV        = .venv
PIP         = $(VENV)/bin/pip
FLAKE8      = $(VENV)/bin/flake8
MYPY        = $(VENV)/bin/mypy

.PHONY: install run debug clean lint lint-strict

## Install project dependencies into a virtual environment
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy curses-stubs

## Run the maze generator with the default config file
run:
	$(PYTHON) $(MAIN) $(CONFIG)

## Run in debug mode with pdb
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

## Remove caches and build artefacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist"       -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build"      -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc"              -delete 2>/dev/null || true

## Lint with flake8 + mypy (standard flags)
lint:
	$(FLAKE8) .
	$(MYPY) . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

## Lint with flake8 + mypy --strict (optional enhanced mode)
lint-strict:
	$(FLAKE8) .
	$(MYPY) . --strict
