def file_extension(filename, extensions_to_render):
	filename = filename.split('.')
	if len(filename) == 1:
		return True
	for extension in extensions_to_render_list:
		if filename[-1] == extension:
			return True
			break
	return False

