.PHONY: test
export PYTHONPATH := .

test:
	python3 -m pytest
