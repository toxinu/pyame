def checkSsh(remoteHost, remoteUser):
	"""	Check ssh connection

		:param string remoteHost: Remote hostname
		:param string remoteUser: Remote username
	"""
	import sys
	from subprocess import getoutput
	output = getoutput('ssh -oNumberOfPasswordPrompts=0 %s@%s "echo hello"' % (remoteUser, remoteHost))
	if output == "hello":
		print(" \033[92m::\033[0m Ssh connection : success !")
	else:
		print(" \033[91m::\033[0m Ssh connection : failed !")
		sys.exit(0)
def pushSsh(remoteHost, remoteUser, remotePath, localPath):
	"""	Push output to remote host via ssh

		:param string remoteHost: Remote hostname
		:param string remoteUser: Remote username
		:param string remotePath: Path for remote output
		:param string localPath: Local path to output
	"""
	from subprocess import getoutput
	print(" \033[93m::\033[0m Sending output at %s@%s:%s" % (remoteUser, remoteHost, remotePath))
	output = getoutput("ssh %s@%s \"rm -R %s/* && mkdir %s\"" % (remoteUser, remoteHost, remotePath, remotePath))
	output = getoutput("scp -r %s/* %s@%s:%s" % (localPath, remoteUser, remoteHost, remotePath))
	output = getoutput("scp -r %s/* %s@%s:%s/_%s" % (localPath, remoteUser, remoteHost, remotePath, localPath))	
