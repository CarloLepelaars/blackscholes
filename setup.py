#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
    name='blackscholes',
    version='0.0.1',
    description='',
    author="Carlo Lepelaars",
    url="https://github.com/CarloLepelaars/blackscholes",
    keywords="finance options black scholes merton",
    maintainer='carlolepelaars',
    license='MIT',
    install_requires=[
        'numpy',
        'scipy'
    ],
    packages=find_packages(exclude=['docs'])
)
