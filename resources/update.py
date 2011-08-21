#!/usr/bin/python
# -*- coding: utf-8 -*-
# Check Python version
import sys, os
from subprocess import getoutput

config_file = "ressources/pyhame.conf"
## Checking updates commands
check_command01 = "git show-ref origin/master"
check_command02 = "git ls-remote origin -h refs/heads/master"

## Update commands
update_command01 = "git pull"

## Force commands
force_command01 = "git reset --hard HEAD"
force_command02 = "git pull"

## Clean command
clean_command01 = "git clean -dfX"

# Archive maker
def create_archive():
	import tarfile, configparser
	from time import gmtime, strftime

	config = configparser.RawConfigParser()
	config.read(config_file)

	section = "general"
	content_folder      = config.get(section, 'content_folder')
	static_path			= config.get(section, 'static_path')

	# Create archives diretorie if not exist
	if not os.path.exists("archives"):
		os.makedirs("archives")

	# Create archive
	tar = tarfile.open("archives/%s_update.tar.gz" % strftime("%d%b%Y_%H-%M-%S"), "w:gz")
	tar.add(content_folder)
	tar.add(static_path)
	tar.close()

# Create conf backup
def conf_backup():
	from shutil import copyfile
	config_back = config_file + ".back"
	copyfile(config_file, config_back)

# Check
def check():
	output = getoutput(check_command01)
	local_head = output[:40]
	print(" :: Lastest local Head :  %s" % local_head)
	
	output = getoutput(check_command02)
	remote_head = output[:40]
	print(" :: Lastest remote Head : %s" % remote_head)
	
	if local_head != remote_head:
		print("\n \033[92m::\033[0m Update available !\n")
		return True
	return False

# Update
def update():
	output = getoutput(update_command01)
	print("\n%s\n" % output)
	print("####################################")
	print("##  \033[92mYour Pyhame is up to date !\033[0m   ##")
	print("####################################\n")

# Clean 
def clean_install():
	gitignore_content = "*\n!archives\n!pyhame.py\n!ressources\n!ressources/pyhame.conf.back"
	gitignore_file = open(".gitignore", 'w')
	gitignore_file.write(gitignore_content)
	gitignore_file.close()
	output = getoutput(clean_command01)
	print(" \033[91m::\033[0m Clean your pyhame installation. Must run pyhame.py init now.")
	print("\n%s\n" % output)
	print("####################################")
	print("##  \033[92mYour Pyhame is now clean  !\033[0m   ##")
	print("####################################\n")

# Run the Update
def run(option):
	if option == "force":
		force, clean = True, False
	elif option == "clean":
		clean, force = True, False
	else:
		clean, force = False, False
	from subprocess import getoutput
	print("####################################")
	print("## \033[93mUpdate script require git-core\033[0m ##")
	print("####################################\n")
	if not force:
		print(" \033[93m::\033[0m Note that you can use force argument to force update\n")
	if not clean:
		print(" \033[93m::\033[0m Note that you can use clean argument to clean installation\n")

	if force:
		print(" \033[93m::\033[0m Force option set")
		if os.path.exists(config_file):
			create_archive()
			conf_backup()
		output = getoutput(force_command01)
		print("\n%s\n" % output)
		output = getoutput(force_command02)
		print("\n%s\n" % output)
		print("####################################")
		print("##  \033[92mYour Pyhame is up to date !\033[0m   ##")
		print("####################################\n")
		sys.exit(0)

	if clean:
		print(" \033[93m::\033[0m Clean option set")
		if os.path.exists(config_file):
			create_archive()
			conf_backup()
		clean_install()
		sys.exit(0)

	if check():
		so = input(" \033[93m::\033[0m Do updates ? (A backup (_update) will be create in archives folder and a conf file backup too). [yes/NO]\n")
		if so == "yes":
			if os.path.exists(config_file):
				create_archive()
				conf_backup()
			update()
	else:
		print("\n####################################")
		print("## \033[92mPyhame is already up to date !\033[0m ##")
		print("####################################\n")

# Update Pyhame
def update_pyhame(force):
	sys.path.append("ressources")
	import update
	update.run(force)
	sys.exit(0)

# Clean Pyhame install
def clean_pyhame():
	sys.path.append("ressources")
	import update
	update.run("clean")
	sys.exit(0)

def arg_check():
	def help():
			print("Usage : ./update [OPTION] ...")
			print("    update         ->  Update Pyhame installation via git")
			print("    update force   ->  Force Update of Pyhame")
			print("    clean          ->  Clean Pyhame installation (Exclude: archives folder)")
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
		if sys.argv[1] == "update":
			if len(sys.argv) > 2:
				if sys.argv[2] == "force":
					force = "force"
				else:
					force = False
			else:
				force = False
			update_pyhame(force)
	except IndexError:
		sys.argv.append(None)
	try:
		if sys.argv[1] == "clean":
			clean_pyhame()
	except IndexError:
		sys.argv.append(None)

arg_check()
