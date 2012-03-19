import xmlrpc.client
import pip
import pkg_resources
import urllib.request, urllib.error, urllib.parse

def check():
    pypi_url = 'http://pypi.python.org/pypi'
    try:
        pypi = xmlrpc.client.ServerProxy(pypi_url)
        urllib.request.urlopen(pypi_url, timeout = 0.1)
        for dist in pip.get_installed_distributions():
            if dist.project_name == 'pyame':
                available = pypi.package_releases(dist.project_name)
                if not available:
                    available = pypi.package_releases(dist.project_name.capitalize())
                if not available:
                    msg = 'n/a'
                elif available[0] != dist.version:
                    msg = '%s available' % available[0]
                else:
                    msg = 'up to date'
                pkg_info = 'Pyame %s' % dist.version
                return ('%s (%s)' % (pkg_info, msg))
    except urllib.error.URLError as e:
        return ('Pyame %s (connection problem)' % pkg_resources.get_distribution("pyame").version)
