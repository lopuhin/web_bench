#!/usr/bin/env python
import sys
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
    server.listen(int(sys.argv[1]))
    start = tornado.ioloop.IOLoop.instance().start
    if '--profile' in sys.argv[2:]:
        start = debug_exec(stat_profile=True)(start)
    start()
