#!/usr/bin/env python3

"""Slow HTTP server class.

This module implements a ThreadingHTTPServer using a custom
SimpleHTTPRequestHandler subclass that introduces delays to all
GET responses, and optionally returns errors to a fraction of
the requests if given the --error_rate command-line argument.
"""

import contextlib
import os
import socket
import time
from functools import partial
from http import server, HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from random import random, uniform

MIN_DELAY = 0.5  # minimum delay for do_GET (seconds)
MAX_DELAY = 5.0  # maximum delay for do_GET (seconds)

class SlowHTTPRequestHandler(SimpleHTTPRequestHandler):
    """SlowHTTPRequestHandler adds delays and errors to test HTTP clients.

    The optional error_rate argument determines how often GET requests
    receive a 418 status code, "I'm a teapot".
    If error_rate is .15, there's a 15% probability of each GET request
    getting that error.
    When the server believes it is a teapot, it refuses requests to serve files.

    See: https://tools.ietf.org/html/rfc2324#section-2.3.2
    """

    def __init__(self, *args, error_rate=0.0, **kwargs):
        self.error_rate = error_rate
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Serve a GET request."""
        delay = uniform(MIN_DELAY, MAX_DELAY)
        cc = self.path[-6:-4].upper()
        print(f'{cc} delay: {delay:0.2}s')
        time.sleep(delay)
        if random() < self.error_rate:
            # HTTPStatus.IM_A_TEAPOT requires Python >= 3.9
            try:
                self.send_error(HTTPStatus.IM_A_TEAPOT, "I'm a Teapot")
            except BrokenPipeError as exc:
                print(f'{cc} *** BrokenPipeError: client closed')
        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                except BrokenPipeError as exc:
                    print(f'{cc} *** BrokenPipeError: client closed')
                finally:
                    f.close()

# The code in the `if` block below, including comments, was copied
# and adapted from the `http.server` module of Python 3.9
# https://github.com/python/cpython/blob/master/Lib/http/server.py

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--bind', '-b', metavar='ADDRESS',
                        help='Specify alternate bind address '
                             '[default: all interfaces]')
    parser.add_argument('--directory', '-d', default=os.getcwd(),
                        help='Specify alternative directory '
                             '[default:current directory]')
    parser.add_argument('--error-rate', '-e', metavar='PROBABILITY',
                        default=0.0, type=float,
                        help='Error rate; e.g. use .25 for 25%% probability '
                             '[default:0.0]')
    parser.add_argument('port', action='store',
                        default=8001, type=int,
                        nargs='?',
                        help='Specify alternate port [default: 8001]')
    args = parser.parse_args()
    handler_class = partial(SlowHTTPRequestHandler,
                            directory=args.directory,
                            error_rate=args.error_rate)

    # ensure dual-stack is not disabled; ref #38907
    class DualStackServer(ThreadingHTTPServer):
        def server_bind(self):
            # suppress exception when protocol is IPv4
            with contextlib.suppress(Exception):
                self.socket.setsockopt(
                    socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            return super().server_bind()

    # test is a top-level function in http.server omitted from __all__
    server.test(  # type: ignore
        HandlerClass=handler_class,
        ServerClass=DualStackServer,
        port=args.port,
        bind=args.bind,
    )
