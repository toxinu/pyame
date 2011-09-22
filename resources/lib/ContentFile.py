##########################################################
# This class represents a content file written by the user
##########################################################

class ContentFile(object):

	###############
	# CONSTRUCTORS
	###############
	
	# The main constructor of the ContentFile object, load all parameters from the created file.
	# @param String path : The path of content file, written by user.
	# @param Config config : The config Object with config file parameters.
	def __init__(self, pathFromContent, config):
		""" The main constructor of the ContentFile object, load all parameters from the created file
		
			:param string pathFromContent: The path of content file, written by user
			:param Config config: The config Object with config file parameters
		"""

		# IMPORTS
		import markdown
		from jinja2 import Template

		self.pathFromContent = pathFromContent
		self.pathFromStatic
		self.contentFileName
		self.content
		self.contentHTML_markdown
		self.contentHTML_jinja
		self.listed = True
		self.fileLink
		self.permalink
		
		# Loading of attributes
		self.generatePathFromStatic()
		self.getFileName()
		self.loadContent()
		self.contentToHTML()
		self.htmlToTemplate()
		self.generateFileLink()
		self.generatePermalink(config)
		
	#########
	# METHODS
	#########
	
	# Load the natural file content, written by user.
	def loadContent(self):
		""" Load the natural file content, written by user """
		file = open(self.pathFromContent, 'r')
		self.content = file.read()
		file.close()
		
	# Load the filename of the content file
	def getFileName(self):
		""" Load the filename of the content file """
		self.contentFileName = self.pathFromContent.split('/')[-1]
	
	# Generate the path from the static repertory from the content repertory
	# i.e. : content/linux/myArticle.txt -> static/linux/myArticle.txt
	def generatePathFromStatic(self):
		""" Generate the path from the static directorie from the content directorie 
			
			**i.e.**: ``content/linux/myArticle.txt -> static/linux/myArticle.txt``
		"""
		tab = self.pathFromContent.split('/')
		tab[0] = ContentFile.conf.static_path
		self.pathFromStatic = ''.join(tab)	
	
	# Turn the original content into html content, using Markdown syntax.
	def contentToHTML(self):
		""" Turn the original content into html content, using Markdown module """
		self.contentHTML_markdown = markdown.markdown(self.content)
	
	# Create the file link to download the original file.
	# i.e: _site/linux/myArticle.txt
	def generateFileLink(self):
		""" Generate the file link to download the original file """
		self.fileLink = '_' + self.pathFromContent
	
	# Generate the permalink of this page.
	def generatePermalink(self, config):
		""" Generate the permalink of this page
		
			:param Config config: The Config object with contains parameters
		"""
		self.permalink = "NOTHING"
		
	# Generate the HTML content, using HTML generated from Markdown
	# and the template, using Jinja2.
	# @param Config config : The Config object which contains parameters
	# @param ContentFile footer : The Footer ContentFile.
	# @param ContentFile welcomeMsg : The Welcome Message ContentFile.
	# @param List rootMenu : The list of root menu.
	# @param List subMenu : The list of sub menu.
	def htmlToTemplate(self, config, footer, welcomeMsg, root_menu, sub_menu):
		""" Generate the HTML content, using HTML generated from Markdown

			:param Config config: The Config object with contains parameters
			:param ContentFile footer: The footer ContentFile
			:param ContentFile welcomeMsg: The welcome message ContentFile
			:param list rootMenu: The root menu
			:param list subMenu: The sub menu
		"""
		# Loading of the global paramaters from config
		websiteTitle = config.website_title
		websiteURL = config.website_url
		
		# Loading of the parameters from 'special' ContentFile
		websiteFooter = footer.contentHTML_markdown
		websiteWelcomeMsg = welcomeMsn.contentHTML_markdown
		
		# Loading of the parameters from the current object
		contentFileName = self.contentFileName
		contentHTML = self.contentHTML_markdown
		dlFileLink = self.fileLink
		permalink = self.permalink
		
		# Loading of the parameters from the menu objects
		rootMenu = root_menu
		subMenu = sub_menu
		
		template = self.loadTemplate(config)
		
		# The template renders the HTML with Jinja2 by giving its parameters
		self.contentHTML_jinja = template.render(	website_title 	= websiteTitle,
													welcome_message = websiteWelcomeMsg, 
													footer 			= websiteFooter, 
													root_menu 		= rootMenu, 
													sub_menu 		= subMenu, 
													website_url 	= websiteURL, 
													file_name 		= contentFileName, 
													file_content 	= contentHTML, 
													dl_file_link 	= dlFileLink, 
													permalink 		= permalink
												)
		
	# Build the HTML file with template structure and data.
	def buildHTMLfile(self):
		""" Build the HTML file with template structure and data """
		file = open(self.pathFromStatic, 'a')
		file.write(self.contentHTML_jinja)
		file.close()
		
	# Load the template from template file, using Jinja2
	# @param Config config : The config Object with config file parameters.
	# @return Template : The template file 
	def loadTemplate(self, config):
		""" Load the template from template file, using Jinja2

			:param Config config: The config Object with config file parameters
			:return: Template - The template file
		"""
		templateFile = open("%s/%s/view.html" % (config.tpl_path, config.template_name), 'r')
		templateContent = templateFileView.read()
		templateFile.close()		
		return Template(templateContent)
	
	# Check if the extension file match with the authorized extension list
	# in the config file.
	# @param List(String) extensionList : The list of extension the file have to match to.
	# @return Boolean : TRUE if the extension is correct, FALSE otherwise.
	def checkFileExtension(self, extensionList):
		""" Check if the extension file match with the authorized extension list

			:param list extensionList: The list of extension the file have to match to
			:return: True if the extension is correct, False otherwise
		"""
		if(self.contentFile.split('.') > 1):
			extension = self.contentFileName.split('.')[-1]
			if extension in extensionList:
				return true
			else:
				return false
		else:
			return false
