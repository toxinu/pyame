def cache(dir_list):
	import os
	from shutil import rmtree
	
	for dir in dir_list:
		if os.path.exists(dir):
			rmtree(dir)
