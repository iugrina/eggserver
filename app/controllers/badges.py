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
from models.badges.badges import BadgesUsers, Badges

class BadgesHandler(tornado.web.RequestHandler):
    def initialize(self, badges ):
        self.b = badges

class GetBadgesHandler(BadgesHandler):
    def get(self):
        try:
            r = self.b.get_badges()
            self.write( json.dumps( r, ensure_ascii=False) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )

class GetBadgesTreeHandler(BadgesHandler):
    def get(self):
        try:
            r = self.b.get_badges_as_tree()
            self.write( json.dumps( r, ensure_ascii=False ) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )

    
class BadgesUsersHandler(tornado.web.RequestHandler):
    def initialize(self, badgesusers ):
        self.bu = badgesusers


class GetBadgesForUserHandler(BadgesUsersHandler):
    def get(self, user_id ):
        user_id = int(user_id)
        try:
            r = self.bu.get_user_badges(user_id)
            self.write( json.dumps( r, ensure_ascii=False ) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )

class AddChangeDeleteBadgesForUserHandler(BadgesUsersHandler):
    def post(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)
        try:
            body = tornado.escape.json_decode( self.request.body )
            # mora dobiti i nekakav description i visibility
            try:
                self.bu.addchange_user_badge(user_id, friend_id, body[0], body[1])
            except eggErrors.BaseException as e :
                self.write( e.get_json() )
        except ValueError:
            e = eggErrors.InvalidJSONException()
            self.write( e.get_json() )
    
    def delete(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)
        try:
            self.bu.delete_user_badge(user_id, friend_id)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )


if __name__ == "__main__":

    conf = confegg.get_config()
    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #self.db.echo = "debug"

    f = open(conf['log']['static_path']+"/badges.log", "wa")

    badgesusers = BadgesUsers(db, f)
    badges = Badges(db, f)

    application = tornado.web.Application([
        (r"/badges", GetBadgesHandler, dict(badges=badges)),
        (r"/badges/tree", GetBadgesTreeHandler, dict(badges=badges)),
        (r"/profile/([0-9]+)/badges", GetBadgesForUserHandler, dict(badgesusers=badgesusers)),
        (r"/profile/([0-9]+)/badges/([0-9]+)", AddChangeDeleteBadgesForUserHandler, dict(badgesusers=badgesusers)),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



