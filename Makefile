all:
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*
	rm -r build/ dist
