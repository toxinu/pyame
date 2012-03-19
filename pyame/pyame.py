#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import configparser
import types
import shutil
from clint.textui import puts, indent, colored

# Check Python version
if sys.version_info < (3, 0):
    print("Must use Python 3.0")
    sys.exit(0)

# Global declarations
global GLOBAL_CONFIG                # Config object from Config class. (import Config)
global GLOBAL_PYAME_PATH           # The path of pyame
global GLOBAL_CONFIG_FILE_PATH      # The path of config file from where the command is launched.
global GLOBAL_INITLOCK_FILE_PATH    # The path of init.lock file from where the command is launched.
global GLOBAL_PWD                   # Actual directory, where the command is launched.

# Global values
GLOBAL_PYAME_PATH = os.path.dirname(__file__)
GLOBAL_TPL_PATH = GLOBAL_PYAME_PATH + "/data/tpl"
GLOBAL_INITLOCK_FILE_PATH = "init.lock"
GLOBAL_CONFIG_FILE_PATH = "pyame.conf"
GLOBAL_PWD = os.getcwd()


#--------------------------------------------------------------------#
##  Argu Check 
#--------------------------------------------------------------------#
def main():
    def help():
        puts()
        print("        Pyame and the ame arrived, 雨.")
        puts()
        with indent(2, quote=(' :: ')):
            puts('Usage : pyame [OPTION]')
        print()
        with indent(2, quote=(' :: ')):
            puts('Actions')
        with indent(4):
            puts('init           ->  Initialize your project')
            puts('run            ->  Generate your content')
            puts('serve          ->  Run webserver')
        puts()
        with indent(2, quote=(' :: ')):
            puts('Example')
        with indent(4):
            puts('mkdir my_project')
            puts('cd my_project')
            puts('pyame init')
            puts('pyame serve')
        puts()
        from pyame import version
        with indent(2, quote=' > '):
            puts("%s" % version.check())
            puts('More informations at https://github.com/Socketubs/pyame')
    if len(sys.argv) < 2:
        help()
        sys.exit(0)
    try:
        if sys.argv[1] != "run" and sys.argv[1] != "init" and sys.argv[1] != "serve":
            help()
            sys.exit(0)
    except IndexError:
        sys.argv.append(None)
    try:
        if sys.argv[1] == "serve":
            if not os.path.exists(GLOBAL_CONFIG_FILE_PATH):
                with indent(2, quote=colored.yellow(' :: ')):
                    puts('This directory is not a pyame project')
                puts()
                with indent(2, quote=colored.green(' > ')):
                    puts('Maybe you have not initialize your project')
                    puts('So you have to run: pyame init')
                sys.exit(0)
            else:
                serve()
    except IndexError:
        sys.argv.append(None)
    try:
        if sys.argv[1] == "init":
            init_pyame()
            puts()
            run()
    except IndexError:
        sys.argv.append(None)
    try:
        if sys.argv[1] == "run":
            if not os.path.exists(GLOBAL_CONFIG_FILE_PATH):
                with indent(2, quote=colored.yellow(' :: ')):
                    puts('This directory is not a pyame project')
                puts()
                with indent(2, quote=colored.green(' > ')):
                    puts('Maybe you have not initialize your project')
                    puts('So you have to run: pyame init')
                sys.exit(0)
            else:
                run()
    except IndexError:
        sys.argv.append(None)

#--------------------------------------------------------------------#
# Init pyame
#--------------------------------------------------------------------#
def init_pyame():
    # Check if the init.lock exists
    if os.path.exists(GLOBAL_INITLOCK_FILE_PATH):
        with indent(2, quote=colored.yellow(' :: ')):
            puts('You have already initialize your project !')
            puts('You can remove init.lock file but many files will be overwrite')
            puts('Be very careful.')
        sys.exit(0)

    # Here, there is not the init.lock
    else:
        with indent(2, quote=colored.yellow(' :: ')):
            puts('Initializing your project')
            puts('Import templates and libraries')
        if not os.path.exists("tpl"):
            if not os.path.exists(GLOBAL_TPL_PATH):
                with indent(2, quote=colored.red(' :: ')):
                    puts('Critical resources missing')
                    puts('Reinstall pyame or check issues on GitHub')
                sys.exit(0)
            else:
                # Config file creation
                with indent(2, quote=colored.yellow(' :: ')):
                    puts('Create default configuration')
                shutil.copyfile(GLOBAL_PYAME_PATH + "/data/pyame.conf.default", GLOBAL_CONFIG_FILE_PATH + ".default")
                if os.path.exists(GLOBAL_CONFIG_FILE_PATH):
                    shutil.copyfile(GLOBAL_CONFIG_FILE_PATH, GLOBAL_CONFIG_FILE_PATH + ".back")
                    os.remove(GLOBAL_CONFIG_FILE_PATH)
                shutil.copyfile(GLOBAL_CONFIG_FILE_PATH + ".default", GLOBAL_CONFIG_FILE_PATH)

                # Read config file
                with indent(2, quote=colored.yellow(' :: ')):
                    puts('Load default parameters')
                from pyame import config
                GLOBAL_CONFIG = config.config(GLOBAL_CONFIG_FILE_PATH)
                with indent(2, quote=colored.yellow(' :: ')):
                    puts('Build project structure')
                puts()
                if not os.path.exists(GLOBAL_CONFIG.content_folder):
                    os.makedirs(GLOBAL_CONFIG.content_folder)
                if os.path.exists(GLOBAL_CONFIG.static_path):
                    shutil.rmtree(GLOBAL_CONFIG.static_path)
                os.makedirs(GLOBAL_CONFIG.static_path)

                shutil.copytree(GLOBAL_TPL_PATH, GLOBAL_PWD + "/tpl")
                shutil.copyfile(GLOBAL_PYAME_PATH + "/data/welcome_message", GLOBAL_CONFIG.content_folder + "/welcome_message")
                shutil.copyfile(GLOBAL_PYAME_PATH + "/data/welcome_content", GLOBAL_CONFIG.content_folder + "/welcome_content")
                shutil.copyfile(GLOBAL_PYAME_PATH + "/data/footer", GLOBAL_CONFIG.content_folder + "/footer")
                shutil.copyfile(GLOBAL_PYAME_PATH + "/data/_pyame", GLOBAL_CONFIG.content_folder + "/Pyame.md")

        open(GLOBAL_INITLOCK_FILE_PATH, 'a').close()
        os.utime(GLOBAL_INITLOCK_FILE_PATH, None)

        with indent(2, quote=colored.green(' > ')):
            puts('Success ! Your project is ready.')
            puts('You can write your docs into \"%s\" and run your project.' % GLOBAL_CONFIG.content_folder)
            puts('But get a look at \"pyame.conf\" before.')    

# Html content folder
def static_folder_maker(path):
    def replace_content_by_static(path):
        tab = path.split('/')
        tab[0] = GLOBAL_CONFIG.static_path
        return '/'.join(tab)

    if not 'reset_static' in globals():
        import shutil
        if os.path.exists(GLOBAL_CONFIG.static_path):
            shutil.rmtree(GLOBAL_CONFIG.static_path)
        os.makedirs(GLOBAL_CONFIG.static_path)
        global reset_static
        reset_static = True
    if not os.path.exists(replace_content_by_static(path)):
        os.makedirs(re_content_static(path))

def re_content_static(path):
    """ Generate the path from the static directorie from the content directorie

        **i.e.**: ``content/linux/myArticle.txt -> static/linux/myArticle.txt``
    """
    tab = path.split('/')
    tab[0] = GLOBAL_CONFIG.static_path
    return '/'.join(tab)

# Build a ContentFile object for each file in dirname directory and
# returns the list of ContentFile objects build by this way.
# @param String dirname : The name of the directory we want to look in.
# @param Boolean recursive: TRUE if we want to search in sub-directories of dirname, FALSE otherwise. Default : TRUE.
# @return: A list of ContentFiles objects.
def browse_and_build_all(dirname, no_list_no_render, special_files, root_menu, sub_menu, recursive = True):
    content_file_list = []
    static_folder_maker(dirname)
    for f in os.listdir(dirname):
        if os.path.isdir(os.path.join(dirname, f)):
            if recursive: browse_and_build_all(dirname + '/' + f, no_list_no_render, special_files, root_menu, sub_menu)
        elif os.path.isfile(os.path.join(dirname, f)):
            if not f in no_list_no_render:
                if not f in special_files:
                    content = content_file(dirname + '/' + f, GLOBAL_CONFIG, special_files, root_menu, sub_menu, build=True)
                    content_file_list.append(content)
    return content_file_list

# Browse all files in the dirname directory 
# and return a ContentFile object if the file has been found, false othewise.
# @param String dirname: The name of the directory we want to look in.
# @param String fileName: The name of the file WITHOUT EXTENSION we want to look for.
# @param Boolean recursive: TRUE if we want to search in sub-directories of dirname, FALSE otherwise. Default : TRUE.
# @return: FALSE if no file has been found, else, returns a ContentFile build from the file itself.
def browse_and_search_file(dirname, filename, recursive = True):
    for f in os.listdir(dirname):
        if os.path.isdir(os.path.join(dirname, f)):
            if recursive: browse_and_search_file(dirname + '/' + f, filename, True)
        elif os.path.isfile(os.path.join(dirname, f)):
            if f.split('.')[0] == filename:
                return content_file(dirname + "/" + f, GLOBAL_CONFIG, build = False)
    return False

# Get the special ContentFiles : "welcome_message","welcome_content","footer"
# If files do not exist, they are created with default values.
# @return: A list wich contains contentfile object from special files.
def get_special_content_files():

    def search_special_files(dirname, special_files):
        for f in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname, f)):
                if f in special_files:
                    return content_to_html(dirname + "/" + f)
        return False

    def content_to_html(special_file_to_html):
        from markdown import markdown
        file = open(special_file_to_html, 'r')
        special_file_to_html = file.read()
        file.close()
        return markdown(special_file_to_html)

    if not search_special_files(GLOBAL_CONFIG.content_folder, 'welcome_message'):
        shutil.copyfile(GLOBAL_PYAME_PATH + "/data/welcome_message", GLOBAL_CONFIG.content_folder)
    if not search_special_files(GLOBAL_CONFIG.content_folder, 'welcome_content'):
        shutil.copyfile(GLOBAL_PYAME_PATH + "/data/welcome_content", GLOBAL_CONFIG.content_folder)
    if not search_special_files(GLOBAL_CONFIG.content_folder, 'footer'):
        shutil.copyfile(GLOBAL_PYAME_PATH + "/data/footer", GLOBAL_CONFIG.content_folder)

    special_files = {}
    special_files['welcome_message'] = search_special_files(GLOBAL_CONFIG.content_folder, 'welcome_message')
    special_files['welcome_content'] = search_special_files(GLOBAL_CONFIG.content_folder, 'welcome_content')
    special_files['footer'] = search_special_files(GLOBAL_CONFIG.content_folder, 'footer')

    return special_files

# Get the index.html template from selected template in Config
# to return it to Jinja2 Template() function.
def get_template_index():
    file = open("%s/%s/index.html" % (GLOBAL_CONFIG.tpl_path, GLOBAL_CONFIG.template_name), 'r')
    template_index = file.read()
    file.close()
    return template_index

# Write index
def write_index(index_final):
    index = open("%s/index.html" % GLOBAL_CONFIG.static_path, 'w')
    index.write(index_final)
    index.close()

# Copy template to static
def static_other():
    from distutils import dir_util

    # Template
    dest_dir = GLOBAL_CONFIG.static_path + "/_template" 
    src_dir = GLOBAL_PWD + "/" + GLOBAL_CONFIG.tpl_path + "/" + GLOBAL_CONFIG.template_name
    dir_util.copy_tree(src_dir, dest_dir)

    # Hightlight
    dest_dir = GLOBAL_CONFIG.static_path + "/_other/highlight"
    src_dir = GLOBAL_PYAME_PATH + "/data/highlight"
    dir_util.copy_tree(src_dir, dest_dir)

    # Robot.txt
    robots = open("%s/robots.txt" % GLOBAL_CONFIG.static_path, 'w')
    robots.write("User-agent: *\nAllow: /")
    robots.close()


# Symlink site into static
def sym_site_static():
    src_dir     = "../" + GLOBAL_CONFIG.content_folder 
    dest_dir     = GLOBAL_CONFIG.static_path + "/_" + GLOBAL_CONFIG.content_folder
    if not os.path.exists(dest_dir):
        os.symlink(src_dir, dest_dir)

# Serve command
def serve():
    import pyame.server
    import time

    with indent(2, quote=colored.yellow(' :: ')):
        puts('Read your configuration file')

    from pyame import config
    global GLOBAL_CONFIG 
    GLOBAL_CONFIG = config.config(GLOBAL_CONFIG_FILE_PATH)
    GLOBAL_CONFIG.check()

    with indent(2, quote=colored.green(' :: ')):
        puts('Run web server')
    puts()

    pyameserver = pyame.server.Server(
            address = '127.0.0.1',
            port = '8080')

    pyameserver.start()

    while not pyameserver.is_shutdown:
        try:
            time.sleep(0.5)
        except KeyboardInterrupt:
            pyameserver.shutdown()

# Run command
def run():
    with indent(2, quote=colored.yellow(' :: ')):
        puts('Read your configuration file')

    from pyame import config
    global GLOBAL_CONFIG 
    GLOBAL_CONFIG = config.config(GLOBAL_CONFIG_FILE_PATH)
    GLOBAL_CONFIG.check()

    with indent(2, quote=colored.yellow(' :: ')):
        puts('Generate your project')
    puts()

    from pyame.content_file import content_file
    global content_file
    special_files = get_special_content_files()
    from pyame import menu
    root_menu, sub_menu = menu.generate(
            GLOBAL_CONFIG.no_list_no_render,
            GLOBAL_CONFIG.no_list_yes_render,
            GLOBAL_CONFIG.extensions_to_render,
            GLOBAL_CONFIG.content_folder,
            special_files)

    browse_and_build_all(
            GLOBAL_CONFIG.content_folder,
            GLOBAL_CONFIG.no_list_no_render,
            special_files,
            root_menu,
            sub_menu)

    from jinja2 import Template
    template = Template(get_template_index())
    html_render_index = template.render(
            website_title = GLOBAL_CONFIG.website_title,
            website_url = GLOBAL_CONFIG.website_url,
            welcome_message = special_files['welcome_message'],
            welcome_content = special_files['welcome_content'],
            footer = special_files['footer'],
            root_menu = root_menu,
            sub_menu = sub_menu)

    write_index(html_render_index)
    static_other()
    sym_site_static()

    with indent(2, quote=colored.green(' > ')):
        puts('Success ! Your project has been rendered')
        puts('You can see output into \"%s\" folder.' % GLOBAL_CONFIG.static_path)
    puts()
    with indent(2, quote=colored.blue(' > ')):
        puts('Tips: pyame serve')
        puts('See your website in your web browser')

    if GLOBAL_CONFIG.archive == "true":
        from pyame import archive
        archive_list = [GLOBAL_CONFIG.static_path, GLOBAL_CONFIG.content_folder]
        archive.create(GLOBAL_CONFIG.archive_path, archive_list)
    if GLOBAL_CONFIG.remote == "true":
        from pyame import remote
        remote.check_ssh(GLOBAL_CONFIG.remote_host, GLOBAL_CONFIG.remote_user)
        remote.push_ssh(GLOBAL_CONFIG.remote_host, GLOBAL_CONFIG.remote_user, GLOBAL_CONFIG.remote_path, GLOBAL_CONFIG.static_path)