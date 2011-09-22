#!/usr/bin/python
# -*- coding: utf-8 -*-
version = "0.8.1.1"

import sys, os, configparser, stat, types, shutil, Config
sys.path.append("/usr/lib/pyhame/resources/lib")

# Check Python version
if sys.version_info < (3, 0):
	print("Must use Python 3.0")
	sys.exit(0)

# Global declarations
global GLOBAL_CONFIG                # Config object from Config class. (import Config)
global GLOBAL_PYHAME_PATH 			# The path of pyhame
global GLOBAL_LIB_PATH				# The path of pyhame lib.
global GLOBAL_CONFIG_FILE_PATH		# The path of config file from where the command is launched.
global GLOBAL_INITLOCK_FILE_PATH	# The path of init.lock file from where the command is launched.
global GLOBAL_PWD					# Actual directory, where the command is launched.

# Global values
GLOBAL_PYHAME_PATH  		= "/usr/lib/pyhame"
GLOBAL_LIB_PATH 			= "/usr/lib/pyhame/resources/lib"
GLOBAL_CONFIG_FILE_PATH 	= "resources/pyhame.conf"
GLOBAL_INITLOCK_FILE_PATH 	= "resources/init.lock"
GLOBAL_PWD 					= os.getcwd()


#--------------------------------------------------------------------#
##  Argu Check 
#--------------------------------------------------------------------#
def arg_check():
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
		if sys.argv[1] != "run" and sys.argv[1] != "version" and sys.argv[1] != "init":
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

	try:
		if sys.argv[1] == "run":
			if not os.path.exists(GLOBAL_CONFIG_FILE_PATH):
				print(" \033[91m::\033[0m There is no config file. Must run pyhame init")
				sys.exit(0)
			else:
				###############
				# RUN CALL HERE
				###############
				run()
	except IndexError:
		sys.argv.append(None)

#--------------------------------------------------------------------#
# Init Pyhame
#--------------------------------------------------------------------#
def init_pyhame():
	
	#Check if the init.lock exists
	if os.path.exists(GLOBAL_INITLOCK_FILE_PATH):
		print(" \033[91m::\033[0m You have already initialize your pyhame installation. You can remove init.lock file but many files will be overwrite")
		sys.exit(0)
		
	#Here, there is not the init.lock
	else:
		print(" \033[93m::\033[0m Pyhame initilization...")
		if not os.path.exists("resources"):
			if not os.path.exists(GLOBAL_PYHAME_PATH + "/resources"):
				print(" \033[91m::\033[0m Critical resources missing. Redownload or reinstall pyhame (socketubs@gmail.com)")
				sys.exit(0)
			else:
				shutil.copytree(GLOBAL_PYHAME_PATH + "/resources/tpl", GLOBAL_PWD + "/resources/tpl")
				shutil.copyfile(GLOBAL_PYHAME_PATH + "/resources/pyhame.conf.default", GLOBAL_CONFIG_FILE_PATH + ".default")

		open(GLOBAL_INITLOCK_FILE_PATH, 'a').close()
		
		#TO CHECK
		os.utime(GLOBAL_INITLOCK_FILE_PATH, None)
		
		#Config file creation
		if os.path.exists(GLOBAL_CONFIG_FILE_PATH):
			shutil.copyfile(GLOBAL_CONFIG_FILE_PATH, GLOBAL_CONFIG_FILE_PATH+".back")
			os.remove(GLOBAL_CONFIG_FILE_PATH)
		shutil.copyfile(GLOBAL_CONFIG_FILE_PATH+".default", GLOBAL_CONFIG_FILE_PATH)
		
		#Read config file
        #from Config import Config # utiliser from si c'est un package ou dossier, ce qui n'est pas le cas de config, importé maintenant dans le fichier en haut.
        # source : http://effbot.org/zone/import-confusion.htm
		GLOBAL_CONFIG = Config(GLOBAL_CONFIG_FILE_PATH)

		if not os.path.exists(GLOBAL_CONFIG.content_folder):
			os.makedirs(GLOBAL_CONFIG.content_folder)
		if os.path.exists(GLOBAL_CONFIG.static_path):
			shutil.rmtree(GLOBAL_CONFIG.static_path)
		os.makedirs(GLOBAL_CONFIG.static_path)
		
		# Create blank special files
		specialFiles = {"welcome_message": "Here your welcome message, edit welcome_message file in your content folder.",
						"welcome_content": "Here your welcome content, edit a welcome_content file in your content folder.",
						"footer": "Here your footer content, edit footer file in your content folder."}
		
		for key, value in specialFiles.items():
			if not os.path.exists("%s/%s" % (GLOBAL_CONFIG.content_folder, key)):
				file = open("%s/%s" % (GLOBAL_CONFIG.content_folder, key), 'w')
				file.write(value)
				file.close()
				
		print(" \033[93m::\033[0m You have to configure your resources/pyhame.conf file")		
		
# Html content folder
def static_folder_maker(path):
	if not 'reset_static' in globals():
		import shutil
		if os.path.exists(config.static_path):
			shutil.rmtree(config.static_path)
		os.makedirs(config.static_path)
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
	
# Build a ContentFile object for each file in dirname directory and
# returns the list of ContentFile objects build by this way.
# @param String dirname : The name of the directory we want to look in.
# @param Boolean recursive: TRUE if we want to search in sub-directories of dirname, FALSE otherwise. Default : TRUE.
# @return: A list of ContentFiles objects.
def browseAndBuildAll(dirname, recursive = True):
	contentFileList = []
	for f in os.listdir(dirname):
		
		if os.path.isdir(os.path.join(dirname, f)):
			if recursive: browseAndBuild(dirname + '/' + f)
			
		elif os.path.isfile(os.path.join(dirname, f)):
			contentFile = ContentFile(dirname + '/' + f, config)
			contentFileList.append(contentFile)
			
	return contentFileList
		
# Browse all files in the dirname directory 
# and return a ContentFile object if the file has been found, false othewise.
# @param String dirname: The name of the directory we want to look in.
# @param String fileName: The name of the file WITHOUT EXTENSION we want to look for.
# @param Boolean recursive: TRUE if we want to search in sub-directories of dirname, FALSE otherwise. Default : TRUE.
# @return: FALSE if no file has been found, else, returns a ContentFile build from the file itself.
def browseAndSearchFile(dirname, fileName, recursive = True):
	for f in os.listdir(dirname):
		
		if os.path.isdir(os.path.join(dirname, f)):
			if recursive: browseAndSearch(dirname + '/' + f, fileName, True)
			
		elif os.path.isfile(os.path.join(dirname, f)):
			if f.split('.')[0] == fileName:
				return ContentFile(dirname, GLOBAL_CONFIG)
		
	return False
			

# Recover special files
"""
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
"""

# Get the special ContentFiles : "welcome_message","welcome_content","footer"
# If files do not exist, they are created with default values.
# @return: A list wich contains ContentFile object from special files.
def getSpecialContentFiles():
	specialContentFilesList = []
	specialFiles = {"welcome_message": "Here your welcome message, edit by creating a welcome_message file in your content folder.",
					"welcome_content": "Here your welcome content, edit by creating a welcome_content file in your content folder.",
					"footer": "Here your footer content, edit by creating a footer file in your content folder."}
	
	for key, value in specialFiles.items():
		if not browseAndSearchFile(GLOBAL_CONFIG.content_folder, key):				# Check if file doesn't exist
			file = open("%s/%s" % (GLOBAL_CONFIG.content_folder, key), 'w')
			file.write(value)
			file.close()
			
		specialContentFilesList.append(browseAndSearchFile(GLOBAL_CONFIG.content_folder, key))
		
	return specialContentFilesList


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


# Get the index.html template from selected template in Config
# to return it to Jinja2 Template() function.
def getTemplate_index():
	file = open("%s/%s/index.html" % (GLOBAL_CONFIG.tpl_path, GLOBAL_CONFIG.template_name), 'r')
	templateIndex = file.read()
	file.close()
	return templateIndex

# Read template view
"""
def read_template_view():
	template_file_view = open("%s/%s/view.html" % (conf.tpl_path, conf.template_name), 'r')
	template_content_view = template_file_view.read()
	template_file_view.close()
	return template_content_view
"""

# Write index
def write_index(index_final):
	index = open("%s/index.html" % conf.static_path, 'w')
	index.write(index_final)
	index.close()

# Copy template to static
def static_other():
	from distutils import dir_util

	# template
	dest_dir = conf.static_path + "/_template" 
	src_dir = conf.tpl_path + "/" + conf.template_name
	dir_util.copy_tree(src_dir, dest_dir)

	# hightlight
	dest_dir = conf.static_path + "/_other/highlight"
	src_dir = lib_path + "/highlight"
	dir_util.copy_tree(src_dir, dest_dir)

# Symlink site into static
def sym_site_static():
	src_dir 	= "../" + conf.content_folder 
	dest_dir 	= conf.static_path + "/_" + conf.content_folder
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

	# Create Config object and check it	
	#from Config import Config # utiliser from si c'est un package ou dossier, ce qui n'est pas le cas de config, importé maintenant dans le fichier en haut.
    # source : http://effbot.org/zone/import-confusion.htm
    
    # Pourquoi avoir déplacé global ici au lieu de son ancien emplacement (entete) ?
    # Si on fait comme ça,  GLOBAL_CONFIG est global n'est global que lors d'un run, plus lors d'un init (or il est nécessaire lors de l'init)
	global GLOBAL_CONFIG 
	GLOBAL_CONFIG = Config(GLOBAL_CONFIG_FILE_PATH)
	GLOBAL_CONFIG.check()
	
	# Recover special files like welcome_message ...
	specialContentFiles = getSpecialContentFiles()
	welcomeMessageFile = browseAndSearchFile(GLOBAL_CONFIG.content_folder, "welcome_message", false)
	welcomeContentFile = browseAndSearchFile(GLOBAL_CONFIG.content_folder, "welcome_content", false)
	footerFile = browseAndSearchFile(GLOBAL_CONFIG.content_folder, "footer", false)
	
	
	# Set up content listing and other specials files
	import menu
	global root_menu, sub_menu
	root_menu, sub_menu = menu.generate(no_list_no_render_list, no_list_yes_render_list, extensions_to_render_list, conf.content_folder, special_files)
	rendering_html_content_files(no_list_no_render_list, special_files)
	
	# Generate index content
	templateContent_index = getTemplate_index()
	template = Template(templateContent_index)
	htmlRender_index = template.render(	config 				= 	GLOBAL_CONFIG, 
										welcome_message		=	welcomeMessageFile.content, 
										welcome_content		=	welcomeContentFile.content, 
										footer				=	footerFile.content, 
										root_menu			=	root_menu, 
										sub_menu			=	sub_menu
										)
#	htmlRender_index = template.render(website_title=conf.website_title, welcome_message=welcome_message, welcome_content=welcome_content, footer=footer, root_menu=root_menu, sub_menu=sub_menu, website_url=conf.website_url)
	
	# Set up index content
	generate_index()
	static_other()
	sym_site_static()
	if conf.archive == "true":
		import archive
		archive_list = [conf.static_path,conf.content_folder]
		archive.create(conf.archive_path, archive_list)
	if conf.remote == "true":
		import remote
		remote.check_ssh(conf.remote_host, conf.remote_user)
		remote.push_ssh(conf.remote_host, conf.remote_user, conf.remote_path, conf.static_path)
	# Clear cache
	import clear
	cache_list = ["__pycache__"]
	clear.cache(cache_list)

arg_check()
