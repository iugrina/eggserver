import tornado.web
from models.auth.auth import Auth
from common import utils, egg_errors
from pprint import pprint as pp
from lib.voluptuous import voluptuous as val

class AuthBase(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db
    self.auth = Auth(self.db)

    self.params = {}
    for param in self.request.arguments:
      self.params[param] = self.request.arguments[param][0]

    return self.params

class LoginHandler(AuthBase):
  "API endpoint: /login/"
  
  def get(self):
    "Not currently defined (used for filtering)"
    pass

  def post(self):
    "Request user authorization"
    try:
      result = self.auth.login(self.params)
      if result:
        json = utils.jsonResult(result)
        self.write(json)
        if not self.get_secure_cookie("user"):
          self.set_secure_cookie("user", '1')
      else:
        self.write('error')
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())

