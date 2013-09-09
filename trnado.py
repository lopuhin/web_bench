#!/usr/bin/env python
import sys
import logging
logging.basicConfig(level=logging.WARN)
import transaction

import tornado.httpserver
import tornado.ioloop
import tornado.web

from utils import debug_exec, is_prime


class ServeHTTP(tornado.web.RequestHandler):
    def get(self, txt, num):
        for i in xrange(int(num)):
            self.write("%d: %s\n" % (i, txt))


class ServeHTTPPrimes(tornado.web.RequestHandler):
    def get(self, txt, num):
        for i in xrange(int(num)):
            if is_prime(i):
                self.write("%d: %s\n" % (i, txt))


class SimpleServeHTTP(tornado.web.RequestHandler):
    def get(self):
        self.write("hi!")


urls = [
    ("^/([^/]+)/([0-9]+)$", ServeHTTPPrimes)
    #("^/([^/]+)/([0-9]+)$", ServeHTTP)
    #("^/$", SimpleServeHTTP)
]
app = tornado.web.Application(urls)


if __name__ == "__main__":
    server = tornado.httpserver.HTTPServer(app)
    n_threads, port = map(int, sys.argv[1:3])
    transaction.set_num_threads(n_threads)
    server.listen(port)
    start = tornado.ioloop.IOLoop.instance().start
    if '--profile' in sys.argv:
        start = debug_exec(profile=True)(start)
    elif '--stat-profile' in sys.argv:
        start = debug_exec(stat_profile=True)(start)
    start()
