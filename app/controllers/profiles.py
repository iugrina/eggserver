# tornado
import tornado.web

# other python
import json
import sqlalchemy
import mongokit
from lib.voluptuous import voluptuous as val

# egg
import confegg
from common import utils, egg_errors, debugconstants, decorators

import controllers
import controllers.profiles

from models.profiles.profile import Profile, ProfileData
from models.status.mongodb_model import StatusModel


class ProfileBase(tornado.web.RequestHandler):
    def initialize(self, db):
        self.db = db
        self.profile = Profile(self.db)

        self.params = {}
        for param in self.request.arguments:
            self.params[param] = self.request.arguments[param][0]

        # cem' ovo ???
        return self.params

    def set_default_headers(self):
        conf = confegg.get_config()
        self.set_header('Access-Control-Allow-Origin', conf['client_url'])
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def get_current_user(self):
        return self.get_secure_cookie("id")


class ProfilesHandler(ProfileBase):
    """
    API endpoint: /profile/
    """

    def get(self):
        pass

    def post(self):
        "Creates a new profile"
        try:
            self.profile.add_user(self.params)
        #validation error
        except val.InvalidList as e:
            self.write(utils.json.dumps(str(e)))
        #query error
        except egg_errors.QueryNotPossible as e:
            self.write(e.get_json())


class ProfileHandler(ProfileBase):
    """Handles single profile interaction
    API endpoint: /profile/:id"""

    def initialize(self, db, profiledata):
        super(ProfileHandler, self).initialize(db)
        self.profiledata = profiledata

    @decorators.authenticated
    def get(self, user_id):
        "Retrieves profile with user_id"
        user_id = int(user_id)

        try:
            result = self.profiledata.get_user_info(user_id)
            self.write( json.dumps(result, ensure_ascii=False) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

    @decorators.authenticated
    def delete(self, user_id):
        "Removed profile with user_id"
        try:
            self.profile.delete_user(int(user_id))
        #validation error
        except val.InvalidList as e:
            self.write(utils.json.dumps(str(e)))
        #query error
        except egg_errors.QueryNotPossible as e:
            self.write(e.get_json())

    def put(self, user_id):
        "Updates profile information"
        self.profile.update_user(user_id, self.params)


class LoginHandler(ProfileBase):
    """Handles single profile interaction
    API endpoint: /profile/login/"""

    def get(self):
        "Not currently defined (used for filtering)"
        pass

    def post(self):
        "Request user profile authorization"
        try:
            result = self.profile.login(self.params)
            if result:
                self.write(json.dumps(result, ensure_ascii=False))
                if not self.get_secure_cookie("user"):
                    self.set_secure_cookie("user", self.params["username"], 
                                           expires_days=debugconstants.cookie_max_days)
                if not self.get_secure_cookie("id"):
                    self.set_secure_cookie("id", str(result["user_id"]),
                                           expires_days=debugconstants.cookie_max_days)
                if not self.get_cookie("id2"):
                    self.set_cookie("id2", str(result["user_id"]),
                                    expires_days=debugconstants.cookie_max_days)
            else:
                self.write(utils.json.dumps({ 'error': 'unknown user' }))
        #validation error
        except val.InvalidList as e:
            self.write(utils.json.dumps(str(e)))
        #query error
        except egg_errors.QueryNotPossible as e:
            self.write(e.get_json())
        except KeyError as e:
            self.write(utils.json.dumps({ 'error': 'no data' }))


class SignupHandler(ProfileBase):
    """API endpoint: /profile/signup/"""

    def get(self):
        "Not currently defined (used for filtering)"
        pass

    def post(self):
        "Create user and set cookie"
        try:
            self.profile.signup(self.params)
            self.set_secure_cookie("user", self.params["email"])
        #validation error
        except val.InvalidList as e:
            self.write(utils.json.dumps(str(e)))
        #query error
        except egg_errors.QueryNotPossible as e:
            self.write(e.get_json())


if __name__ == "__main__":
    conf = confegg.get_config()
    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #db.echo = "debug"

    conMongo = mongokit.Connection(conf['mongo']['host'], conf['mongo']['port'])
    conMongo.register([StatusModel])

    f = open(conf['log']['static_path']+conf['log']['master'], "wa")
    profiledata = ProfileData( db, conMongo, f )

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    app = tornado.web.Application([
      (r"/profile/", controllers.profiles.ProfilesHandler, dict(db=db)),
      (r"/profile/([0-9]+)", controllers.profiles.ProfileHandler, dict(db=db, profiledata=profiledata)),
      (r"/profile/login/", controllers.profiles.LoginHandler, dict(db=db)),
      (r"/profile/signup/", controllers.profiles.SignupHandler, dict(db=db)),
    ], **settings)

    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
