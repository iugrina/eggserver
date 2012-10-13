#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.escape

import json

import sqlalchemy
import controllers
from common import utils
import confegg
import common.egg_errors as eggErrors
from models.friends.friends import Friends

    
class FriendsHandler(tornado.web.RequestHandler):
    def initialize(self, friends ):
        self.friends = friends


class GetFriendsHandler(FriendsHandler):
    def get(self, user_id):
        user_id = int(user_id)
        try:
            fs = self.friends.get_friends(user_id)
            print fs
            self.write( json.dumps( list(fs) ) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )

class AddDeleteFriendHandler(FriendsHandler):
    def post(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)
        try:
            self.friends.add_friend(user_id, friend_id)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )
    
    def delete(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)
        try:
            self.friends.delete_friend(user_id, friend_id)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )


class ApproveFriendHandler(FriendsHandler):
    def post(self, user_id, friend_id): 
        try:
            self.friends.approve_friend(user_id, friend_id)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )



if __name__ == "__main__":

    conf = confegg.get_config()
    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #self.db.echo = "debug"

    friends = Friends(db)

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/friends", GetFriendsHandler, dict(friends=friends)),
        (r"/profile/([0-9]+)/friends/([0-9]+)", AddDeleteFriendHandler, dict(friends=friends)),
        (r"/profile/([0-9]+)/friends/approve/([0-9]+)", ApproveFriendHandler, dict(friends=friends)),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



