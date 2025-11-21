# encoding: utf-8
"""
Main doctor entry point.
This is a HTTP server which receives commands from the DoctorKernel Java class
"""

import dataiku  # going first is usually bad practise but it shut downs some warning
import sys
import logging

import urlparse
import cgi
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import commands

from . import DoctorException
from dataiku.core import dkujson as json
from dataiku.core import debugging
from dkuapi import json_api

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
debugging.install_handler()

def handle_generic_error(error, command=None, arg=None):
    logging.exception("API call failed : " + str(command))
    return {
        "code": "-1",
        "errorType": error.__class__.__name__,
        "message": str(error),
        "command": command,
        "arg": arg
    }


def handle_doctor_error(error):
    logging.exception("API call failed")
    return {
        "code": error.code,
        "errorType": error.errorType,
        "message": error.message
    }


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


COMMANDS = {
    command_name: json_api(command_method)
    for (command_name, command_method) in commands._list_commands()
}


class RequestHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        # Work around a bug in Python < 2.7.5, whereas creating
        # a multiprocessing ThreadPool on any thread other than main 
        # fails.
        # See http://bugs.python.org/issue14881
        import threading, weakref
        threading.current_thread()._children = weakref.WeakKeyDictionary()

        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            form = cgi.parse_multipart(self.rfile, pdict, keep_blank_values=True)
        else:
            length = int(self.headers.getheader('content-length'))
            d = self.rfile.read(length)
            form = urlparse.parse_qs(d)
        form.setdefault("arg", ["{}"])

        code = 500
        ret = {"error": "Unknown error"}
        try:
            command = form["command"][0]
            arg = form["arg"][0]
            # TODO make it proper logging.
            #print "command", command
            #print "arg", arg
            if command not in COMMANDS:
                raise ValueError("Command %s is unknown." % command)
            else:
                logging.info("RUNNING COMMAND %s" % command)
                api_command = COMMANDS[command]
                ret = api_command(arg)
                code = 200
        except DoctorException as e:
            code = 400
            ret = handle_doctor_error(e)
        except ValueError as e:
            code = 403
            ret = handle_generic_error(e, command=command, arg=arg)
        except Exception as e:
            code = 500
            ret = handle_generic_error(e)
            logging.warning("Handle failed")
        finally:
            self.send_response(code)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(ret))


def usage():
    print """
    python main.py <server port>
    """


def serve(kernel_id, port=0):
    # Bind on an ephemeral port
    ts = ThreadingServer(('', port), RequestHandler)
    myport = ts.server_port
    # Register to the backend

    import urllib
    import urllib2
    import time
    import os
    while port == 0:
        logging.info("Trying to register my port : %d" % myport)
        try:
            url = "http://localhost:" + os.getenv("DKU_BACKEND_PORT") + "/dip/api/models/kernel-register"
            qs = urllib.urlencode({"kernelId": kernel_id, "port": myport})
            req = urllib2.Request(url, qs)
            urllib2.urlopen(req).read()
            logging.info("Registered, starting service")
            break
        except Exception, e:
            logging.warning("Register failed", e)
            time.sleep(1)

    logging.info("Service starting on port %d" % myport)
    ts.serve_forever()


if __name__ == "__main__":
    serve(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0)
