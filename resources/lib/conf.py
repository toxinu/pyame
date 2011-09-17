class configuration:
	"""Configuration file content"""
	def read(self, config_file):
		import configparser, sys
		config = configparser.RawConfigParser()
		config.read(config_file)
		section = "general"
		try:
			self.website_title           	= config.get(section, 'website_title')
			self.content_folder          	= config.get(section, 'content_folder')
			self.template_name           	= config.get(section, 'template_name')
			self.website_url             	= config.get(section, 'website_url')
			self.extensions_to_render    	= config.get(section, 'extensions_to_render')
			self.no_list_no_render       	= config.get(section, 'no_list_no_render')
			self.no_list_yes_render      	= config.get(section, 'no_list_yes_render')
			self.tpl_path                	= config.get(section, 'tpl_path')
			self.static_path             	= config.get(section, 'static_path')
		except configparser.Error as err:
			print('There is an error in pyhame.conf (%s)' % err)
			sys.exit(1)
		## Others ##
		section = "others"
		try:
			self.archive                    = config.get(section, 'archive')
			self.archive_path               = config.get(section, 'archive_path')
		except configparser.Error as err:
			print('There is an error in pyhame.conf (%s)' % err)
			sys.exit(1)
		## Remote ##
		section = "remote"
		try:
			self.remote                     = config.get(section, 'remote')
			self.remote_host                = config.get(section, 'remote_host')
			self.remote_user     	    	= config.get(section, 'remote_user')
			self.remote_path				= config.get(section, 'remote_path')
		except configparser.Error as err:
			print('There is an error in pyhame.conf (%s)' % err)

	def check(conf, logging):
		import os
		## General section
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
		if not conf.tpl_path or not conf.static_path:
			logging.error('"tpl_path", "static_path" must be given in pyhame.conf (general section)')
			print(" \033[91m::\033[0m \"tpl_path\", \"static_path\"  must be given in pyhame.conf (general section)")
			sys.exit(0)
		## Others section
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
		## Remote section
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

class build:
	def string_to_list(elements):
		""" elements : string ("txt","md"...)"""
		elements_list = []
		for element in elements.split(','):
			element = element.replace('"', '')
			elements_list.append(element)
		return elements_list
