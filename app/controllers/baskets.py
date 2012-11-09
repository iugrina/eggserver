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

import models.baskets.dbproxy as dbproxy
from models.baskets.mongodb_model import Basket

    
class BasketHandler(tornado.web.RequestHandler):
    def initialize(self, dbp):
        self.dbp = dbp

    def get_current_user(self):
        return self.get_secure_cookie("id")


class GetChangeOrderBasketsHandler(BasketHandler):
    @decorators.authenticated
    def get(self, user_id):
        user_id = int(user_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            baskets = self.dbp.get_baskets(user_id)
            self.write( json.dumps( baskets ) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

    @decorators.authenticated
    def post(self, user_id):
        user_id = int(user_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            new_order = tornado.escape.json_decode( self.request.body )
            try:
                baskets = self.dbp.change_order_of_baskets(user_id, new_order)
            except egg_errors.BaseException as e :
                self.write( e.get_json() )
        except ValueError:
            e = egg_errors.InvalidJSONException()
            self.write( e.get_json() )


class AddBasketHandler(BasketHandler):
    @decorators.authenticated
    def post(self, user_id): 
        user_id = int(user_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        basket_name = self.get_argument("basket_name")

        if not basket_name :
            self.write("sranje")

        try:
            self.dbp.add_basket(user_id, basket_name)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


class GetDelChangeOrderBasketHandler(BasketHandler):
    @decorators.authenticated
    def get(self, user_id, basket_id):
        user_id = int(user_id)
        basket_id = int(basket_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            basket = self.dbp.get_basket(user_id, basket_id)
            self.write( json.dumps( basket ) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

    @decorators.authenticated
    def delete(self, user_id, basket_id):
        user_id = int(user_id)
        basket_id = int(basket_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            basket = self.dbp.delete_basket(user_id, basket_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

    @decorators.authenticated
    def post(self, user_id, basket_id):
        user_id = int(user_id)
        basket_id = int(basket_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            new_order = tornado.escape.json_decode( self.request.body )
            try:
                baskets = self.dbp.change_order_of_users_in_basket(user_id, basket_id, new_order)
            except egg_errors.BaseException as e :
                self.write( e.get_json() )
        except ValueError:
            e = egg_errors.InvalidJSONException()
            self.write( e.get_json() )


class AddDelUserFromBasketHandler(BasketHandler):
    @decorators.authenticated
    def post(self, user_id, basket_id, add_user_id):
        user_id = int(user_id)
        basket_id = int(basket_id)
        add_user_id = int(add_user_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            basket = self.dbp.add_user_to_basket(user_id, basket_id, add_user_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

    @decorators.authenticated
    def delete(self, user_id, basket_id, add_user_id):
        user_id = int(user_id)
        basket_id = int(basket_id)
        del_user_id = int(add_user_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see/change it's baskets
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            basket = self.dbp.delete_user_from_basket(user_id, basket_id, del_user_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

                
if __name__ == "__main__":
    conf = confegg.get_config()

    con = mongokit.Connection(conf['mongo']['host'], conf['mongo']['port'])
    con.register([Basket])
    mongodb = con

    dbp = dbproxy.DbProxy( mongodb, None)

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/baskets", GetChangeOrderBasketsHandler, dict(dbp=dbp)),
        (r"/profile/([0-9]+)/basket", AddBasketHandler, dict(dbp=dbp)),
        (r"/profile/([0-9]+)/basket/([0-9]+)", GetDelChangeOrderBasketHandler, dict(dbp=dbp)),
        (r"/profile/([0-9]+)/basket/([0-9]+)/([0-9]+)", AddDelUserFromBasketHandler, dict(dbp=dbp)),
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

