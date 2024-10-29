.PHONY: test format
export PYTHONPATH := .

test:
	python3 -m pytest -vv

format:
	black .
