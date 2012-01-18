def create(archive_path, archive_list):
	"""	Create archive of website

		:param string archivePath: Path to directorie where archives will be stored
		:param list archiveList: List of elements to archive
	"""
	import tarfile, os
	from time import gmtime, strftime

	pwd = os.getcwd()

	# Create archives diretorie if not exist
	if not os.path.exists(pwd + "/" + archive_path):
		os.makedirs(pwd + "/" + archive_path)

	# Create archive
	def reset(tarinfo):
		tarinfo.uid = tarinfo.gid = 0
		tarinfo.uname = tarinfo.gname = "pyhame"
		return tarinfo

	tar = tarfile.open("%s/%s.tar.gz" % (archive_path, strftime("%d%b%Y_%H-%M-%S")), "w:gz")
	for i in archive_list:
		tar.add(i, filter=reset)
	tar.close()
