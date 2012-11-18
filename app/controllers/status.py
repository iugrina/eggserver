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

import models.status.status
from models.status.mongodb_model import StatusModel

 
class StatusHandler(tornado.web.RequestHandler):
    def initialize(self, dbp):
        self.dbp = dbp

    def get_current_user(self):
        return self.get_secure_cookie("id")
  
    def set_default_headers(self):
        conf = confegg.get_config()
        self.set_header('Access-Control-Allow-Origin', conf['client_url'])
        self.set_header('Access-Control-Allow-Credentials', 'true')


class GetStatusesHandler(StatusHandler):
    @decorators.authenticated
    def get(self, user_id):
        user_id = int(user_id)

        # everyone can see user's statuses

        try:
            s = self.dbp.get_statuses(user_id)
            for x in s :
                x['datetime'] = unicode(x['datetime'])
            self.write( json.dumps( s, ensure_ascii=False ) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


class GetLastStatusHandler(StatusHandler):
    @decorators.authenticated
    def get(self, user_id):
        user_id = int(user_id)

        # everyone can see user's statuses

        try:
            s = self.dbp.get_last_status(user_id)
            print s
            s['datetime'] = unicode(s['datetime'])
            self.write( json.dumps( s, ensure_ascii=False ) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


class AddStatusHandler(StatusHandler):
    @decorators.authenticated
    def post(self, user_id): 
        user_id = int(user_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can add a status
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        status = self.get_argument("status")

        if not status:
            self.write("sranje")

        try:
            self.dbp.add_status(user_id, unicode(status))
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


class DeleteStatusHandler(StatusHandler):
    @decorators.authenticated
    def get(self, user_id, status_id): 
        user_id = int(user_id)
        status_id = int(status_id)

        if debugconstants.eggPrivileges :
            # check privileges
            # only user can delete it's status
            if int(self.current_user) != user_id :
                self.write( egg_errors.PrivilegeException().get_json() )
                return

        try:
            self.dbp.delete_status(user_id, status_id)
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


if __name__ == "__main__":
    conf = confegg.get_config()

    handlers = []

    conRec = mongokit.Connection(conf['mongo']['host'], conf['mongo']['port'])
    conRec.register([StatusModel])

    status_dbp = models.status.status.Status(conRec)

    handlers.extend([
        (r"/profile/([0-9]+)/status/all", GetStatusesHandler, dict(dbp=status_dbp)),
        (r"/profile/([0-9]+)/status/last", GetLastStatusHandler, dict(dbp=status_dbp)),
        (r"/profile/([0-9]+)/status/add", AddStatusHandler, dict(dbp=status_dbp)),
        (r"/profile/([0-9]+)/status/([0-9]+)/delete", DeleteStatusHandler, dict(dbp=status_dbp)),
        ])

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application( handlers, **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

