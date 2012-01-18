#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
from setuptools import setup

if sys.version_info <= (3, 0):
	print("Pyhame at least need Python 3.0.")
	exit(0)

setup(
	name = 'pyhame',
	version = '0.8.3',
	author = "Socketubs",
	author_email = "socketubs@gmail.com",
	description = "Static website creator with Markdown syntax",
	license = "AGPLv3",
	keywords = "website static markdown html",
	url = "http://pyhame.socketubs.net/",
	include_package_data = True,
	packages = ['pyhame'],
	scripts = ['bin/pyhame'],
	install_requires=['Markdown', 'Jinja2']
)
