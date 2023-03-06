test:
	python -Wd setup.py test

mypy:
	mypy django_fakery

isort:
	isort --atomic .

black:
	black .

release:
	rm -rf dist
	rm -rf build
	rm -rf django_fakery.egg-info
	python setup.py sdist bdist_wheel
	twine upload dist/*
