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
from common import utils, debugconstants, egg_errors, decorators

import models.recommended.recommended
from models.recommended.mongodb_model import Recommended

 
class RecommendedHandler(tornado.web.RequestHandler):
    def initialize(self, dbp):
        self.dbp = dbp

    def get_current_user(self):
        return self.get_secure_cookie("id")
  
    def set_default_headers(self):
        conf = confegg.get_config()
        self.set_header('Access-Control-Allow-Origin', conf['client_url'])
        self.set_header('Access-Control-Allow-Credentials', 'true')


class GetRecommendedHandler(RecommendedHandler):
    @decorators.authenticated
    def get(self, user_id, start_id, size):
        user_id = int(user_id)
        start_id = int(start_id)
        size = int(size)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see it's recommended
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            recommended = self.dbp.get_recommended(user_id, start_id, size)
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
        (r"/profile/([0-9]+)/recommended/([0-9]+)/([0-9]+)", GetRecommendedHandler, dict(dbp=recommended_dbp)),
        ])

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application( handlers, **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

