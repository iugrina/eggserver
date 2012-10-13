import tornado.web
from models.profiles.profile import Profile
from common import utils, egg_errors
from lib.voluptuous import voluptuous as val
import confegg
import sqlalchemy
import bcrypt
import controllers

class ProfileBase(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db
    self.profile = Profile(self.db)
    
    self.params = {}
    for param in self.request.arguments:
      self.params[param] = self.request.arguments[param][0]
      
    return self.params
  
  
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
  def get(self, user_id):
    "Retrieves profile with user_id"
    try:
      result = self.profile.get_user(int(user_id))
      json = utils.jsonResult(result)
      self.write(json)
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())
      
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
        json = utils.jsonResult(result)
        self.write(json)
        if not self.get_secure_cookie("user"):
          self.set_secure_cookie("user", self.params["email"])
      else:
        self.write('error')
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())
      
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

    app = tornado.web.Application([
      (r"/profile/", controllers.profiles.ProfilesHandler, dict(db=db)),
      (r"/profile/([0-9]+)", controllers.profiles.ProfileHandler, dict(db=db)),
      (r"/profile/login/", controllers.profiles.LoginHandler, dict(db=db)),
      (r"/profile/signup/", controllers.profiles.SignupHandler, dict(db=db)),
    ])

    settings = dict(
      debug=True,
      cookie_secret="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    )

    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

