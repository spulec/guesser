#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='guesser',
    version='0.0.1',
    description='Guesser is a library that allows you to smartly guess values '
                'to find an unkownn boundary on a function.',
    author='Steve Pulec',
    author_email='spulec@gmail',
    url='https://github.com/spulec/guesser',
    packages=find_packages(exclude=("tests", "tests.*")),
)
