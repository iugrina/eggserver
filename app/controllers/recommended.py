#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.escape

import mongokit
import json

import confegg

import models.recommended.recommended
import common.egg_errors as eggErrors
from models.recommended.mongodb_model import Recommended

 
class BasketHandler(tornado.web.RequestHandler):
    def initialize(self, dbp):
        self.dbp = dbp


class GetRecommendedHandler(BasketHandler):
    def get(self, user_id):
        user_id = int(user_id)
        try:
            recommended = self.dbp.get_recommended(user_id)
            self.write( json.dumps( recommended, ensure_ascii=False ) )
        except eggErrors.BaseException as e :
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
      debug=True,
      cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    )

    application = tornado.web.Application( handlers, **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



