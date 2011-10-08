#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

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
