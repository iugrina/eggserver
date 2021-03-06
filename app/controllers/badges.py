#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.escape

import json

import sqlalchemy
import controllers
from common import utils, debugconstants, egg_errors, decorators
import confegg
import models.badges.badges
from models.badges.badges import BadgesUsers, Badges

class BadgesHandler(tornado.web.RequestHandler):
    def initialize(self, badges, badgeslist, badgestree ):
        self.b = badges
        self.blist = badgeslist
        self.btree = badgestree

    def get_current_user(self):
        return self.get_secure_cookie("id")

    def set_default_headers(self):
        conf = confegg.get_config()
        self.set_header('Access-Control-Allow-Origin', conf['client_url'])
        self.set_header('Access-Control-Allow-Credentials', 'true')

class GetBadgesHandler(BadgesHandler):
    @decorators.authenticated
    def get(self):
        self.write( json.dumps( self.blist, ensure_ascii=False ) )
#        try:
#            r = self.b.get_badges()
#            self.write( json.dumps( r, ensure_ascii=False) )
#        except egg_errors.BaseException as e :
#            self.write( e.get_json() )


class GetBadgesTreeHandler(BadgesHandler):
    @decorators.authenticated
    def get(self):
        self.write( json.dumps( self.btree, ensure_ascii=False ) )
#        try:
#            r = self.b.get_badges_as_tree()
#            self.write( json.dumps( r, ensure_ascii=False ) )
#        except egg_errors.BaseException as e :
#            self.write( e.get_json() )


class BadgesUsersHandler(tornado.web.RequestHandler):
    def initialize(self, badgesusers ):
        self.bu = badgesusers

    def get_current_user(self):
        return self.get_secure_cookie("id")


class GetBadgesForUserHandler(BadgesUsersHandler):
    @decorators.authenticated
    def get(self, user_id ):
        user_id = int(user_id)

        # check privileges
        if debugconstants.eggPrivileges :
            # only user can see all of his badges
            if int(self.current_user) == user_id :
                getbadges = lambda x : self.bu.get_user_badges(x)
            else:
                getbadges = lambda x : self.bu.get_user_badges_by_visibility(user_id, visibility=0)
        # if we do not care about user priviledges (DEBUG MODE)
        else:
          getbadges = lambda x : self.bu.get_user_badges(x)

        try:
            r = getbadges(user_id)
            self.write( json.dumps( r, ensure_ascii=False ) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

class AddChangeDeleteBadgesForUserHandler(BadgesUsersHandler):
    @decorators.authenticated
    def post(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can change it's badges
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            body = tornado.escape.json_decode( self.request.body )
            # mora dobiti i nekakav description i visibility
            try:
                self.bu.addchange_user_badge(user_id, friend_id, body[0], body[1])
            except egg_errors.BaseException as e :
                self.write( e.get_json() )
        except ValueError:
            e = egg_errors.InvalidJSONException()
            self.write( e.get_json() )

    @decorators.authenticated
    def delete(self, user_id, friend_id):
        user_id = int(user_id)
        friend_id = int(friend_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can change it's badges
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            self.bu.delete_user_badge(user_id, friend_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


if __name__ == "__main__":

    conf = confegg.get_config()
    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #self.db.echo = "debug"

    images_path = conf['env']['static_url_path'] + conf['images']['images_root']
    badges_path = images_path + conf['images']['badges']

    logging_file = open(conf['log'][
                        'static_path'] + conf['log']['master'], "wa")

    badges_path = images_path + conf['images']['badges']

    badgesusers = models.badges.badges.BadgesUsers(db, logging_file)
    badges = Badges(db, logging_file=logging_file, images_path=badges_path)

    # koristit cemo vec gotovu listu i dict jer ce se bedzevi
    # uredjivati sa zasebnim alatom u "maintenance mode"-u
    badgeslist = badges.get_badges()
    badgestree = badges.get_badges_as_tree()

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application([
        (r"/badges", GetBadgesHandler, dict(badges=badges, badgeslist=badgeslist, badgestree=badgestree)),
        (r"/badges/tree", GetBadgesTreeHandler, dict(badges=badges, badgeslist=badgeslist, badgestree=badgestree)),
        (r"/profile/([0-9]+)/badges", GetBadgesForUserHandler, dict(badgesusers=badgesusers)),
        (r"/profile/([0-9]+)/badges/([0-9]+)", AddChangeDeleteBadgesForUserHandler, dict(badgesusers=badgesusers)),
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()



