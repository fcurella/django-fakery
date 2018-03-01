test:
	python setup.py test

coverage:
	coverage run --source django_fakery setup.py test

release: coverage
	rm -rf dist
	rm -rf build
	rm -rf django_fakery.egg-info
	python setup.py sdist bdist_wheel
	twine upload dist/*
