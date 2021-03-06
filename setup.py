#!/usr/bin/env python
import os, codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

# reqs is a list of requirement spec strings
with open('requirements.txt') as f:
    reqs = [req.strip() for req in f]

setup(name='ctk-cli-indexer',
    version='0.6',
    description=('Python utilities for creating an ElasticSearch database '
                 'containing information on available CLI modules'),
    long_description=readme,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    author='Hans Meine, Jean-Christophe Fillion-Robin',
    author_email='hans_meine@gmx.net, jchris.fillionr@kitware.com',
    url='https://github.com/commontk/ctk-cli-indexer',
    install_requires=reqs,
    packages=['ctk_cli_indexer'],
    entry_points = {
        'console_scripts': [
            'ctk_cli_indexer = ctk_cli_indexer.main:main',
        ],
    },
    package_data={
        '': ['requirements.txt'],
    },
    )
