#!/usr/bin/env python3

from setuptools import setup, find_packages

NAME = 'pacdb'
VERSION = '1.1.1'
DESCRIPTION = 'Pacman DB to SQLite Converter'
LONG_DESCRIPTION = 'Covnerts pacman sync databases to an sqlite database for easier querying.'
AUTHOR = 'Ryan Petris'
AUTHOR_EMAIL = 'ryan@petris.net'
LICENSE = 'GPL3'
PLATFORMS = 'Any'
URL = 'https://github.com/ryanpetris/pacdb'
DOWNLOAD_URL = 'https://github.com/ryanpetris/pacdb'
CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
    'Programming Language :: Python :: 3.13',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]
PROJECT_URLS = {
   'Bug Tracker': 'https://github.com/ryanpetris/pacdb/issues',
   'Source Code': 'https://github.com/ryanpetris/pacdb',
}

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    platforms=PLATFORMS,
    url=URL,
    download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    project_urls=PROJECT_URLS,
    python_requires='>=3.11',
    package_dir={
        '': 'src'
    },
    packages=find_packages('src'),
    entry_points={
        'console_scripts': [
            'pacdb = pacdb.cli:main'
        ]
    }
)
