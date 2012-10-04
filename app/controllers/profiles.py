import tornado.web
from models.profiles.profile import Profile
from common import utils, egg_errors
from lib.voluptuous import voluptuous as val

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