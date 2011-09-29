def cache(dirList):
	"""	Clear the cache

		:param list dirList: List of file/folder to check in order to remove it
	"""
	import os
	from shutil import rmtree
	
	for dir in dirList:
		if os.path.exists(dir):
			rmtree(dir)
