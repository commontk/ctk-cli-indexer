#!/usr/bin/env python
import os, codecs
from setuptools import setup
from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README
with codecs.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    readme = f.read()

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements(os.path.join(here, 'requirements.txt'))

# reqs is a list of requirement spec strings
reqs = [str(ir.req) for ir in install_reqs]

setup(name='ctk-cli-indexer',
    version='0.1.dev3',
    description=('Python utilities for creating an ElasticSearch database '
                 'containing information on available CLI modules'),
    long_description=readme,
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2'
    ],
    author='Hans Meine, Jean-Christophe Fillion-Robin',
    author_email='hans_meine@gmx.net, jchris.fillionr@kitware.com',
    url='https://github.com/commontk/ctk-cli-indexer',
    install_requires=reqs,
    scripts=['cli_to_json.py', 'index_from_json.py'],
    package_data={
        '': ['requirements.txt'],
    },
    )
