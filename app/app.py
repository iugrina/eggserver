import tornado.ioloop
import tornado.web

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
    #self.db.echo = "debug"
    tornado.web.Application.__init__(self, handlers, **settings)




if __name__ == "__main__":
  app = Application()
  app.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()
