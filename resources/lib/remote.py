def check_ssh(remote_host, remote_user):
	import sys
	from subprocess import getoutput
	output = getoutput('ssh -oNumberOfPasswordPrompts=0 %s@%s "echo hello"' % (remote_user, remote_host))
	if output == "hello":
		print(" \033[92m::\033[0m Ssh connection : success !")
	else:
		print(" \033[91m::\033[0m Ssh connection : failed !")
		sys.exit(0)
def push_ssh(remote_host, remote_user, remote_path, local_path):
	from subprocess import getoutput
	print(" \033[93m::\033[0m Sending output at %s@%s:%s" % (remote_user, remote_host, remote_path))
	output = getoutput("ssh %s@%s \"rm -R %s/* && mkdir %s\"" % (remote_user, remote_host, remote_path, remote_path))
	output = getoutput("scp -r %s/* %s@%s:%s" % (local_path, remote_user, remote_host, remote_path))
	output = getoutput("scp -r %s/* %s@%s:%s/_%s" % (local_path, remote_user, remote_host, remote_path, local_path))	
