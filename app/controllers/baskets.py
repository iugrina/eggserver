#!/usr/bin/env python

import tornado.ioloop
import tornado.web

import mongokit
import json

import models.baskets.dbproxy as dbproxy
import common.eggErrors as eggErrors
from models.baskets.mongodb_model import Basket

    
class BasketHandler(tornado.web.RequestHandler):
    def initialize(self, dbp):
        self.dbp = dbp


class GetChangeOrderBasketsHandler(BasketHandler):
    def get(self, user_id):
        user_id = int(user_id)
        try:
            baskets = self.dbp.get_baskets(user_id)
            self.write( json.dumps( baskets ) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )

class AddBasketHandler(BasketHandler):
    def post(self, user_id): 
        basket_name = self.get_argument("basket_name")

        if not basket_name :
            self.write("sranje")

        user_id = int(user_id)

        try:
            self.dbp.add_basket(user_id, basket_name)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )


class GetDelChangeOrderBasketHandler(BasketHandler):
    def get(self, user_id, basket_id):
        user_id = int(user_id)
        basket_id = int(basket_id)
        try:
            basket = self.dbp.get_basket(user_id, basket_id)
            self.write( json.dumps( basket ) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )


class AddDelUserFromBasketHandler(BasketHandler):
    def post(self, user_id, basket_id, add_user_id):
        user_id = int(user_id)
        basket_id = int(basket_id)
        add_user_id = int(add_user_id)
        try:
            basket = self.dbp.add_user_to_basket(user_id, basket_id, add_user_id)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )


                
if __name__ == "__main__":
    con = mongokit.Connection('localhost', 27017)
    con.register([Basket])
    mongodb = con

    dbp = dbproxy.DbProxy( mongodb, None)

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/baskets", GetChangeOrderBasketsHandler, dict(dbp=dbp)),
        (r"/profile/([0-9]+)/basket", AddBasketHandler, dict(dbp=dbp)),
        (r"/profile/([0-9]+)/basket/([0-9]+)", GetDelChangeOrderBasketHandler, dict(dbp=dbp)),
        (r"/profile/([0-9]+)/basket/([0-9]+)/([0-9]+)", AddDelUserFromBasketHandler, dict(dbp=dbp)),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



