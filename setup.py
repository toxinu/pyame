#!/usr/bin/env python
#-*- coding:utf-8 -*-
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
	scripts = ['bin/pyhame'],
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	package_data = {
        'pyhame': ['data/*'],
    }
)
