#!/usr/bin/python
# -*- coding: utf-8 -*-
# Version : 0.3-1
import sys
# Check Python version
if sys.version_info < (3, 1):
	print("Must use Python 3.1")
	sys.exit(0)

import os, configparser, stat, types

config = configparser.RawConfigParser()
config_file = "pyhame.conf"
config.read(config_file)

## General ##
section = "general"
try:
	content_folder		= config.get(section, 'content_folder')
	template_name		= config.get(section, 'template_name')
	website_url			= config.get(section, 'website_url')
	content_html		= config.get(section, 'content_html')
	extensions_to_render= config.get(section, 'extensions_to_render')
except configparser.Error as err:
	print('There is an error in pyhame.conf (%s)' % err)
	sys.exit(1)

## WebShare ##
section = "webshare"
try:
	webshare_active		= config.get(section, 'webshare')
	port_everywhere		= config.get(section, 'port_everywhere')
	port				= config.get(section, 'port')
	ip_proto			= config.get(section, 'ip_proto')
except configparser.Error as err:
	print('There is an error in pyhame.conf (%s)' % err)
	sys.exit(1)
## Others ##
section = "others"
try:
	archive				= config.get(section, 'archive')
except configparser.Error as err:
	print('There is an error in pyhame.conf (%s)' % err)
	sys.exit(1)

#################
### Pre-Check ###
#################
def pre_check():
	#####################
	## General section ##
	#####################
	# Check if content_folder is set
	if not content_folder:
		print(" \033[91m::\033[0m \"content_folder\" must be given in pyhame.conf (general section)")
		sys.exit(0)
	if content_folder == "tpl" or content_folder == "lib":
		print(" \033[91m::\033[0m \"content_folder\" cant be \"tpl\", \"lib\" or \"archives\".  (general section)")
		sys.exit(0)
	# Check if template_name is set
	global template_name
	if not template_name:
		print(" \033[93m::\033[0m \"template_name\" must be given in pyhame.conf (general section)")
		sys.exit(0)
	# Check if website_url is set
	if not website_url:
		print(" \033[91m::\033[0m \"website_url\" must be given in pyhame.conf (general section)")
		sys.exit(0)
	# Check content_html value
	if content_html != "yes" and content_html != "no" or not content_html:
		print(" \033[91m::\033[0m \"content_html\" must be \"yes\" or \"no\" in pyhame.conf (general section)")
		sys.exit(0)
	######################
	## WebShare section ##
	######################
	# Check webshare_active
	if webshare_active != "yes" and webshare_active != "no" or not webshare_active:
		print(" \033[91m::\033[0m \"webshare_active\" must be \"yes\" or \"no\" in pyhame.conf (webshare section)")
		sys.exit(0)
	if webshare_active == "yes":
		# Check if port is set
		global port
		if not port:
			print(" \033[91m::\033[0m \"port\" must be given in pyhame.conf and must be an integer (webshare section)")
			sys.exit(0)
		try:
			port = int(port)
		except ValueError:
			print(" \033[91m::\033[0m \"port\" must be an integer (webshare section)")
			sys.exit(0)
		if ip_proto != "ipv4" and ip_proto != "ipv6" or not ip_proto:
			print(" \033[91m::\033[0m \"ip_proto\" must be \"ipv4\" or \"ipv6\" in pyhame.conf (webshare section)")
			sys.exit(0)
		global port_everywhere
		if port_everywhere != "no" and port_everywhere != "yes" or not port_everywhere:
			print(" \033[91m::\033[0m \"port_everywhere\" must be \"yes\" or \"no\" in pyhame.conf (webshare section)")
			sys.exit(0)
	if webshare_active == "no":
		port_everywhere = "no"
	####################
	## Others section ##
	####################
	# Check if archive is set
	if archive != "yes" and archive != "no" or not archive:
		print(" \033[91m::\033[0m \"archive\" must be \"yes\" or \"no\" in pyhame.conf (others section)")
		sys.exit(0)
				
	## Create defaults files
	# Check if content_folder exist, if not, create it.
	if not os.path.exists(content_folder):
		print(" \033[93m::\033[0m \"content_folder\" you have given not exist. It will be automatically create")
		os.makedirs(content_folder)
	# Check if template_name exit
	template_path = "tpl/%s" % template_name
	if not os.path.exists(template_path) or not os.path.exists("%s/%s_index" % (template_path, template_name)) or not os.path.exists("%s/%s_view" % (template_path, template_name)):
		print(" \033[93m::\033[0m \"template_name\" you have given not exist.\n \033[93m::\033[0m These files: _index, _view must be in template folder. Default will be used.")
		template_name = "default"

#################
###  Plugins  ###
#################
# Import and run
def plugins_go():
	sys.path.append('lib')
	global plugins
	plugins = plugins.split(',')
	global plugins_pre_functions
	plugins_variables = ["plugin_hide_special_files"]
	gl = globals()
	for f in plugins_variables:
		gl[f] = []
	for plugin in plugins:
		print("\n \033[93m::\033[0m Import %s..." % plugin)
		exec("import plugins." + plugin)
		print(" \033[93m::\033[0m Run %s...\n" % plugin)
		# Plugins_Pre
		import configparser
		for f in plugins_variables:
			config = configparser.RawConfigParser()
			config_file = "lib/plugins/%s.conf" % plugin
			config.read(config_file)
			section = "variables"
			for each in config.get(section, f).split(','):
				gl[f].append(each)
		#exec("plugins.%s.main()" % plugin)
		print(" \033[92m::\033[0m Success")
	print(plugin_hide_special_files)

# WebShare
def webshare(port):
	import http.server, socketserver, urllib.request, re

	Handler = http.server.SimpleHTTPRequestHandler
	httpd = socketserver.TCPServer(("", port), Handler)

	if ip_proto == "ipv4":
		page = str((urllib.request.urlopen('http://ipv4.icanhazip.com/').read()))
		pub_ip = page[2:-3]
	elif ip_proto == "ipv6":
		page = str((urllib.request.urlopen('http://ipv6.icanhazip.com/').read()))
		pub_ip = page[2:-3]
	else:
		print("Wrong ip_proto argument. Use \"ipv4\" or \"ipv6\".")
		quit()
	try:
		print("\n  # Starting web server at port %s ..." % port)
		print("  ##  Tape in your browser :")
		print("  ##   http://localhost:%s for local access" % port)
		print("  ##   http://%s:%s for public access" % (pub_ip, port))
		print("  # To stop server, Ctrl-C")
		print("...")
		httpd.serve_forever()
	except KeyboardInterrupt:
		print("\n \033[93m::\033[0m Ctrl-C received, shutting down server")
		httpd.socket.close()

# Archive maker
def create_archive():
	import zipfile
	from time import gmtime, strftime

	# Create archives diretorie if not exist
	if not os.path.exists("archives"):
		os.makedirs("archives")

	# Create archive
	archive = zipfile.ZipFile('archives/%s.zip' % strftime("%d%b%Y_%H-%M-%S"), mode='w')
	archive.write(content_folder)
	archive.write("html_%s" % content_folder)
	archive.write("index.html")
	archive.write("tpl/%s" % template_name)
	archive.close()

# Html content rendering
def html_content_file(path_to_file):
	html_render_file = "html_" + path_to_file + ".html"
	brute_file = open(path_to_file, 'r')
	html_file = open(html_render_file, 'w')
	html_file.write(text_to_html(brute_file.read()))
	html_file.close()
	brute_file.close()

# Text file parser to html for view
def text_to_html(brute_file):
	global file_content
	sys.path.append('lib')
	import markdown
	file_content = markdown.markdown(brute_file)	
	template_view = read_template_view()
	html_file_content = setup_view(template_view)
	return html_file_content

# Text file parser for special files
def markdown_it(brute_content):
	sys.path.append('lib')
	import markdown
	return markdown.markdown(brute_content)

# Html content folder
def html_content_folder_make(path):
	if not 'html_content_root_delete' in globals():
		if os.path.exists("html_%s" % content_folder):
			import shutil
			shutil.rmtree("html_%s" % content_folder)
		else:
			os.makedirs("html_%s" % content_folder)
		global html_content_root_delete
		html_content_root_delete = True
	if not os.path.exists(path):
		os.makedirs(path)

# Recover specials files in content folder
def recover_special_files():
	global special_files
	special_files = ["website_title","welcome_message","footer","welcome_content"]
	exclude_markdown = ["website_title"]
	gl = globals()
	for f in special_files:
		gl[f] = False		
	for file in special_files:
		for i in os.listdir(content_folder):
			if i == file:
				tmp_file = open("%s/%s" % (content_folder, i), 'r')
				gl[file] = tmp_file.read()
				tmp_check = False
				for f in exclude_markdown:
					if i == f:
						tmp_check = True
						break
					if tmp_check:
						gl[file] = gl[file].replace('\n', '<br>')
						gl[file] = gl[file][:-4]
					else:
						gl[file] = markdown_it(gl[file])
				tmp_file.close()

# List extensions to render
def create_extensions_to_render_list():
	global extensions_to_render_list
	extensions_to_render_list = []
	for extension in extensions_to_render.split(','):
		extension = extension.replace('"', '')
		extensions_to_render_list.append(extension)

# Check file extension
def check_file_extension(filename):
	filename = filename.split('.')
	tmp_extension_check = False
	if len(filename) == 1:
		return True
	for extension in extensions_to_render_list:
		if filename[-1] == extension:
			return True
			break
	return False

# Remove extension
def remove_extension(filename):
	filename = filename.split('.')
	tmp_extension_check = False
	for extension in extensions_to_render_list:
		if filename[-1] == extension:
			del filename[-1]
	filename = ''.join(filename)
	return filename

# List content folder files
def content_listing(content_html):
	# Import for escape unsafe char in url
	from urllib.parse import quote
	# Create empty list to store collected folders
	aDirs = []
	global root_menu_01
	global root_menu_02
	global sub_menu_01
	global sub_menu_02
	root_menu_01 = ""
	root_menu_02 = ""
	sub_menu_01 = ""
	sub_menu_02 = ""
	# Iterate through root folder to collected folders
	for oDirPaths, oDirNames, oFiles in os.walk( content_folder, True, None ):
    	# Add folder to list
		if content_html == "yes":
			html_content_folder_make("html_%s" % oDirPaths)
		aDirs.append(oDirPaths)
		oDirNames.sort()
	# Check if folders were collected
	if len( aDirs ) < 1:
		print("No folder collected.")
	else:
		# Iterate through collected folder to get files
		for oDir in aDirs:
			if oDir == content_folder:
				if port_everywhere == "yes":
					root_menu_01 = root_menu_01 + ("<a href=\"http://%s:%s\" class=\"root_content_title\">%s</a>\n<ul class=\"root_content_ul\">\n" % (website_url, port, oDir))
				else:
					root_menu_01 = root_menu_01 + ("<a href=\"http://%s\" class=\"root_content_title\">%s</a>\n<ul class=\"root_content_ul\">\n" % (website_url, oDir))
			else:
				if os.listdir(oDir):
					sub_menu_01 = sub_menu_01 + ("<a href=\"#\" class=\"sub_content_title\">%s</a>\n<ul class=\"sub_content_ul\">\n" % oDir)
			for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
				global file_name
				global dl_file_link
				global permalink
				oDirs.sort()
				oDirFiles.sort()
				for i in oDirFiles:
					file_name = i
					dl_file_link = "<a href=\"/%s/%s\">download</a>" % (quote(oPaths), quote(i))
					permalink = "<a href=\"/html_%s/%s.html\">permalink</a>" % (quote(oPaths), quote(i))
					if oDir == content_folder:
						tmp_check = False
						for f in special_files:
							if i == f:
								tmp_check = True
								break
						if not tmp_check:
							if content_html == "yes":
								if check_file_extension(i):
									html_content_file("%s/%s" % (oPaths, i))
									filename_without_extension = i.split('.')					
									root_menu_01 = root_menu_01 + ("<li><a href=\"html_%s/%s.html\">%s</a></li>\n" % (quote(oPaths), quote(i), remove_extension(i)))
								else:
									root_menu_01 = root_menu_01 + ("<li><a href=\"%s/%s\">%s</a></li>\n" % (quote(oPaths), quote(i), i))									
							else:
								root_menu_01 = root_menu_01 + ("<li><a href=\"%s/%s\">%s</a></li>\n" % (quote(oPaths), quote(i), i))
					else:
						if content_html == "yes":
							if check_file_extension(i):
								html_content_file("%s/%s" % (oPaths, i))
								filename_without_extension = i.split('.')
								sub_menu_01 = sub_menu_01 + ("<li><a href=\"html_%s/%s.html\">%s</a></li>\n" % (quote(oPaths), quote(i), remove_extension(i)))
							else:
								sub_menu_01 = sub_menu_01 + ("<li><a href=\"%s/%s\">%s</a></li>\n" % (quote(oPaths), quote(i), i))
						else:
							sub_menu_01 = sub_menu_01 + ("<li><a href=\"%s/%s\">%s</a></li>\n" % (quote(oPaths), quote(i), i))
				break
			if oDir == content_folder:
				root_menu_01 += ("</ul>\n")
			else:
				if os.listdir(oDir):
					sub_menu_01 += ("</ul>\n")

# Read template index
def read_template_index():
	template_file_index = open("tpl/%s/%s_index" % (template_name, template_name), 'r')
	template_content_index = template_file_index.read()
	template_file_index.close()
	return template_content_index

# Read template view
def read_template_view():
	template_file_view = open("tpl/%s/%s_view" % (template_name, template_name), 'r')
	template_content_view = template_file_view.read()
	template_file_view.close()
	return template_content_view

# Replace template variables view
def setup_view(template_file):
	if website_title:
		template_file = template_file.replace("set_website_title", website_title)
	else:
		template_file = template_file.replace("set_website_title", "Create your website_title file")
	if footer:
		template_file = template_file.replace("set_footer", footer)
	else:
		template_file = template_file.replace("set_footer", "Create your footer file")
	template_file = template_file.replace("set_file_name", file_name)
	template_file = template_file.replace("set_file_content", file_content)
	if port_everywhere == "yes":
		template_file = template_file.replace("set_website_url", "http://%s:%s" % (website_url, port))
	else:
		template_file = template_file.replace("set_website_url", "http://%s" % website_url)
	template_file = template_file.replace("set_dl_file_link", dl_file_link)
	template_file = template_file.replace("set_permalink", permalink)
	template_file = template_file.replace("set_root_menu_01", root_menu_01)
	template_file = template_file.replace("set_sub_menu_01", sub_menu_01)
	return template_file

# Replace template variables index
def setup_index(template_file):
	if website_title:
		template_file = template_file.replace("set_website_title", website_title)
	else:
		template_file = template_file.replace("set_website_title", "Create your website_title file")
	if welcome_message:
		template_file = template_file.replace("set_welcome_message", welcome_message)
	else:
		template_file = template_file.replace("set_welcome_message", "Create your welcome_message file")
	if welcome_content:
		template_file = template_file.replace("set_welcome_content", welcome_content)
	else:
		template_file = template_file.replace("set_welcome_content", "Create your welcome_content file")
	if footer:
		template_file = template_file.replace("set_footer", footer)
	else:
		template_file = template_file.replace("set_footer", "Create your footer file")
	template_file = template_file.replace("set_root_menu_01", root_menu_01)
	template_file = template_file.replace("set_sub_menu_01", sub_menu_01)
	if port_everywhere == "yes":
		template_file = template_file.replace("set_website_url", "http://%s:%s" % (website_url, port))
	else:
		template_file = template_file.replace("set_website_url", "http://%s" % website_url)
	return template_file

# Write index
def write_index(index_final):
	index = open("index.html", 'w')
	index.write(index_final)
	index.close()

######################################
# Start script #######################
######################################
# Check every variables and folders
pre_check()
# Create extensions to render list
create_extensions_to_render_list()
# Recover special files like welcome_message ...
recover_special_files()
# Read template Index
template_file_index = read_template_index()
# Set up content listing and other specials files
content_listing(content_html)
# Set up index content
index_content = setup_index(template_file_index)
# Write index.html file
write_index(index_content)
if archive == "yes":
	# Create archive
	create_archive()
# Webshare
if webshare_active == "yes":
	webshare(port)
