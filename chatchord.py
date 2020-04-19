from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from server import app, socketio

http_server = HTTPServer(
    WSGIContainer(
        socketio.run(app)
        # app.run(
        #     host = '0.0.0.0', 
        #     port = 3001,
        #     debug=False
        # )
    )
)
http_server.listen(3001)
IOLoop.instance().start()