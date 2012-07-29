#!/usr/bin/env python

import tornado.ioloop
import tornado.web

import mongokit
import json

import egg.baskets.dbproxy as dbproxy
import egg.common.eggErrors as eggErrors
from egg.baskets.mongodb_model import Basket

    
class BasketHandler(tornado.web.RequestHandler):
    def initialize(self, dbp):
        self.dbp = dbp


class GetBasketsCreateBasketHandler(BasketHandler):
    def get(self, user_id):
        try:
            user_id = int(user_id)
            baskets = self.dbp.get_baskets(user_id)
            self.write( json.dumps( baskets ) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )

                
if __name__ == "__main__":
    con = mongokit.Connection('localhost', 27017)
    con.register([Basket])
    mongodb = con

    dbp = dbproxy.DbProxy( mongodb, None)

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/basket", GetBasketsCreateBasketHandler, dict(dbp=dbp)),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

