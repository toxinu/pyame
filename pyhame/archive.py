def create(archive_path, archive_list):
    """    Create archive of website

        :param string archivePath: Path to directorie where archives will be stored
        :param list archiveList: List of elements to archive
    """
    import tarfile, os
    from time import gmtime, strftime
    from clint.textui import puts, indent, colored    

    pwd = os.getcwd()

    # Create archives diretorie if not exist
    if not os.path.exists(pwd + "/" + archive_path):
        with indent(2, quote=colored.yellow(' :: ')):
            puts('Create archives folder')
        os.makedirs(pwd + "/" + archive_path)

    # Create archive
    def reset(tarinfo):
        tarinfo.uid = tarinfo.gid = 0
        tarinfo.uname = tarinfo.gname = "pyhame"
        return tarinfo

    archive_time = strftime("%d%b%Y_%H-%M-%S")
    tar = tarfile.open("%s/%s.tar.gz" % (archive_path, archive_time), "w:gz")

    puts()
    with indent(2, quote=colored.yellow(' :: ')):
        puts('Make website archive')
    for i in archive_list:
        tar.add(i, filter=reset)
    tar.close()
    puts()
    with indent(2, quote=colored.green(' > ')):
        puts('New archive available: %s.tar.gz' % archive_time)
