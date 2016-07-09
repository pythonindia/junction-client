#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'junction/__init__.py')) as f:
    version = re.search("^__version__ = '(\d\.\d+\.\d+(\.?(dev|a|b|rc)\d?)?)'$",
                  f.read(), re.M).group(1)

requires = ['requests==2.9.1', 'schematics==2.0.0a1']
test_requirements = requires + ['pytest==2.8.5']


setup(
    name='junction-client',
    license='MIT',
    version=version,
    description='Python API client for junction',
    url='https://github.com/pythonindia/junction-client',
    packages=['junction-client'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',,
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    install_requires=requires,
    test_requires=test_requirements
)
