#!/usr/bin/python
# -*- coding: utf-8 -*-
version = "0.7.5"

import sys
sys.path.append("resources")
import os, configparser, stat, types
from lib.conf import configuration as conf

# Check Python version
if sys.version_info < (3, 1):
	print("Must use Python 3.1")
	sys.exit(0)

config_file		= "resources/pyhame.conf"
init_lock_path	= "resources/init.lock"
pwd				= os.getcwd()

#################
##  Argu Check ##
#################
def arg_check():
	logging.info('Running pyhame v%s' % version)
	def help():
		print("""Usage : pyhame [OPTION] ...
	init           ->  Init your new website project
	run            ->  Run pyhame to generate website
	version        ->  Print pyhame version
	help           ->  Print this help""")
	if len(sys.argv) < 2:
		help()
		sys.exit(0)
	try:
		if sys.argv[1] == "help":
			help()
			sys.exit(0)
	except IndexError:
		sys.argv.append(None)
	try:
		if sys.argv[1] == "version":
			print(version)
			sys.exit(0)
	except IndexError:
		sys.argv.append(None)
	try:
		if sys.argv[1] == "init":
			init_pyhame()
	except IndexError:
		sys.argv.append(None)
	if not os.path.exists(config_file):
		logging.error('There is no config file. Must run pyhame init')
		print(" \033[91m::\033[0m There is no config file. Must run pyhame init")
		sys.exit(0)
	else:
		global conf
		conf.read(conf, config_file)
	try:
		if sys.argv[1] == "run":
			run()
	except IndexError:
		sys.argv.append(None)

#############
### Login ###
#############
import logging
import time

logging.basicConfig(
    filename='pyhame.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    )

#################
### Pre-Check ###
#################
def pre_check():
	#####################
	## General section ##
	#####################
	# Check if content_folder is set
	if not conf.content_folder:
		logging.error('"content_folder" must be given in pyhame.conf (general section)')
		print(" \033[91m::\033[0m \"content_folder\" must be given in pyhame.conf (general section)")
		sys.exit(0)
	if conf.content_folder == "resources" or conf.content_folder == conf.archive_path:
		logging.error('"content_folder" cant be "resources" or "%s"' % conf.archive_path)
		print(" \033[91m::\033[0m \"content_folder\" cant be \"resources\", or \"%s\".  (general section)" % archive_path)
		sys.exit(0)
	# Check if template_name is set
	if not conf.template_name:
		logging.error('"template_name" must be given in pyhame.conf (general section)')
		print(" \033[93m::\033[0m \"template_name\" must be given in pyhame.conf (general section)")
		sys.exit(0)
	# Check if website_url is set
	if not conf.website_url:
		logging.info('No website_url has be given, default will be "/"')
		conf.website_url = "/"
	if not conf.tpl_path or not conf.lib_path or not conf.static_path:
		logging.error('"tpl_path", "static_path" and "lib_path" must be given in pyhame.conf (general section)')
		print(" \033[91m::\033[0m \"tpl_path\", \"static_path\"  and \"lib_path\" must be given in pyhame.conf (general section)")
		sys.exit(0)
	####################
	## Others section ##
	####################
	# Check if archive is set
	if conf.archive != "true" and conf.archive != "false" or not conf.archive:
		logging.error('"archive" must be "true" or "false" in pyhame.conf (other section)')
		print(" \033[91m::\033[0m \"archive\" must be \"true\" or \"false\" in pyhame.conf (others section)")
		sys.exit(0)
	## Create defaults files
	# Check if content_folder exist, if not, create it.
	if not os.path.exists(conf.content_folder):
		logging.info('"content_folder" you have given not exist. It will be automatically create')
		print(" \033[93m::\033[0m \"content_folder\" you have given not exist. It will be automatically create")
		os.makedirs(conf.content_folder)
	# Check if template_name exit
	conf.template_path = "%s/%s" % (conf.tpl_path, conf.template_name)
	if not os.path.exists(conf.template_path) or not os.path.exists("%s/index.html" % conf.template_path) or not os.path.exists("%s/view.html" % conf.template_path):
		logging.error('"template_name" you have given not exist. Or index.html, view.html are not in your template directori')
		print(" \033[91m::\033[0m \"template_name\" you have given not exist.\n \033[93m::\033[0m These files: index.html, view.html must be in template folder.")
		sys.exit(0)
	###################
	###    Remote   ###
	###################
	# Check remote section
	if conf.remote != "true" and conf.remote != "false" or not conf.remote:
		logging.error('"remote" must be "true" or "false" in pyhame.conf (remote section)')
		print(" \033[91m::\033[0m \"remote\" must be \"true\" or \"false\" in pyhame.conf (remote section)")
		sys.exit(0)
	if conf.remote == "true":
		if conf.remote_host == "":
			logging.error('"remote_host" must be given in pyhame.conf (remote section)')
			print(" \033[91m::\033[0m \"remote_host\" must be given in pyhame.conf (remote section)")
			sys.exit(0)
		if conf.remote_user == "":
			logging.error('"remote_user" must be given in pyhame.conf (remote section)')
			print(" \033[91m::\033[0m \"remote_user\" must be given in pyhame.conf (remote section)")
			sys.exit(0)
		if conf.remote_path == "":
			logging.error('"remote_path" must be given in pyhame.conf (remote section)')
			print(" \033[91m::\033[0m \"remote_path\" must be given in pyhame.conf (remote section)")
			sys.exit(0)
	print(" \033[92m::\033[0m Generate your website...")
# Init Pyhame
def init_pyhame():
	import shutil
	if os.path.exists(init_lock_path):
		logging.error('You have already initilize your pyhame installation. You can remove init.lock but.. seriously ?')
		print(" \033[91m::\033[0m You have already initialize your pyhame installation. You can remove init.lock file but many files will be overwrite")
		sys.exit(0)
	else:
		logging.info('Pyhame initilization')
		print(" \033[93m::\033[0m Pyhame initilization...")
		if not os.path.exists("resources"):
			if not os.path.exists("/usr/lib/pyhame/resources"):
				logging.critical('Important resources are missing. Reinstall pyhame.')
				print(" \033[91m::\033[0m Critical resources missing. Redownload or reinstall pyhame (socketubs@gmail.com)")
				sys.exit(0)
			else:
				logging.info('Create resources project with "/usr/lib/pyhame/resources"')
				shutil.copytree("/usr/lib/pyhame/resources", pwd+"/resources")
		open(init_lock_path, 'a').close()
		os.utime(init_lock_path, None)
		if os.path.exists(config_file):
			logging.info('Backup old configuration file (pyhame.conf.back)')
			shutil.copyfile(config_file, config_file+".back")
			os.remove(config_file)
		logging.info('Create new configuration file based on "pyhame.conf.default"')
		shutil.copyfile(config_file+".default", config_file)
		conf.read(conf, config_file)
		if not os.path.exists(conf.content_folder):
			logging.info('Create %s' % conf.content_folder)
			os.makedirs(conf.content_folder)
		if os.path.exists(conf.static_path):
			logging.info('Remove %s' % conf.static_path)
			shutil.rmtree(conf.static_path)
		logging.info('Create %s' % conf.static_path)
		os.makedirs(conf.static_path)
		# Create blank special files
		special_files = ["welcome_message","footer","welcome_content"]
		for f in special_files:
			if not os.path.exists("%s/%s" % (conf.content_folder, f)):
				tmp_file = open("%s/%s" % (conf.content_folder, f), 'w')
				if f == "welcome_message":
					logging.info('Create %s file in %s' % (f, conf.content_folder))
					tmp_file.write("Edit welcome_message file")
				elif f == "footer":
					logging.info('Create %s file in %s' % (f, conf.content_folder))
					tmp_file.write("Edit footer file")
				elif f == "welcome_content":
					logging.info('Create %s file in %s' % (f, conf.content_folder))
					tmp_file.write("Edit welcome_content file")	
				tmp_file.close()
		logging.info('Don\'t forget to edit your resources/pyhame.conf')
		print(" \033[93m::\033[0m You have to configure your resources/pyhame.conf file")

# Replace content_folder by static_path in urls
def re_content_static(path):
	tmp = path.split('/')
	tmp[0] = conf.static_path
	new_path = ""
	for i in tmp:
		new_path += "/"+i
	new_path = new_path[1:]
	return new_path

# Remove content folder name in path for menu generator
def remove_content_folder_name(path):
	tmp = path.split('/')
	tmp = tmp[1:]
	new_path = ""
	for i in tmp:
		new_path += "/"+i
	return new_path

# Html content rendering
def html_content_file(path_to_file):
	html_render_file = re_content_static(path_to_file) + ".html"
	brute_file = open(path_to_file, 'r')
	html_file = open(html_render_file, 'w')
	html_file.write(text_to_html(brute_file.read()))
	html_file.close()
	brute_file.close()

# Text file parser to html for view
def text_to_html(brute_file):
	global file_content
	sys.path.append(conf.lib_path)
	import markdown
	file_content = markdown.markdown(brute_file)	
	html_file_content = generate_view()
	return html_file_content

# Text file parser for special files
def markdown_it(brute_content):
	sys.path.append(conf.lib_path)
	import markdown
	return markdown.markdown(brute_content)

# Html content folder
def static_folder_maker(path):
	if not 'reset_static' in globals():
		import shutil
		if os.path.exists(conf.static_path):
			shutil.rmtree(conf.static_path)
		os.makedirs(conf.static_path)
		global reset_static
		reset_static = True
	if not os.path.exists(re_content_static(path)):
		os.makedirs(re_content_static(path))

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

# Recover special files
def recover_special_files(content_folder, special_files, exclude_markdown):
	import os
	gl = globals()
	for f in special_files:
		gl[f] = False
	for file in special_files:
		for i in os.listdir(content_folder):
			if i == file:
				tmp_file = open("%s/%s" % (content_folder, i), 'r')
				gl[file] = tmp_file.read()
				tmp_file.close()
				tmp_check = False
			for f in exclude_markdown:
				if i == f:
					tmp_check = True
					break
				if tmp_check:
					gl[file] = gl[file].replace('\n', '<br>')
					gl[file] = gl[file][:-4]
				else:
					gl[file] = markdown.markdown(gl[file])

# Rendering html content files
def rendering_html_content_files(no_list_no_render, special_files):
	from urllib.parse import quote
	aDirs = []
	for oDirPaths, oDirNames, oFiles in os.walk(conf.content_folder, True, None):
		static_folder_maker(re_content_static(oDirPaths))
		aDirs.append(oDirPaths)
		oDirNames.sort()
	for oDir in aDirs:
		for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
			global file_name, dl_file_link, permalink
			oDirs.sort()
			oDirFiles.sort()
			tmp_check = False
			for f in no_list_no_render:
				if oPaths == f:
					tmp_check = True
					break
			if not tmp_check:
				for i in oDirFiles:
					file_name = i
					dl_file_link = "/_%s/%s" % (quote(oPaths), quote(i))
					permalink = "%s/%s.html" % (remove_content_folder_name(quote(oPaths)), quote(i))
					if oDir == conf.content_folder:
						tmp_check = False
						for f in special_files:
							if i == f:
								tmp_check = True
								break
						if not tmp_check:
							if check_file_extension(i):
								html_content_file("%s/%s" % (oPaths, i))
					else:
						if check_file_extension(i):
							html_content_file("%s/%s" % (oPaths, i))	

# Read template index
def read_template_index():
	template_file_index = open("%s/%s/index.html" % (conf.tpl_path, conf.template_name), 'r')
	template_content_index = template_file_index.read()
	template_file_index.close()
	return template_content_index

# Read template view
def read_template_view():
	template_file_view = open("%s/%s/view.html" % (conf.tpl_path, conf.template_name), 'r')
	template_content_view = template_file_view.read()
	template_file_view.close()
	return template_content_view

# Write index
def write_index(index_final):
	index = open("%s/index.html" % conf.static_path, 'w')
	index.write(index_final)
	index.close()

# Copy template to static
def static_other():
	from distutils import dir_util

	# template
	dest_dir = conf.static_path+"/_template" 
	src_dir = conf.tpl_path+"/"+conf.template_name
	dir_util.copy_tree(src_dir, dest_dir)

	# hightlight
	dest_dir = conf.static_path+"/_other/highlight"
	src_dir = conf.lib_path+"/highlight"
	dir_util.copy_tree(src_dir, dest_dir)

# Symlink site into static
def sym_site_static():
	src_dir 	= "../"+conf.content_folder 
	dest_dir 	= conf.static_path+"/_"+conf.content_folder
	if not os.path.exists(dest_dir):
		os.symlink(src_dir, dest_dir)

def generate_index():
	from jinja2 import Template, Environment
	template = Template(read_template_index())
	write_index(template.render(website_title=conf.website_title, welcome_message=welcome_message, welcome_content=welcome_content, footer=footer, root_menu=root_menu, sub_menu=sub_menu, website_url=conf.website_url))

def generate_view():
	from jinja2 import Template
	template = Template(read_template_view())
	return template.render(website_title=conf.website_title,
	welcome_message=welcome_message, footer=footer, root_menu=root_menu, sub_menu=sub_menu, website_url=conf.website_url, file_name=file_name, file_content=file_content, dl_file_link=dl_file_link, permalink=permalink)

######################################
# Start script #######################
######################################
def run():
	# Check every options and config file
	pre_check()
	# Create list of conf list entries
	from lib.conf import build
	extensions_to_render_list = build.string_to_list(conf.extensions_to_render)
	no_list_no_render_list = build.string_to_list(conf.no_list_no_render)
	no_list_yes_render_list = build.string_to_list(conf.no_list_yes_render)
	# Recover special files like welcome_message ...
	special_files = ["welcome_message","welcome_content","footer"]
	exclude_markdown = []
	recover_special_files(conf.content_folder, special_files, exclude_markdown)
	# Set up content listing and other specials files
	from lib import menu
	global root_menu, sub_menu
	root_menu, sub_menu = menu.generate(no_list_no_render_list, no_list_yes_render_list, extensions_to_render_list, conf.content_folder, special_files)
	rendering_html_content_files(no_list_no_render_list, special_files)
	# Set up index content
	logging.info('Running pyhame v%s' % version)
	generate_index()
	static_other()
	sym_site_static()
	if conf.archive == "true":
		from lib import archive
		archive_list = [conf.static_path,conf.content_folder]
		archive.create(conf.archive_path, archive_list)
	if conf.remote == "true":
		from lib import remote
		remote.check_ssh(conf.remote_host, conf.remote_user)
		remote.push_ssh(conf.remote_host, conf.remote_user, conf.remote_path, conf.static_path)
	# Clear cache
	from lib import clear
	cache_list = ["__pycache__","resources/lib/__pycache__","resources/lib/markdown/__pycache__"]
	clear.cache(cache_list)

arg_check()
