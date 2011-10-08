#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
from setuptools import setup, find_packages

if sys.version_info <= (3, 0):
	print("Pyhame at least need Python 3.0.")
	exit(0)

setup(
	name="pyhame",
	version="0.8.2",
	author = "Socketubs",
    author_email = "socketubs@gmail.com",
    description = "Static website creator with Markdown syntax",
    license = "GPL",
    keywords = "website static markdown",
    url = "http://pyhame.socketubs.net/",
	packages = find_packages('src'),
	package_dir = {'':'src'},
	include_package_data=True,
	scripts = ['bin/pyhame'],
	install_requires=[
		'setuptools',
		'jinja2',
	],
)
