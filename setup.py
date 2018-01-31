#!/usr/bin/env python

from os import path
from codecs import open
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'pyq',
  version = '0.1',
  description = 'Python jsonl query engine',
  long_description=long_description,
  author = 'Lasse Hyyrynen',
  author_email = 'leh@protonmail.com',
  maintainer = 'Lasse Hyyrynen',
  maintainer_email = 'leh@protonmail.com',
  license = 'MIT',
  keywords = ['json', 'yaml', 'jq'],
  download_url = 'https://github.com/alhoo/pyq/archive/0.1.tar.gz',
  url = 'https://github.com/alhoo/pyq',
  classifier=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Topic :: Utilities'
  ],
  packages = find_packages('pyq'),
  setup_requires = [
    'setuptools>=20.2.2'
  ],
  install_requires = [
    'pygments>=2.0.0',
    'regex>=2016.3.2',
    'python-dateutil>=2.6.1',
    'PyYAML>=3.12',
    'dateparser>=0.6.0'
  ],
  tests_require = [
    'nose>=1.3.0'
  ],
  test_suite = 'tests',
  zip_safe = True,
  entry_points = {
    'console_scripts': ['pyq=pyq.__main__:main']
  }
)

