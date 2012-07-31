from common import eggErrors
from mongodb_model import Basket
import mongoconnector

class DbProxy:
    """DbProxy class is user as bridge between different DBs
    and the needs of client app. It defines several methods
    (interface) regarding Baskets"""

    def __init__(self, dbmongo, dbredis):
        """Takes connection objects to MongoDb and Redis"""
        self.dbmongo = dbmongo
        self.dbredis = dbredis

        self.mc = mongoconnector.MongoConnector(self.dbmongo)

    def __chooseDB(self) :
        # for now there is only MongoDB
        self.currentdb = self.dbmongo


    def get_baskets(self, user_id): 
        "Returns all baskets for user with user_id"
        self.__chooseDB()
        if self.currentdb == self.dbmongo :
            return self.mc.get_baskets(user_id)
        else :
            pass


    def change_order_of_baskets(self, user_id, new_order):
        "Changes the order of baskets for user with user_id"

        # this part should be done in mongodb and then
        # refreshed in redis (caching algorithm???)

        return self.mc.change_order_of_baskets( user_id, new_order )


    def add_basket(self, user_id, basket_name) :
        "Creates new basket with basket_name for user with user_id"

        # this part should be done in mongodb and then
        # refreshed in redis (caching algorithm???)

        self.mc.add_basket( user_id, basket_name )


    def get_basket(self, user_id, basket_id):
        "Returns basket with basket_id for with user_id"
        self.__chooseDB()
        if self.currentdb == self.dbmongo :
            return self.mc.get_basket(user_id, basket_id)
        else :
            pass


    def delete_basket(self, user_id, basket_id):
        """Removes basket with basket_id from user with user_id
        Deletion of the last basket is forbidden"""

        # this part should be done in mongodb and then
        # refreshed in redis (caching algorithm???)

        return self.mc.delete_basket( user_id, basket_id )


    def change_order_of_users_in_basket(self, user_id, basket_id, new_order):
        "Changes the order of users in basket with basket_id for user with user_id"

        # this part should be done in mongodb and then
        # refreshed in redis (caching algorithm???)

        return self.mc.change_order_of_users_in_basket( user_id, basket_id, new_order )


    def add_user_to_basket(self, user_id, basket_id, new_user_id):
        "Adds user with new_user_id to basket with basket_id for user with user_id"

        # this part should be done in mongodb and then
        # refreshed in redis (caching algorithm???)

        return self.mc.add_user_to_basket( user_id, basket_id, new_user_id )


    def delete_user_from_basket(self, user_id, basket_id, del_user_id):
        """Removes user with del_user_id from basket with basket_id
        for user with user_id."""

        # this part should be done in mongodb and then
        # refreshed in redis (caching algorithm???)

        return self.mc.delete_user_from_basket( user_id, basket_id, del_user_id )


