test:
	python setup.py test

isort:
	isort -rc --atomic .

black:
	black --target-version py27 .

release:
	rm -rf dist
	rm -rf build
	rm -rf django_fakery.egg-info
	python setup.py sdist bdist_wheel
	twine upload dist/*
