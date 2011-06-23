#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Version : 0.1
import os, ConfigParser, stat, types
from io import open

config_file = u"default.cnf"
section = u"default"

config = ConfigParser.RawConfigParser()
config.read(config_file)

content_folder		= config.get(section, u'content_folder')
template_name		= config.get(section, u'template_name')
website_url			= config.get(section, u'website_url')
content_html		= config.get(section, u'content_html')
webshare_active		= config.get(section, u'webshare')
port				= int(config.get(section, u'port'))
ip_proto            = config.get(section, 'ip_proto')

# WebShare
def webshare(port):
	import re
	import urllib2, urllib
	import SimpleHTTPServer, SocketServer

	Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
	httpd = SocketServer.TCPServer(("", port), Handler)

	if ip_proto == "ipv4":
		page = str((urllib2.urlopen('http://ipv4.icanhazip.com/').read()))
	elif ip_proto == "ipv6":
		page = str((urllib2.urlopen('http://ipv6.icanhazip.com/').read()))
	else:
		print("Wrong ip_proto argument. Use \"ipv4\" or \"ipv6\". Auto is used...")
		page = str((urllib.request.urlopen('http://icanhazip.com/').read()))	
	ips = re.findall(u'(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})\.(?:[\d]{1,3})', page)
	pub_ip = unicode(ips[0])

	print u"# Starting web server at port %s ..." % port
	print u"##  Tape in your browser :"
	print u"##   http://localhost:%s for local access" % port
	print u"##   http://%s:%s for public access" % (pub_ip, port)
	print u"# To stop server, Ctrl-C"
	print u"..."
	httpd.serve_forever()

# Html content rendering
def html_content_file(path_to_file):
	html_render_file = u"html_" + path_to_file + u".html"
	brute_file = open(path_to_file, u'r')
	html_file = open(html_render_file, u'w')
	html_file.write(text_to_html(brute_file.read()))
	html_file.close()
	brute_file.close()

# Text file parser to html
def text_to_html(brute_content):
	global file_content
	file_content = brute_content.replace(u'\n', u'<br>')
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

# List content folder files
def content_listing(content_html):
	global website_title
	global welcome_message
	global footer
	global welcome_content
	website_title = False
	welcome_message = False
	footer = False
	welcome_content = False
	# Create empty list to store collected folders
	aDirs = []
	global root_html_content_folder
	global sub_html_content_folder	
	root_html_content_folder = u""
	sub_html_content_folder = u""
	# Iterate through root folder to collected folders
	for oDirPaths, oDirNames, oFiles in os.walk( content_folder, True, None ):
    	# Add folder to list
		if content_html == u"yes":
			html_content_folder_make(u"html_%s" % oDirPaths)
		aDirs.append( oDirPaths )

	# Check if folders were collected
	if len( aDirs ) < 1:
		print u"No folder collected."
	else:
		# Iterate through collected folder to get files
		for oDir in aDirs:
			if oDir == content_folder:
				 root_html_content_folder = root_html_content_folder + ("<ul class=\"root_content_ul\"><a href=\"#\" class=\"root_content_title\">%s</a>\n" % oDir)
			else:
				sub_html_content_folder = sub_html_content_folder + ("<ul class=\"sub_content_ul\"><a href=\"#\" class=\"sub_content_title\">%s</a>\n" % oDir)
			for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
				global file_name
				for i in oDirFiles:
					file_name = i
					if oDir == content_folder:
						if i == u"website_title":
							website_title_file = open(u"%s/%s" % (oPaths, i), u'r')
							website_title = website_title_file.readline()
							website_title = website_title.replace(u'\n', u'')
							website_title_file.close()
						elif i == u"footer":
							footer_file = open(u"%s/%s" % (oPaths, i), u'r')
							footer = footer_file.readline()
							footer = footer.replace(u'\n', u'')
							footer_file.close()
						elif i == u"welcome_message":
							welcome_message_file = open(u"%s/%s" % (oPaths, i), u'r')
							welcome_message = welcome_message_file.readline()
							welcome_message = welcome_message.replace(u'\n', u'')
							welcome_message_file.close()
						elif i == u"welcome_content":
							welcome_content_file = open(u"%s/%s" % (oPaths, i), u'r')
							welcome_content = welcome_content_file.read()
							welcome_content = welcome_content.replace(u'\n', u'<br>')
							welcome_content_file.close()
						else:
							if content_html == u"yes":
								html_content_file(u"%s/%s" % (oPaths, i))
								root_html_content_folder = root_html_content_folder + ("<li><a href=\"html_%s/%s.html\">%s</a></li>\n" % (replace_spaces(oPaths), replace_spaces(i), i))
							else:
								root_html_content_folder = root_html_content_folder + ("<li><a href=\"%s/%s\">%s</a></li>\n" % (replace_spaces(oPaths), replace_spaces(i), i))
					else:
						if content_html == u"yes":
							sub_html_content_folder = sub_html_content_folder + ("<li><a href=\"html_%s/%s.html\">%s</a></li>\n" % (replace_spaces(oPaths), replace_spaces(i), i))
							html_content_file(u"%s/%s" % (oPaths, i))
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
	template_file_index = open(u"tpl/%s/%s_index" % (template_name, template_name), u'r')
	template_content_index = template_file_index.read()
	template_file_index.close()
	return template_content_index

# Read template view
def read_template_view():
	template_file_view = open(u"tpl/%s/%s_view" % (template_name, template_name), u'r')
	template_content_view = template_file_view.read()
	template_file_view.close()
	return template_content_view

# Replace template variables view
def setup_view(template_file):
	if website_title:
		template_file = template_file.replace(u"set_website_title", website_title)
	else:
		template_file = template_file.replace(u"set_website_title", u"Create your website_title file")
	if footer:
		template_file = template_file.replace(u"set_footer", footer)
	else:
		template_file = template_file.replace(u"set_footer", u"Create your footer file")
	template_file = template_file.replace(u"set_file_name", file_name)
	template_file = template_file.replace(u"set_file_content", file_content)
	template_file = template_file.replace(u"set_website_url", u"http://%s:%s" % (website_url, port))
	return template_file

# Replace template variables index
def setup_index(template_file):
	if website_title:
		template_file = template_file.replace(u"set_website_title", website_title)
	else:
		template_file = template_file.replace(u"set_website_title", u"Create your website_title file")
	if welcome_message:
		template_file = template_file.replace(u"set_welcome_message", welcome_message)
	else:
		template_file = template_file.replace(u"set_welcome_message", u"Create your welcome_message file")
	if welcome_content:
		template_file = template_file.replace(u"set_welcome_content", welcome_content)
	else:
		template_file = template_file.replace(u"set_welcome_content", u"Create your welcome_content file")
	if footer:
		template_file = template_file.replace(u"set_footer", footer)
	else:
		template_file = template_file.replace(u"set_footer", u"Create your footer file")
	template_file = template_file.replace(u"set_root_menu", root_html_content_folder)
	template_file = template_file.replace(u"set_sub_menu", sub_html_content_folder)
	template_file = template_file.replace(u"set_website_url", u"http://%s:%s" % (website_url, port))
	return template_file

# Write index
def write_index(index_final):
	index = open(u"index.html", u'w')
	index.write(index_final)
	index.close()

####
# Read template Index
template_file_index = read_template_index()
# Set up content listing and other specials files
content_listing(content_html)
# Set up index content
index_content = setup_index(template_file_index)
# Write index.html file
write_index(index_content)
# Webshare
if webshare_active == u"yes":
	webshare(port)
