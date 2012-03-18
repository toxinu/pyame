import http.server
import logging
import os
import sys
import re
import threading
import configparser
from urllib.parse import urlparse
from clint.textui import puts, indent, colored

logger = logging.getLogger("pyhame.server")

class Server(threading.Thread):
    def __init__(self, address='127.0.0.1', port='8080'):
        self.port = int(port)
        self.address = address
        if self.address == "0.0.0.0":
            #Bind to all addresses available
            address = ""
        threading.Thread.__init__(self)
        self.is_shutdown = False
        server_address = (address, self.port)
        HandlerClass = PyhameRequestHandler
        ServerClass = http.server.HTTPServer
        HandlerClass.protocol_version = "HTTP/1.0"
        self.httpd = ServerClass(server_address, HandlerClass)
        self.sa = self.httpd.socket.getsockname()

    def run(self):
        with indent(2, quote=colored.green(' > ')):
            puts("I'm here for you my Lord.")
            puts("Open your web browser on http://%s:%s" % (self.address, self.port))
            puts("Press Ctrl-C to stop it.")
        self.httpd.serve_forever()

    def shutdown(self):
        puts()
        with indent(2, quote=colored.red(' > ')):
            puts("Ok ok... I'm shutting down webserver")
        self.httpd.shutdown()
        self.httpd.socket.close()
        self.is_shutdown = True

class PyhameRequestHandler(http.server.SimpleHTTPRequestHandler):

    error_template = """
<head>
<title>Error response</title>
</head>
<body>
<h1>404 Error</h1>
Your Blogofile site is configured for a subdirectory, maybe you were looking
for the root page? : <a href="{0}">{1}</a>
</body>"""

    def __init__(self, *args, **kwargs):
        config = configparser.RawConfigParser()
        config.read('pyhame.conf')
        self.static_path = config.get('general', 'static_path')
        path = urlparse('').path
        self.PYHAME_SUBDIR_ERROR = self.error_template.format(path, path)
        http.server.SimpleHTTPRequestHandler.__init__(
                self, *args, **kwargs)

    def translate_path(self, path):
        site_path = urlparse('').path
        if(len(site_path.strip("/")) > 0 and
                not path.startswith(site_path)):
            self.error_message_format = self.PYHAME_SUBDIR_ERROR
            return "" #Results in a 404

        p = http.server.SimpleHTTPRequestHandler.translate_path(
            self, path)
        if len(site_path.strip("/")) > 0:
            build_path = os.path.join(
                os.getcwd(),
                util.path_join(site_path.strip("/")))
        else:
            build_path = os.getcwd()
        build_path = p.replace(build_path, os.path.join(os.getcwd(),self.static_path))
        return build_path

    def log_message(self, format, *args):
        pass
