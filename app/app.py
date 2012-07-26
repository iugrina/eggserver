import tornado.ioloop
import tornado.web
from sqlalchemy import select

from tornado.options import options
import settings
import sqlalchemy
import json
import utils

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/events/", EventsHandler),
    ]

    settings = dict(
      debug=True,
    )

    self.db = sqlalchemy.create_engine(options.engine + "://" + options.user + ":" +
                                       options.password + "@" + options.host + "/" +
                                       options.database)
    self.metadata  = sqlalchemy.MetaData(bind=self.db)
    self.db.echo = "debug"
    tornado.web.Application.__init__(self, handlers, **settings)


class BaseHandler(tornado.web.RequestHandler):
  @property
  def db(self):
    return self.application.db

  @property
  def metadata(self):
    return self.application.metadata


class EventsHandler(BaseHandler):
  def get(self):
    users = sqlalchemy.Table("events", self.metadata, autoload=True)
    r = users.select().execute()
    self.write(json.dumps(utils.jsonify(r)))

if __name__ == "__main__":
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
