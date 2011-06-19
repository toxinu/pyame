#!/usr/bin/python
# -*- coding: utf-8 -*-
# Version : 0.1
import os, configparser, stat, types

config_file = "default.cnf"
section = "default"

config = configparser.RawConfigParser()
config.read(config_file)
content_folder = config.get(section, 'content_folder')
template_name = config.get(section, 'template_name')

# List content folder files
def content_listing():
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
	html_content_folder = ""
	# Iterate through root folder to collected folders
	for oDirPaths, oDirNames, oFiles in os.walk( content_folder, True, None ):
    	# Add folder to list
		aDirs.append( oDirPaths )

	# Check if folders were collected
	if len( aDirs ) < 1:
		print("No folder collected.")
	else:
		# Iterate through collected folder to get files
		for oDir in aDirs:
			html_content_folder = html_content_folder + ("<span class=\"folder_title\">%s</span>\n<ul>" % oDir)

			for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
				for i in oDirFiles:
					if oDir == content_folder:
						if i == "website_title":
							website_title_file = open("%s/%s" % (oPaths, i), 'r')
							website_title = website_title_file.readline()
							website_title = website_title.replace('\n', '')
							website_title_file.close()
						elif i == "footer":
							footer_file = open("%s/%s" % (oPaths, i), 'r')
							footer = footer_file.readline()
							footer = footer.replace('\n', '')
							footer_file.close()
						elif i == "welcome_message":
							welcome_message_file = open("%s/%s" % (oPaths, i), 'r')
							welcome_message = welcome_message_file.readline()
							welcome_message = welcome_message.replace('\n', '')
							welcome_message_file.close()
						elif i == "welcome_content":
							welcome_content_file = open("%s/%s" % (oPaths, i), 'r')
							welcome_content = welcome_content_file.read()
							welcome_content = welcome_content.replace('\n', '<br>')
							welcome_content_file.close()
						else:
							html_content_folder = html_content_folder + ("<li><a href=\"%s/%s\">%s</a></li>" % (oPaths, i, i))
					else:
						html_content_folder = html_content_folder + ("<li><a href=\"%s/%s\">%s</a></li>" % (oPaths, i, i))
				break
			html_content_folder += ("</ul>")
	return html_content_folder

# Read template
def read_template(template_name):
	template_file = open("tpl/%s/%s" % (template_name, template_name), 'r')
	template_content = template_file.read()
	template_file.close()
	return template_content

# Replace template variables
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
	template_file = template_file.replace("set_content_listing", html_content_folder)
	return template_file

# Write index
def write_index(index_final):
	index = open("index.html", 'w')
	index.write(index_final)
	index.close()

####
# Read template
template_file = read_template(template_name)
# Set up content listing and other specials files
html_content_folder = content_listing()
# Set up index content
index_content = setup_index(template_file)
# Write index.html file
write_index(index_content)
