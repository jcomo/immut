from setuptools import setup, find_packages

setup(
    name = 'immut',
    version = '0.1.1',
    description = "An immutable container library for python",
    url = 'https://github.com/jcomo/immut',
    author = 'Jonathan Como',
    author_email = 'jonathan.como@gmail.com',
    packages = find_packages(exclude=['docs', 'tests']),
    install_requires = [],
    classifiers = [
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords = 'development immutable container functional'
)
