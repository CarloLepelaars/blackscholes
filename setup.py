#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
    name='vollib',
    version='0.0.1',
    description='',
    maintainer='carlolepelaars',
    license='MIT',
    # install_requires = [
    #     'numpy',
    #     'pandas'
    # ],
    packages=find_packages(exclude=['docs'])
)