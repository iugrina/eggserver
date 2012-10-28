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
from common import utils, debugconstants, egg_errors
import controllers
import controllers.blacklist
from models.blacklist.blacklist import Blacklist

class BlacklistHandler(tornado.web.RequestHandler):
    def initialize(self, blacklist2db, blacklist2dic=None ):
        self.b2db = blacklist2db
        self.b2dic = blacklist2dic

    def get_current_user(self):
        return self.get_secure_cookie("id")

    def prepare(self):
        if debugconstants.eggAuthenticate==True and not self.current_user :
            self.write( egg_errors.UnauthenticatedException().get_json() )
            self.finish()


class GetBlacklistHandler(BlacklistHandler):
    def get(self, user_id):
        user_id = int(user_id)

        # check privileges
        # only user can see/change it's blacklist
        if int(self.current_user) != user_id :
            self.write( egg_errors.PrivilegeException().get_json() )
            return

        self.write( json.dumps( self.b2dic.get(user_id, []), ensure_ascii=False ) )


class AddDeleteBlacklistedForUserHandler(BlacklistHandler):
    def post(self, user_id, blacklisted_id):
        user_id = int(user_id)

        # check privileges
        # only user can see/change it's blacklist
        if int(self.current_user) != user_id :
            self.write( egg_errors.PrivilegeException().get_json() )
            return

        blacklisted_id = int(blacklisted_id)
        try:
            self.b2db.add_to_blacklist(user_id, blacklisted_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )
            return
        self.b2dic.setdefault(user_id, []).append(blacklisted_id)
    
    def delete(self, user_id, blacklisted_id):
        user_id = int(user_id)

        # check privileges
        # only user can see/change it's blacklist
        if int(self.current_user) != user_id :
            self.write( egg_errors.PrivilegeException().get_json() )
            return

        blacklisted_id = int(blacklisted_id)
        try:
            self.b2db.delete_from_blacklist(user_id, blacklisted_id)
        except egg_errors.BaseException as e :
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

    handlers = []



    fblacklist = open(conf['log']['static_path']+conf['log']['blacklist'], "wa")

    blacklist2db = Blacklist(db, fblacklist)
    # radi brzine radimo s dict-om !!!
    blacklist2dic = blacklist2db.get_all_blacklisted_as_dict()

    handlers.extend([
        (r"/profile/([0-9]+)/blacklist", controllers.blacklist.GetBlacklistHandler, dict(blacklist2db=blacklist2db, blacklist2dic=blacklist2dic)),
        (r"/profile/([0-9]+)/blacklist/([0-9]+)", controllers.blacklist.AddDeleteBlacklistedForUserHandler, dict(blacklist2db=blacklist2db, blacklist2dic=blacklist2dic)),
        ])

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application( handlers, **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

