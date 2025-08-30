SHELL := /bin/sh

.PHONY: help test

help:
	@echo "Available targets:"
	@echo "  test     - Run python unittest discovery"

test:
	./.venv/bin/python -m unittest discover -s tests -p 'test*.py' -q
