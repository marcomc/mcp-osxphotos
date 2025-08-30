SHELL := /bin/sh

.PHONY: help test test-verbose test-failfast test-one

PY := ./.venv/bin/python
DISCOVER := -m unittest discover -s tests -p 'test*.py'

help:
	@echo "Available targets:"
	@echo "  test         - Run python unittest discovery (quiet)"
	@echo "  test-verbose - Run tests with verbose output"
	@echo "  test-failfast- Verbose + stop on first failure"
	@echo "  test-one     - Run a single test (make test-one name=tests.test_mod.Class.test)"

test:
	$(PY) $(DISCOVER) -q

test-verbose:
	$(PY) $(DISCOVER) -v

test-failfast:
	$(PY) $(DISCOVER) -v -f

# Usage: make test-one name=tests.test_schema_shapes.TestSchemaShapes.test_no_tuple_annotations_for_multi_args
test-one:
	@if [ -z "$(name)" ]; then \
		echo "Usage: make test-one name=<module.Class.test>"; \
		exit 2; \
	fi
	$(PY) -m unittest -v $(name)
