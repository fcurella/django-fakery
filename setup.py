import os
from setuptools import find_packages, setup


VERSION = '1.9.0'


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
    packages=find_packages(exclude=["docs", "tests", "tests.*"]),
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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        "Faker>=0.8.0,<0.9.0",
        "Django>=1.8",
        "six>=1.10.0",
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    test_suite='tests.runtests.runtests',
)
