def generate(no_list_no_render, no_list_yes_render, extensions_to_render, content_folder, special_files):
    """ Walk into content folder and generate root and sub menu

        :param list no_list_no_render: File wich won't be listed
        :param list no_list_yes_render: File wich won't be listed
        :param list extensions_to_render: Extensions wich will be listed
        :param string content_folder: Content folder path
        :param dict special_files: Special files key and content

        :rtype: tuple
    """
    import os, sys
    from pyame.tools import remove
    from urllib.parse import quote
    root_menu, sub_menu, sub_file_list, aDirs = [], [], [], []
    for oDirPaths, oDirNames, oFiles in os.walk(content_folder, True, None):
        aDirs.append(oDirPaths)
        oDirNames.sort()
    for oDir in aDirs:
        if oDir.split('/')[-1][0] == '.':
            continue
        if os.listdir(oDir):
            if oDir != content_folder:
                tmp_check = False
                if oDir in no_list_no_render:
                    tmp_check = True
                    break
                if oDir in no_list_yes_render:
                    tmp_check = True
                    break
        for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
            oDirs.sort()
            oDirFiles.sort()
            for i in oDirFiles:
                if i[0] == '.':
                    continue
                tmp_check = False
                if oDir in no_list_no_render:
                    tmp_check = True
                    break
                if oDir in no_list_yes_render:
                    tmp_check = True
                    break
                if not tmp_check:
                    if oDir == content_folder:
                        tmp_check = False
                        if i in special_files:
                            tmp_check = True
                        if not tmp_check:
                            if check_file_extension(i, extensions_to_render):
                                tmp_root = ("/%s.html" % quote(i), remove.extension(i, extensions_to_render))
                                root_menu.append(tmp_root)
                            else:
                                tmp_root = ("/_%s/%s" % (quote(oPaths), quote(i)),i)
                                root_menu.append(tmp_root)
                    else:
                        if check_file_extension(i, extensions_to_render):
                            file_info = ("%s/%s.html" % (remove.content_folder_name(quote(oPaths)), quote(i)), remove.extension(i, extensions_to_render))
                            sub_file_list.append(file_info)
                        else:
                            file_info = ("%s/%s.html" % (remove.content_folder_name(quote(oPaths)), quote(i)), remove.extension(i, extensions_to_render))
                            sub_file_list.append(file_info)
            break
        if oDir != content_folder:
            if os.listdir(oDir):
                tmp_check = False
                if oDir in no_list_no_render:
                    tmp_check = True
                    break
                if oDir in no_list_yes_render:
                    tmp_check = True
                    break
                if not tmp_check:
                    foldername = (remove.content_folder_name(oDir), sub_file_list)
                    sub_menu.append(foldername)
                    sub_file_list = []
    return root_menu, sub_menu

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
