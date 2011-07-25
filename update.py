#!/usr/bin/python
# -*- coding: utf-8 -*-
# Check Python version
import sys
if sys.version_info < (3, 1):
	print("Must use Python 3.1")
	sys.exit(0)

print("####################################")
print("## \033[93mUpdate script require git-core\033[0m ##")
print("####################################\n")
print(" \033[93m::\033[0m Note that you can use -f argument to force update\n")

## Checking updates commands
check_command01 = "git show-ref origin/master"
check_command02 = "git ls-remote origin -h refs/heads/master"

## Update commands
update_command01 = "git pull"

## Force commands
force_command01 = "git reset --hard HEAD"
force_command02 = "git pull"

from subprocess import getoutput

# Archive maker
def create_archive():
	import tarfile, os, configparser
	from time import gmtime, strftime

	config = configparser.RawConfigParser()
	config_file = "ressources/pyhame.conf"
	config.read(config_file)

	section = "general"
	content_folder      = config.get(section, 'content_folder')
	static_path			= config.get(section, 'static_path')

	# Create archives diretorie if not exist
	if not os.path.exists("archives"):
		os.makedirs("archives")

	# Create archive
	tar = tarfile.open("archives/%si_update.tar.gz" % strftime("%d%b%Y_%H-%M-%S"), "w:gz")
	tar.add(content_folder, filter=reset)
	tar.add(static_path_folder, filter=reset)
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

try:
	if sys.argv[1] == "force":
		print(" \033[93m::\033[0m force option set")
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
except IndexError:
	sys.argv.append(None)

if check():
	so = input(" \033[93m::\033[0m Do updates ? (A backup (_update) will be create in archives folder and a conf file backup too). [yes/NO]\n")
	if so == "yes":
		create_archive()
		conf_backup()
		update()
else:
	print("\n####################################")
	print("## \033[92mPyhame is already up to date !\033[0m ##")
	print("####################################\n")
