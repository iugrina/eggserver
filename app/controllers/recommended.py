#!/usr/bin/env python

# tornado
import tornado.ioloop
import tornado.web
import tornado.escape

# other python
import mongokit
import json

# egg
import confegg
from common import utils, debugconstants, egg_errors

import models.recommended.recommended
from models.recommended.mongodb_model import Recommended

 
class BasketHandler(tornado.web.RequestHandler):
    def initialize(self, dbp):
        self.dbp = dbp

    def get_current_user(self):
        return self.get_secure_cookie("id")

    def prepare(self):
        if debugconstants.eggAuthenticate==True and not self.current_user :
            self.write( egg_errors.UnauthenticatedException().get_json() )
            self.finish()



class GetRecommendedHandler(BasketHandler):
    def get(self, user_id):
        user_id = int(user_id)

        # check privileges
        # only user can see it's recommended profiles
        if int(self.current_user) != user_id :
            self.write( egg_errors.PrivilegeException().get_json() )
            return

        try:
            recommended = self.dbp.get_recommended(user_id)
            self.write( json.dumps( recommended, ensure_ascii=False ) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

                
if __name__ == "__main__":
    conf = confegg.get_config()

    handlers = []



    conRec = mongokit.Connection(conf['mongo']['host'], conf['mongo']['port'])
    conRec.register([Recommended])

    recommended_dbp = models.recommended.recommended.Recommended( conRec)

    handlers.extend( [
        (r"/profile/([0-9]+)/recommended", GetRecommendedHandler, dict(dbp=recommended_dbp)),
        ])

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application( handlers, **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

