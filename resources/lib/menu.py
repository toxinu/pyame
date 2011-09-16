def generate(no_list_no_render, no_list_yes_render, extensions_to_render, content_folder, special_files):
	import os
	from urllib.parse import quote
	from tools import check
	root_menu, sub_menu, sub_file_list, aDirs = [], [], [], []
	for oDirPaths, oDirNames, oFiles in os.walk(content_folder, True, None):
		aDirs.append(oDirPaths)
		oDirNames.sort()
	for oDir in aDirs:
		if os.listdir(oDir):
			if oDir != content_folder:
				tmp_check = False
				for f in no_list_no_render:
					if oDir == f:
						tmp_check = True
						break
				for f in no_list_yes_render:
					if oDir ==f:
						tmp_check = True
						break
		for oPaths, oDirs, oDirFiles in os.walk( oDir, True, None ):
			oDirs.sort()
			oDirFiles.sort()
			for i in oDirFiles:
				tmp_check = False
				for f in no_list_no_render:
					if oDir == f:
						tmp_check = True
						break
				for f in no_list_yes_render:
					if oDir == f:
						tmp_check = True
						break
				if not tmp_check:
					if oDir == content_folder:
						tmp_check = False
						for f in special_files:
							if i == f:
								tmp_check = True
								break
						if not tmp_check:
							if check_file_extension(i):
								filename_without_extension = i.split('.')
								tmp_root = ("/%s.html" % quote(i),tools.remover.extension(i, extensions_to_render))
								root_menu.append(tmp_root)
							else:
								tmp_root = ("/_%s/%s" % (quote(oPaths), quote(i)),i)
								root_menu.append(tmp_root)
					else:
						if check_file_extension(i):
							filename_without_extension = i.split('.')
							file_info = ("%s/%s.html" % (tools.remove.content_folder_name(quote(oPaths)), quote(i)), toots.remove.extension(i, extensions_to_render))
							sub_file_list.append(file_info)
						else:
							file_info = ("%s/%s.html" % (remove.content.folder_name(quote(oPaths)), quote(i)), toots.remove.extension(i, extensions_to_render))
							sub_file_list.append(file_info)
			break
		if oDir != content_folder:
			if os.listdir(oDir):
				tmp_check = False
				for f in no_list_no_render:
					if oDir == f:
						tmp_check = True
						break
				for f in no_list_yes_render:
					if oDir ==f:
						tmp_check = True
						break
				if not tmp_check:
					foldername = (tools.remove.content_folder_name(oDir), sub_file_list)
					sub_menu.append(foldername)
					sub_file_list = []
	return root_menu, sub_menu
