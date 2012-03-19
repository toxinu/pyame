def extension(filename, extensions_to_render):
    filename = filename.split('.')
    for extension in extensions_to_render:
        if filename[-1] == extension:
            del filename[-1]
    filename = ''.join(filename)
    return filename

def content_folder_name(path):
    tmp = path.split('/')
    tmp = tmp[1:]
    new_path = ""
    for i in tmp:
        new_path += "/"+i
    return new_path
