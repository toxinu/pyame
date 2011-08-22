#!/usr/bin/python
# -*- coding: utf-8 -*-
version = "0.7.5"

import sys
# Check Python version
if sys.version_info < (3, 1):
	print("Must use Python 3.1")
	sys.exit(0)

import os, configparser, stat, types

config 			= configparser.RawConfigParser()
pwd 			= os.getcwd()
config_file 	= "resources/pyhame.conf"
init_lock_path	= "resources/init.lock"

#############
## General ##
#############
def read_conf():
	config.read(config_file)
	section = "general"
	global content_folder, template_name, website_url, extensions_to_render
	global no_list_no_render, no_list_yes_render, tpl_path, lib_path, static_path
	global website_title
	try:
		website_title		= config.get(section, 'website_title')
		content_folder		= config.get(section, 'content_folder')
		template_name		= config.get(section, 'template_name')
		website_url			= config.get(section, 'website_url')
		extensions_to_render= config.get(section, 'extensions_to_render')
		no_list_no_render	= config.get(section, 'no_list_no_render')
		no_list_yes_render	= config.get(section, 'no_list_yes_render')
		tpl_path			= config.get(section, 'tpl_path')
		lib_path			= config.get(section, 'lib_path')
		static_path			= config.get(section, 'static_path')
	except configparser.Error as err:
		print('There is an error in pyhame.conf (%s)' % err)
		sys.exit(1)
	## Others ##
	section = "others"
	global archive
	try:
		archive				= config.get(section, 'archive')
	except configparser.Error as err:
		print('There is an error in pyhame.conf (%s)' % err)
		sys.exit(1)
	## Remote ##
	section = "remote"
	global remote, remote_host, remote_user, remote_path
	try:
		remote				= config.get(section, 'remote')
		remote_host			= config.get(section, 'remote_host')
		remote_user         = config.get(section, 'remote_user')
		remote_path         = config.get(section, 'remote_path')
	except configparser.Error as err:
		print('There is an error in pyhame.conf (%s)' % err)

#################
##  Argu Check ##
#################
def arg_check():
	def help():
		print("Usage : pyhame [OPTION] ...")
		print("    init           ->  Init your new website project")
		print("    run            ->  Run pyhame to generate website")
		print("    version        ->  Print pyhame version")
		print("    help           ->  Print this help")
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
		print(" \033[91m::\033[0m There is no config file. Must run pyhame init")
		sys.exit(0)
	else:
		read_conf()
	try:
		if sys.argv[1] == "run":
			run()
	except IndexError:
		sys.argv.append(None)
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
	global website_url
	if not website_url:
		website_url = "/"
	if not tpl_path or not lib_path or not static_path:
		print(" \033[91m::\033[0m \"tpl_path\", \"static_path\"  and \"lib_path\" must be given in pyhame.conf (general section)")
		sys.exit(0)
	####################
	## Others section ##
	####################
	# Check if archive is set
	if archive != "true" and archive != "false" or not archive:
		print(" \033[91m::\033[0m \"archive\" must be \"true\" or \"false\" in pyhame.conf (others section)")
		sys.exit(0)
	## Create defaults files
	# Check if content_folder exist, if not, create it.
	if not os.path.exists(content_folder):
		print(" \033[93m::\033[0m \"content_folder\" you have given not exist. It will be automatically create")
		os.makedirs(content_folder)
	# Check if template_name exit
	template_path = "%s/%s" % (tpl_path, template_name)
	if not os.path.exists(template_path) or not os.path.exists("%s/index.html" % template_path) or not os.path.exists("%s/view.html" % template_path):
		print(" \033[91m::\033[0m \"template_name\" you have given not exist.\n \033[93m::\033[0m These files: index.html, view.html must be in template folder.")
		sys.exit(0)
	###################
	###    Remote   ###
	###################
	# Check remote section
	if remote != "true" and remote != "false" or not remote:
		print(" \033[91m::\033[0m \"remote\" must be \"true\" or \"false\" in pyhame.conf (remote section)")
		sys.exit(0)
	if remote == "true":
		if remote_host == "":
			print(" \033[91m::\033[0m \"remote_host\" must be given in pyhame.conf (remote section)")
			sys.exit(0)
		if remote_user == "":
			print(" \033[91m::\033[0m \"remote_user\" must be given in pyhame.conf (remote section)")
			sys.exit(0)
		if remote_path == "":
			print(" \033[91m::\033[0m \"remote_path\" must be given in pyhame.conf (remote section)")
			sys.exit(0)
	print(" \033[92m::\033[0m Generate your website...")
# Init Pyhame
def init_pyhame():
	import shutil
	if os.path.exists(init_lock_path):
		print(" \033[91m::\033[0m You have already initialize your pyhame installation. You can remove init.lock file but many files will be overwrite")
		sys.exit(0)
	else:
		print(" \033[93m::\033[0m Pyhame initilization...")
		if not os.path.exists("resources"):
			if not os.path.exists("/usr/lib/pyhame/resources"):
				print(" \033[91m::\033[0m Critical resources missing. Redownload or reinstall pyhame (socketubs@gmail.com)")
				sys.exit(0)
			else:
				shutil.copytree("/usr/lib/pyhame/resources", pwd+"/resources")
		open(init_lock_path, 'a').close()
		os.utime(init_lock_path, None)
		if os.path.exists(config_file):
			shutil.copyfile(config_file, config_file+".back")
			os.remove(config_file)			
		shutil.copyfile(config_file+".default", config_file)
		read_conf()
		if not os.path.exists(content_folder):
			os.makedirs(content_folder)
		if os.path.exists(static_path):
			shutil.rmtree(static_path)
		os.makedirs(static_path)
		# Create blank special files
		special_files = ["welcome_message","footer","welcome_content"]
		for f in special_files:
			if not os.path.exists("%s/%s" % (content_folder, f)):
				tmp_file = open("%s/%s" % (content_folder, f), 'w')
				if f == "welcome_message":
					tmp_file.write("Edit welcome_message file")
				elif f == "footer":
					tmp_file.write("Edit footer file")
				elif f == "welcome_content":
					tmp_file.write("Edit welcome_content file")	
				tmp_file.close()
		print(" \033[93m::\033[0m You have to configure your resources/pyhame.conf file")

# Archive maker
def create_archive():
	import tarfile
	from time import gmtime, strftime

	# Create archives diretorie if not exist
	if not os.path.exists(pwd+"/archives"):
		os.makedirs(pwd+"/archives")

	# Create archive
	def reset(tarinfo):
		tarinfo.uid = tarinfo.gid = 0
		tarinfo.uname = tarinfo.gname = "pyhame"
		return tarinfo

	tar = tarfile.open("archives/%s.tar.gz" % strftime("%d%b%Y_%H-%M-%S"), "w:gz")
	tar.add(content_folder, filter=reset)
	tar.add(static_path, filter=reset)
	tar.close()

# Replace content_folder by static_path in urls
def re_content_static(path):
	tmp = path.split('/')
	tmp[0] = static_path
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
	sys.path.append(lib_path)
	import markdown
	file_content = markdown.markdown(brute_file)	
	html_file_content = generate_view()
	return html_file_content

# Text file parser for special files
def markdown_it(brute_content):
	sys.path.append(lib_path)
	import markdown
	return markdown.markdown(brute_content)

# Html content folder
def static_folder_maker(path):
	if not 'reset_static' in globals():
		import shutil
		if os.path.exists(static_path):
			shutil.rmtree(static_path)
		os.makedirs(static_path)
		global reset_static
		reset_static = True
	if not os.path.exists(re_content_static(path)):
		os.makedirs(re_content_static(path))

# Recover specials files in content folder
def recover_special_files():
	global special_files
	special_files = ["welcome_message","footer","welcome_content"]
	exclude_markdown = [""]
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

# List folders to not list
def no_list_no_render_listing():
	global no_list_no_render_list
	no_list_no_render_list = []
	for item in no_list_no_render.split(','):
		item = item.replace('"', '')
		no_list_no_render_list.append(item)

# List folders to not list
def no_list_yes_render_listing():
	global no_list_yes_render_list
	no_list_yes_render_list = []
	for item in no_list_yes_render.split(','):
		item = item.replace('"', '')
		no_list_yes_render_list.append(item)

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
def menu_generator():
	# Import for escape unsafe char in url
	from urllib.parse import quote
	# Create empty list to store collected folders
	global root_menu, sub_menu
	root_menu, sub_menu	= [], []
	sub_file_list = []
	aDirs 				= []
	# Iterate through root folder to collected folders
	for oDirPaths, oDirNames, oFiles in os.walk(content_folder, True, None):
		aDirs.append(oDirPaths)
		oDirNames.sort()
	for oDir in aDirs:
		if os.listdir(oDir):
			if oDir != content_folder:
				tmp_check = False
				for f in no_list_no_render_list:
					if oDir == f:
						tmp_check = True
						break
				for f in no_list_yes_render_list:
					if oDir ==f:
						tmp_check = True
						break
		for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
			oDirs.sort()
			oDirFiles.sort()
			for i in oDirFiles:
				tmp_check = False
				for f in no_list_no_render_list:
					if oDir == f:
						tmp_check = True
						break
				for f in no_list_yes_render_list:
					if oDir == f:
						tmp_check = True
						break
				if not tmp_check:
					if oDir == content_folder:
						tmp_check = False
						for f in special_files:
							if i == f:
								tmp_check = True
								break
						if not tmp_check:
							if check_file_extension(i):
								filename_without_extension = i.split('.')
								tmp_root = ("/%s.html" % quote(i),remove_extension(i))
								root_menu.append(tmp_root)
							else:
								tmp_root = ("/_%s/%s" % (quote(oPaths), quote(i)),i)
								root_menu.append(tmp_root)
					else:
						if check_file_extension(i):
							filename_without_extension = i.split('.')
							file_info = ("%s/%s.html" % (remove_content_folder_name(quote(oPaths)), quote(i)), remove_extension(i))
							sub_file_list.append(file_info)
						else:
							file_info = ("%s/%s.html" % (remove_content_folder_name(quote(oPaths)), quote(i)), remove_extension(i))
							sub_file_list.append(file_info)
			break
		if oDir != content_folder:
			if os.listdir(oDir):
				tmp_check = False
				for f in no_list_no_render_list:
					if oDir == f:
						tmp_check = True
						break
				for f in no_list_yes_render_list:
					if oDir ==f:
						tmp_check = True
						break
				if not tmp_check:
					foldername = (remove_content_folder_name(oDir), sub_file_list)
					sub_menu.append(foldername)
					sub_file_list = []

# Rendering html content files
def rendering_html_content_files():
	from urllib.parse import quote
	aDirs = []
	for oDirPaths, oDirNames, oFiles in os.walk(content_folder, True, None):
		static_folder_maker(re_content_static(oDirPaths))
		aDirs.append(oDirPaths)
		oDirNames.sort()
	for oDir in aDirs:
		for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
			global file_name, dl_file_link, permalink
			oDirs.sort()
			oDirFiles.sort()
			tmp_check = False
			for f in no_list_no_render_list:
				if oPaths == f:
					tmp_check = True
					break
			if not tmp_check:
				for i in oDirFiles:
					file_name = i
					dl_file_link = "/_%s/%s" % (quote(oPaths), quote(i))
					permalink = "%s/%s.html" % (remove_content_folder_name(quote(oPaths)), quote(i))
					if oDir == content_folder:
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
	template_file_index = open("%s/%s/index.html" % (tpl_path, template_name), 'r')
	template_content_index = template_file_index.read()
	template_file_index.close()
	return template_content_index

# Read template view
def read_template_view():
	template_file_view = open("%s/%s/view.html" % (tpl_path, template_name), 'r')
	template_content_view = template_file_view.read()
	template_file_view.close()
	return template_content_view

# Write index
def write_index(index_final):
	index = open("%s/index.html" % static_path, 'w')
	index.write(index_final)
	index.close()

# Copy template to static
def static_other():
	from distutils import dir_util

	# template
	dest_dir = static_path+"/_template" 
	src_dir = tpl_path+"/"+template_name
	dir_util.copy_tree(src_dir, dest_dir)

	# hightlight
	dest_dir = static_path+"/_other/highlight"
	src_dir = lib_path+"/highlight"
	dir_util.copy_tree(src_dir, dest_dir)

# Symlink site into static
def sym_site_static():
	src_dir 	= "../"+content_folder 
	dest_dir 	= static_path+"/_"+content_folder
	if not os.path.exists(dest_dir):
		os.symlink(src_dir, dest_dir)

# Send to Remote
def send_remote(host, user, path):
	from subprocess import getoutput
	print(" \033[93m::\033[0m Sending output at %s@%s:%s" % (user, host, path))	
	output = getoutput("ssh %s@%s \"rm -R %s/* && mkdir %s\"" % (user, host, path, path))
	output = getoutput("scp -r %s/* %s@%s:%s" % (static_path, user, host, path))
	output = getoutput("scp -r %s/* %s@%s:%s/_%s" % (content_folder, user, host, path, content_folder))

def generate_index():
	from jinja2 import Template, Environment
	template = Template(read_template_index())
	write_index(template.render(website_title=website_title, welcome_message=welcome_message, welcome_content=welcome_content, footer=footer, root_menu=root_menu, sub_menu=sub_menu, website_url=website_url))

def generate_view():
	from jinja2 import Template
	template = Template(read_template_view())
	return template.render(website_title=website_title, footer=footer, root_menu=root_menu, sub_menu=sub_menu, website_url=website_url, file_name=file_name, file_content=file_content, dl_file_link=dl_file_link, permalink=permalink)

def clear_cache():
	import shutil
	if os.path.exists("__pycache__"):
		shutil.rmtree("__pycache__")
	if os.path.exists("resources/lib/markdown/__pycache__"):
		shutil.rmtree("resources/lib/markdown/__pycache__")

##############################
# Check file ssh connection ##
##############################
def check_ssh(remote_user, remote_host):
	from subprocess import getoutput
	output = getoutput('ssh -oNumberOfPasswordPrompts=0 %s@%s "echo hello"' % (remote_user, remote_host))
	if output == "hello":
		print(" \033[92m::\033[0m Ssh connection : success !")
	else:
		print(" \033[91m::\033[0m Ssh connection : failed !")
		sys.exit(0)

######################################
# Start script #######################
######################################
def run():
	# Check every options and config file
	pre_check()
	# Create the list of folders to exlude in listing
	no_list_no_render_listing()
	no_list_yes_render_listing()
	# Create extensions to render list
	create_extensions_to_render_list()
	# Recover special files like welcome_message ...
	recover_special_files()
	# Set up content listing and other specials files
	menu_generator()
	rendering_html_content_files()
	# Set up index content
	generate_index()
	static_other()
	sym_site_static()
	clear_cache()
	if archive == "true":
		# Create archive
		create_archive()
	if remote == "true":
		# Test ssh connection
		check_ssh(remote_user, remote_host)
		# Send to remote server
		send_remote(remote_host, remote_user, remote_path)

arg_check()
