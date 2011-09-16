def recover(content_folder, special_files, exclude_markdown):
	import os
	gl = globals()
	for f in special_files:
		gl[f] = False
	for file in special_files:
		for i in os.listdir(content_folder):
			if i == file:
				tmp_file = open("%s/%s" % (content_folder, i), 'r')
				gl[file] = tmp_file.read()
				tmp_file.close()
				tmp_check = False
			for f in exclude_markdown:
				if i == f:
					tmp_check = True
					break
				if tmp_check:
					gl[file] = gl[file].replace('\n', '<br>')
					gl[file] = gl[file][:-4]
				else:
					gl[file] = markdown.markdown(gl[file])
