#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import os
import sys

try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

setup(
    name = 'pyame',
    version = '0.8.10',
    author = "toxinu",
    author_email = "toxinu@gmail.com",
    description = "Static website creator with Markdown syntax",
    license = open("LICENSE").read(),
    keywords = "website static markdown html",
    url = "https://github.com/toxinu/pyame",
    include_package_data = True,
    packages = ['pyame'],
    scripts = ['bin/pyame'],
    install_requires=['Markdown', 'Jinja2', 'clint']
)
