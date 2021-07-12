import io
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as fp:
    README = fp.read()

with io.open(os.path.join(here, "VERSION")) as version_file:
    VERSION = version_file.read().strip()


setup(
    name="django-fakery",
    version=VERSION,
    url="https://github.com/fcurella/django-fakery/",
    author="Flavio Curella",
    author_email="flavio.curella@gmail.com",
    description="A model instances generator for Django",
    long_description=README,
    license="MIT",
    packages=find_packages(exclude=["docs", "tests", "tests.*"]),
    package_data={"django_fakery": ["py.typed"]},
    platforms=["any"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={"pytest11": ["django_fakery = django_fakery.plugin"]},
    install_requires=["Faker>=4.0,<5.0", "Django>=2.0", "six>=1.10.1"],
    python_requires=">=3.4",
    test_suite="tests.runtests.runtests",
)
