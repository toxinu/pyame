import xmlrpc.client
import pip
import pkg_resources
import urllib.request, urllib.error, urllib.parse

def check():
    pypi_url = 'http://pypi.python.org/pypi'
    pypi = xmlrpc.client.ServerProxy(pypi_url)
    try:
        urllib.request.urlopen(pypi_url, timeout = 0.1)
    except urllib.error.URLError as e:
        return ('Pyhame %s (connection problem)' % pkg_resources.get_distribution("pyhame").version)

    for dist in pip.get_installed_distributions():
        if dist.project_name == 'pyhame':
            available = pypi.package_releases(dist.project_name)
            if not available:
                available = pypi.package_releases(dist.project_name.capitalize())
            if not available:
                msg = 'n/a'
            elif available[0] != dist.version:
                msg = '%s available' % available[0]
            else:
                msg = 'up to date'
            pkg_info = 'Pyhame %s' % dist.version
            return ('%s (%s)' % (pkg_info, msg))
