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
			self.lib_path                	= config.get(section, 'lib_path')
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
			self.remote_user         	= config.get(section, 'remote_user')
			self.remote_path		= config.get(section, 'remote_path')
		except configparser.Error as err:
			print('There is an error in pyhame.conf (%s)' % err)
