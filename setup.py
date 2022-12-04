#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
    name='blackscholes',
    version='0.0.1',
    description='',
    maintainer='carlolepelaars',
    license='MIT',
    install_requires=[
        'numpy',
        'scipy'
    ],
    packages=find_packages(exclude=['docs'])
)