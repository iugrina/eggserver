#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.escape

import mongokit
import json

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
    con = mongokit.Connection('localhost', 27017)
    con.register([Recommended])
    mongodb = con

    dbp = models.recommended.recommended.Recommended( mongodb)

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/recommended", GetRecommendedHandler, dict(dbp=dbp)),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



