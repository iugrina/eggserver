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
from models.blacklist.blacklist import Blacklist

class BlacklistHandler(tornado.web.RequestHandler):
    def initialize(self, blacklist2db, blacklist2dic=None ):
        self.b2db = blacklist2db
        self.b2dic = blacklist2dic

class GetBlacklistHandler(BlacklistHandler):
    def get(self, user_id):
        user_id = int(user_id)
        self.write( json.dumps( self.b2dic[user_id], ensure_ascii=False ) )

class AddDeleteBlacklistedForUserHandler(BlacklistHandler):
    def post(self, user_id, blacklisted_id):
        user_id = int(user_id)
        blacklisted_id = int(blacklisted_id)
        try:
            self.b2db.add_to_blacklist(user_id, blacklisted_id)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )
            return
        self.b2dic[user_id].append(blacklisted_id)
    
    def delete(self, user_id, blacklisted_id):
        user_id = int(user_id)
        blacklisted_id = int(blacklisted_id)
        try:
            self.b2db.delete_from_blacklist(user_id, blacklisted_id)
        except eggErrors.BaseException as e :
            self.write( e.get_json() )
            return
        self.b2dic[user_id].remove(blacklisted_id)


if __name__ == "__main__":

    conf = confegg.get_config()
    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
        conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
        conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #self.db.echo = "debug"

    f = open(conf['log']['static_path']+conf['log']['blacklist'], "wa")

    blacklist2db = Blacklist(db, f)
    # radi brzine radimo s dict-om !!!
    blacklist2dic = blacklist2db.get_all_blacklisted_as_dict()

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/blacklist", GetBlacklistHandler, dict(blacklist2db=blacklist2db, blacklist2dic=blacklist2dic)),
        (r"/profile/([0-9]+)/blacklist/([0-9]+)", AddDeleteBlacklistedForUserHandler, dict(blacklist2db=blacklist2db, blacklist2dic=blacklist2dic)),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
