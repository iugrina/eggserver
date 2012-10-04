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
      (r"/profile/([0-9]+)", controllers.profiles.ProfileHandler, dict(db=self.db)),
      (r"/profile/login/", controllers.profiles.LoginHandler, dict(db=self.db)),
      (r"/profile/signup/", controllers.profiles.SignupHandler, dict(db=self.db)),
    ]

    settings = dict(
      debug=True,
      cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    )

    tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
  app = Application()
  app.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
