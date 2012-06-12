import os
import tornado.ioloop
import tornado.web
import tornado.database
from tornado import autoreload

class ProtoHandler(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db

class MainHandler(ProtoHandler):
  def get(self):
    badges = self.db.query("select * from badges")
    self.render("badges.html", badges=badges)

db = tornado.database.Connection("localhost", "eggdb", user="egg", password="egg")

settings = {
  "debug": True,
  "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
  (r"/", MainHandler, dict(db=db)),
], **settings)

if __name__ == "__main__":
  application.listen(8880)
  ioloop = tornado.ioloop.IOLoop().instance()
  autoreload.start(ioloop)
  ioloop.start()
