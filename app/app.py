import tornado.ioloop
import tornado.web

from tornado.options import options
import settings
import sqlalchemy
import controllers
from common import utils

class Application(tornado.web.Application):
  def __init__(self):
    self.db = sqlalchemy.create_engine(options.engine + "://" + options.user + ":" +
                                       options.password + "@" + options.host + "/" +
                                       options.database)
    self.db.metadata  = sqlalchemy.MetaData(bind=self.db)
    #self.db.echo = "debug"

    handlers = [
      (r"/event/", controllers.events.EventsHandler, dict(db=self.db)),
      (r"/event/([0-9]+)", controllers.events.EventHandler, dict(db=self.db)),
    ]

    settings = dict(
      debug=True,
    )

    tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
