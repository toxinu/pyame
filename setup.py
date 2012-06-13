#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.version_info <= (3, 0):
    print("Pyame at least need Python 3.0.")
    exit(0)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name = 'pyame',
    version = '0.8.8',
    author = "Geoffrey Lehée",
    author_email = "geoffrey@lehee.name",
    description = "Static website creator with Markdown syntax",
    license = open("LICENSE").read(),
    keywords = "website static markdown html",
    url = "https://github.com/Socketubs/Pyame",
    include_package_data = True,
    packages = ['pyame'],
    scripts = ['bin/pyame'],
    install_requires=['Markdown', 'Jinja2', 'clint']
)
