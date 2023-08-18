all:
	clear
	autopep8 -i *.py
	pytest -vv test.py
