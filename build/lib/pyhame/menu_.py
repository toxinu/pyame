class menu(object):
	
	def __init__(self, config, extentions_to_render, special_files):
		import os, sys
		from pyhame.tools import remove

		self.content_dir            = config.content_folder
		self.no_list_no_render      = config.no_list_no_render
		self.no_list_yes_render     = config.no_list_yes_render
		self.extentions_to_render   = extentions_to_render
		self.special_files          = special_files

		self.root_menu              = []
		self.sub_menu               = []
		self.sub_menu_list          = []

	def browse_and_generate(self):
		root_menu, sub_menu, sub_file_list, aDirs = [], [], [], []
		for f in os.listdir(dirname):
			target = os.path.join(dirname, f)
			if os.path.isdir(target):
				if target == self.content_folder:
					if target in self.no_list_no_render or self.no_list_yes_render:
						break
					if target in self.special_files:
						break
					root_menu_creator(dirname, f)
				else:
					sub_menu_creator(dirname, f)
				browse_and_generate()
			elif os.path.isfile(target):
				if target in self.no_list_no_render or self.no_list_yes_render:
					break
				if target in self.special_files:
					break
					sub_menu_creator(dirname, f)

	def root_menu_creator(self, dir, file):
		from urllib.parse import quote

		element = ''

		if check_file_extension(file, self.extensions_to_render):
			element = ("/%s.html" % quote(file), remove.extension(file, extensions_to_render))
			self.root_menu.append(element)
		else:
			element = ("/_%s/%s" % (quote(dir), quote(file)), file)
			self.root_menu.append(element)

	def sub_menu_creator(self, dir, file):
		from urllib.parse import quote

		element = ''

		if check_file_extension(file, self.extensions_to_render):
			element = ("%s/%s.html" % (remove.content_folder_name(quote(dir)), quote(file)), remove.extension(file, extensions_to_render))
			self.sub_menu_list.append(element)
		else:
			element = ("%s/%s.html" % (remove.content.folder_name(quote(dir)), quote(file)), remove.extension(file, extensions_to_render))
			self.sub_menu_list.append(element)

def check_file_extension(filename, extension_list):
	""" Check if the extension file match with the authorized extension list

		:param string filename: Filename to check
		:param list extension_list: The list of extension the file have to match to
		:return: True if the extension is correct, False otherwise
	"""
	if len(filename.split('.')) > 1:
		extension = filename.split('.')[-1]
		if extension in extension_list:
			return True
		else:
			return False
	else:
		return False
