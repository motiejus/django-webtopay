clean:
	find -name '*.pyc' -exec rm {} \;

test: clean
	./runtests.py
