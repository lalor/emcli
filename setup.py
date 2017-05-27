#!/usr/bin/env python
# coding: utf-8
from setuptools import setup

setup(
    name='emcli',
    version='0.2',
    author='Mingxing LAI',
    author_email='me@mingxinglai.com',
    url='https://github.com/lalor/emcli',
    description='A email client in terminal',
    packages=['emcli'],
    install_requires=['yagmail'],
    tests_require=['nose', 'tox'],
    entry_points={
        'console_scripts': [
            'emcli=emcli:main',
        ]
    }
)
