#!/usr/bin/env python

from setuptools import setup

setup(
    name='wallet',
    version='0.1',
    py_modules=['wallet'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': ['wallet=wallet:cli']
    },
)
