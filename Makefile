# Makefile for Python Project

VENV_NAME := venv
PYTHON := python3.11
VENV_FLAKE8 := $(VENV_NAME)/bin/flake8
VENV_PYTHON := $(VENV_NAME)/bin/${PYTHON}
VENV_PIP := $(VENV_NAME)/bin/pip

.PHONY: venv install test clean

help:
	@echo "Available targets:"
	@echo "  venv      - Create a virtual environment"
	@echo "  install   - Install dependencies"
	@echo "  test      - Run tests"
	@echo "  clean     - Remove generated files and virtual environment"

venv:
	$(PYTHON) -m venv $(VENV_NAME)

install: venv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt

install-test: venv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r test-requirements.txt

lint: venv
	$(VENV_PYTHON) $(VENV_FLAKE8) sample/ tests/

test: venv install-test
	$(VENV_PYTHON) -m unittest discover -s tests -v

test-coverage: venv install-test
	coverage run -m unittest discover -s tests/
	coverage xml

clean:
	rm -rf $(VENV_NAME) __pycache__ .pytest_cache

