from setuptools import find_packages, setup


VERSION = '0.0.2'

setup(
    name='django-fakery',
    version=VERSION,
    url='https://github.com/fcurella/django-factory/',
    author='Flavio Curella',
    author_email='flavio.curella@gmail.com',
    description='A model instances generator for Django',
    license='MIT',
    packages=find_packages(exclude=['*.tests']),
    platforms=["any"],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=[
        "fake-factory==0.5.3",
        "Django>=1.7",
    ],
    test_suite='django_fakery.tests.runtests.runtests',
)
