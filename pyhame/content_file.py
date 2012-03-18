class content_file(object):
    """ This class represents a file

        :param string path_from_content: Path to file from content
        :param config config: Config object
        :param dict special_files: Dict with special files key and content (Default: ``None``)
        :param list root_menu: Files in root menu (Default: ``None``)
        :param tuple sub_menu: Sub menu structure (Default: ``None``)
        :param booleen build: Build the file or just render it (Default: ``None``)
    """
    def __init__(self,path_from_content, config, special_files = None, root_menu = None, sub_menu = None, build = False):
        """ The main constructor of the ContentFile object, load all parameters from the created file

            :param string path_from_content: The path of content file, written by user
            :param config config: The config Object with config file parameters
        """
        self.path_from_content     = path_from_content
        self.path_from_static      = self.generate_path_from_static(config)
        self.content               = self.load_content()
        self.filename              = self.get_filename()
        self.filelink              = self.generate_filelink()
        self.permalink             = self.generate_permalink()
        self.content_html_markdown = self.content_to_html()

        if self.check_file_extension(config.extensions_to_render):
            if build:
                self.listed = True
                self.content_html_jinja = self.html_to_template(config, special_files, root_menu, sub_menu)
                self.build_html_file()

    def load_content(self):
        """ Load the natural file content, written by user

            :rtype: string
        """
        file = open(self.path_from_content, 'r')
        return file.read()
        file.close()

    def get_filename(self):
        """ Load the filename of the content file

            :rtype: string
        """
        return self.path_from_content.split('/')[-1]

    def generate_path_from_static(self, config):
        """ Generate the path from the static directorie from the content directorie 

            **i.e.**: ``content/linux/myArticle.txt -> static/linux/myArticle.txt``

            :rtype: string
        """
        tab = self.path_from_content.split('/')
        tab[0] = config.static_path
        return '/'.join(tab) 

    def content_to_html(self):
        """ Turn the original content into html content, using Markdown module

            :rtype: string
        """
        from markdown import markdown
        return markdown(self.content)

    def generate_filelink(self):
        """ Generate the file link to download the original file

            **i.e.**: ``_site/linux/myArticle.txt``

            :rtype: string
        """
        return '_' + self.path_from_content

    def generate_permalink(self):
        """ Generate the permalink of this page

            :rtype: string    
        """
        tab = self.path_from_content.split('/')
        del tab[0]
        return '/'.join(tab) + ".html"

    def html_to_template(self, config, special_files, root_menu, sub_menu):
        """ Generate the HTML content, using HTML generated from Markdown

            :param config config: The Config object with contains parameters
            :param dict special_files: Special files key and content
            :param list root_menu: The root menu
            :param tuple sub_menu: The sub menu

            :rtype: string
        """
        from jinja2 import Template

        # Loading of the global paramaters from config
        website_title           = config.website_title
        website_url             = config.website_url

        # Loading of the parameters from 'special' ContentFile
        website_welcomemsg      = special_files['welcome_message']
        website_welcome_content = special_files['welcome_content']
        website_footer          = special_files['footer']

        # Loading of the parameters from the current object
        filename                = self.filename
        content_html            = self.content_html_markdown
        filelink                = self.filelink
        permalink               = self.permalink

        # Loading of the parameters from the menu objects
        root_menu               = root_menu
        sub_menu                = sub_menu

        template                = Template(self.load_template(config))

        # The template renders the HTML with Jinja2 by giving its parameters
        self.content_html_jinja = template.render(
                        website_title   = website_title,
                        welcome_message = website_welcomemsg,
                        footer          = website_footer,
                        root_menu       = root_menu,
                        sub_menu        = sub_menu,
                        website_url     = website_url,
                        file_name       = filename,
                        file_content    = content_html,
                        filelink        = filelink, 
                        permalink       = permalink)

        return self.content_html_jinja

    def build_html_file(self):
        """ Write the HTML file with template structure and data """
        file = open(self.path_from_static + ".html", 'w')
        file.write(self.content_html_jinja)
        file.close()

    def load_template(self, config):
        """ Load the template from template file, using Jinja2

            :param config config: The config Object with config file parameters
            :return: template - The template file
        """
        template_file_view = open("%s/%s/view.html" % (config.tpl_path, config.template_name), 'r')
        template_view = template_file_view.read()
        template_file_view.close()
        return template_view

    def check_file_extension(self, extension_list):
        """ Check if the extension file match with the authorized extension list

            :param list extension_list: The list of extension the file have to match to
            :return: True if the extension is correct, False otherwise
        """
        if len(self.filename.split('.')) > 1:
            extension = self.filename.split('.')[-1]
            if extension in extension_list:
                return True
            else:
                return False
        else:
            return False
