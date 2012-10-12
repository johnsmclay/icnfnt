import daemon
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from icnfnt import app

port = 5000

log = open('/var/log/tornado/tornado.' + str(port) + '.log', 'a+')
log_stream_descriptor = log.fileno()
ctx = daemon.DaemonContext(files_preserve=[log_stream_descriptor], gid=0, uid=0, stdout=log, stderr=log,  working_directory='.')
ctx.open()

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(port)

IOLoop.instance().start()
