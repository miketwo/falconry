.PHONY: init test testw
init:
	pip install -r requirements.txt

test:
	find . -name \*.pyc -delete
	py.test -v -s

testw:
	find . -name \*.pyc -delete
	ptw -- -v -s --cache-clear
