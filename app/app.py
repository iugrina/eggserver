import tornado.ioloop
import tornado.web

from tornado.options import options
import sqlalchemy
import controllers
from common import utils
import confegg

class Application(tornado.web.Application):
  def __init__(self):
    conf = confegg.get_config()
    self.db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    self.db.metadata  = sqlalchemy.MetaData(bind=self.db)
    #self.db.echo = "debug"

    handlers = [
      (r"/event/", controllers.events.EventsHandler, dict(db=self.db)),
      (r"/event/([0-9]+)", controllers.events.EventHandler, dict(db=self.db)),
      (r"/event/([0-9]+)/user/([0-9]+)", controllers.events.EventUserHandler, dict(db=self.db)),
      (r"/profile/", controllers.profiles.ProfilesHandler, dict(db=self.db)),
    ]

    settings = dict(
      debug=True,
    )

    tornado.web.Application.__init__(self, handlers)


if __name__ == "__main__":
  app = Application()
  app.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
