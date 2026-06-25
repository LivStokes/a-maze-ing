PYTHON      = python3
MAIN        = a_maze_ing.py
CONFIG      = config.txt
VENV        = .venv
PIP         = pip
FLAKE8      = flake8
MYPY        = mypy
MAZE_PACKAGE = dist/mazegen-*.whl
SRC = src

.PHONY: install run debug clean lint lint-strict

# Install project dependencies into a virtual environment
install:
	$(PIP) install --upgrade pip
	$(PIP) install --force-reinstall $(MAZE_PACKAGE)

# Rebuilds the mazegen package from source
rebuild:
	$(PIP) install --upgrade pip
	$(PIP) install build
	$(PYTHON) -m build
	
# Run the maze generator with the default config file
run:
	$(PYTHON) $(MAIN) $(CONFIG)

# Run in debug mode with pdb
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# Remove caches and build artefacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist"       -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build"      -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc"              -delete 2>/dev/null || true

# Lint with flake8 + mypy (standard flags)
lint:
	$(PIP) install flake8 mypy
	$(FLAKE8) $(SRC)
	$(MYPY) $(SRC) \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

# Lint with flake8 + mypy --strict (optional enhanced mode)
lint-strict:
	$(PIP) install flake8 mypy
	$(FLAKE8) $(SRC)
	$(MYPY) $(SRC) --strict
