#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
from setuptools import setup

if sys.version_info <= (3, 0):
    print("Pyame at least need Python 3.0.")
    exit(0)

setup(
    name = 'pyame',
    version = '0.8.5',
    author = "Socketubs",
    author_email = "geoffrey@lehee.name",
    description = "Static website creator with Markdown syntax",
    license = "AGPLv3",
    keywords = "website static markdown html",
    url = "https://github.com/Socketubs/Pyame",
    include_package_data = True,
    packages = ['pyame'],
    scripts = ['bin/pyame'],
    install_requires=['pip', 'Markdown', 'Jinja2', 'clint']
)
