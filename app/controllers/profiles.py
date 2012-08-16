import tornado.web
from models.profiles.profile import Profile
from common import utils, egg_errors
from lib.voluptuous import voluptuous as val

class ProfileBase(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db
    self.profile = Profile(self.db)

  def params(self):
    "returns params dictionary"
    params = {}
    for param in self.request.arguments:
      params[param] = self.request.arguments[param]

    return params

class ProfilesHandler(ProfileBase):
  """
  API endpoint: /profile/
  """

  def get(self):
    pass

  def post(self):
    try:
      self.profile.add_user(self.params())
    except:
      pass
