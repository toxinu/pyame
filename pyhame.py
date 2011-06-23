#!/usr/bin/python
# -*- coding: utf-8 -*-
# Version : 0.2
import os, configparser, stat, types

config_file = "default.cnf"
section = "default"

config = configparser.RawConfigParser()
config.read(config_file)

content_folder		= config.get(section, 'content_folder')
template_name		= config.get(section, 'template_name')
website_url			= config.get(section, 'website_url')
content_html		= config.get(section, 'content_html')
webshare_active		= config.get(section, 'webshare')
port				= int(config.get(section, 'port'))
ip_proto			= config.get(section, 'ip_proto')
archive				= config.get(section, 'archive')

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

	print("# Starting web server at port %s ..." % port)
	print("##  Tape in your browser :")
	print("##   http://localhost:%s for local access" % port)
	print("##   http://%s:%s for public access" % (pub_ip, port))
	print("# To stop server, Ctrl-C")
	print("...")
	httpd.serve_forever()

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

# Text file parser to html
def text_to_html(brute_content):
	global file_content
	file_content = brute_content.replace('\n', '<br>')
	template_view = read_template_view()
	html_file_content = setup_view(template_view)
	return html_file_content
	
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
	gl = globals()
	for f in special_files:
		gl[f] = False		
	for file in special_files:
		for i in os.listdir(content_folder):
			if i == file:
				tmp_file = open("%s/%s" % (content_folder, i), 'r')
				gl[file] = tmp_file.read()
				gl[file] = gl[file].replace('\n', '<br>')
				gl[file] = gl[file][:-4]
				tmp_file.close()
	
# List content folder files
def content_listing(content_html):
	# Create empty list to store collected folders
	aDirs = []
	global root_html_content_folder
	global sub_html_content_folder
	root_html_content_folder = ""
	sub_html_content_folder = ""
	# Iterate through root folder to collected folders
	for oDirPaths, oDirNames, oFiles in os.walk( content_folder, True, None ):
    	# Add folder to list
		if content_html == "yes":
			html_content_folder_make("html_%s" % oDirPaths)
		aDirs.append( oDirPaths )

	# Check if folders were collected
	if len( aDirs ) < 1:
		print("No folder collected.")
	else:
		# Iterate through collected folder to get files
		for oDir in aDirs:
			if oDir == content_folder:
				root_html_content_folder = root_html_content_folder + ("<a href=\"#\" class=\"root_content_title\">%s</a>\n<ul class=\"root_content_ul\">\n" % oDir)
			else:
				sub_html_content_folder = sub_html_content_folder + ("<a href=\"#\" class=\"sub_content_title\">%s</a>\n<ul class=\"sub_content_ul\">\n" % oDir)
			for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
				global file_name
				global dl_file_link
				global permalink
				for i in oDirFiles:
					file_name = i
					dl_file_link = "<a href=\"/%s/%s\">download</a>" % (replace_spaces(oPaths), replace_spaces(i))
					permalink = "<a href=\"/html_%s/%s.html\">permalink</a>" % (replace_spaces(oPaths), replace_spaces(i))
					if oDir == content_folder:
						tmp_check = False
						for f in special_files:
							if i == f:
								tmp_check = True
								break
						if not tmp_check:
							if content_html == "yes":
								html_content_file("%s/%s" % (oPaths, i))
								root_html_content_folder = root_html_content_folder + ("<li><a href=\"html_%s/%s.html\">%s</a></li>\n" % (replace_spaces(oPaths), replace_spaces(i), i))
							else:
								root_html_content_folder = root_html_content_folder + ("<li><a href=\"%s/%s\">%s</a></li>\n" % (replace_spaces(oPaths), replace_spaces(i), i))
					else:
						if content_html == "yes":
							sub_html_content_folder = sub_html_content_folder + ("<li><a href=\"html_%s/%s.html\">%s</a></li>\n" % (replace_spaces(oPaths), replace_spaces(i), i))
							html_content_file("%s/%s" % (oPaths, i))
						else:
							sub_html_content_folder = sub_html_content_folder + ("<li><a href=\"%s/%s\">%s</a></li>\n" % (replace_spaces(oPaths), replace_spaces(i), i))
				break
			if oDir == content_folder:
				root_html_content_folder += ("</ul>\n")
			else:
				sub_html_content_folder += ("</ul>\n")

# Replace spaces by %20 in a href url
def replace_spaces(url):
	url = url.replace(" ", "%20")
	return url

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
	template_file = template_file.replace("set_website_url", "http://%s:%s" % (website_url, port))
	template_file = template_file.replace("set_dl_file_link", dl_file_link)
	template_file = template_file.replace("set_permalink", permalink)
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
	template_file = template_file.replace("set_root_menu", root_html_content_folder)
	template_file = template_file.replace("set_sub_menu", sub_html_content_folder)
	template_file = template_file.replace("set_website_url", "http://%s:%s" % (website_url, port))
	return template_file

# Write index
def write_index(index_final):
	index = open("index.html", 'w')
	index.write(index_final)
	index.close()

######################################
# Start script #######################
######################################

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
