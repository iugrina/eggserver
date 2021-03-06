#!/usr/bin/env python

# tornado
import tornado.ioloop
import tornado.web
import tornado.escape

# other python
import json
import sqlalchemy

# egg
import confegg
from common import utils, debugconstants, egg_errors, decorators

import controllers
from models.friends.friends import Friends

    
class FriendsHandler(tornado.web.RequestHandler):
    def initialize(self, friends ):
        self.friends = friends

    def get_current_user(self):
        return self.get_secure_cookie("id")

    def set_default_headers(self):
        conf = confegg.get_config()
        self.set_header('Access-Control-Allow-Origin', conf['client_url'])
        self.set_header('Access-Control-Allow-Credentials', 'true')

class GetFriendsHandler(FriendsHandler):
    @decorators.authenticated
    def get(self, user_id):
        user_id = int(user_id)

        # everyone can see user's friends

        try:
            fs = self.friends.get_friends(user_id)
            self.write( json.dumps( fs ) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


class AddDeleteFriendHandler(FriendsHandler):
    @decorators.authenticated
    def post(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see change it's friends
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            self.friends.add_friend(user_id, friend_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )
    
    @decorators.authenticated
    def delete(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see change it's friends
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            self.friends.delete_friend(user_id, friend_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


class ApproveFriendHandler(FriendsHandler):
    @decorators.authenticated
    def post(self, user_id, friend_id): 

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can see change it's friends
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            self.friends.approve_friend(user_id, friend_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )



if __name__ == "__main__":

    conf = confegg.get_config()
    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #self.db.echo = "debug"

    f = open(conf['log']['static_path']+conf['log']['friends'], "wa")
    friends = Friends(db, f)

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/friends", GetFriendsHandler, dict(friends=friends)),
        (r"/profile/([0-9]+)/friends/([0-9]+)", AddDeleteFriendHandler, dict(friends=friends)),
        (r"/profile/([0-9]+)/friends/approve/([0-9]+)", ApproveFriendHandler, dict(friends=friends)),
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

