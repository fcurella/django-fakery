import os
from setuptools import find_packages, setup


VERSION = '1.6.0'


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as fh:
            return fh.read()
    except IOError:
        return ''

setup(
    name='django-fakery',
    version=VERSION,
    url='https://github.com/fcurella/django-fakery/',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    description='A model instances generator for Django',
    long_description=read('README.rst'),
    license='MIT',
    packages=find_packages(exclude=['*.tests']),
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        "fake-factory>=0.6.0,<0.7.0",
        "Django>=1.7",
        "django-autoslug==1.9.3",
    ],
    test_suite='django_fakery.tests.runtests.runtests',
)
