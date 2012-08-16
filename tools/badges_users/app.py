import os
import sys
import traceback
import json
import tornado.ioloop
import tornado.web
import tornado.database
from tornado import autoreload
import confegg

class ProtoHandler(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db

class MainHandler(ProtoHandler):
  def get(self):
    self.render("menu.html")
    
class ListBadgesHandler(ProtoHandler):
  def get(self):
    badges = self.db.query("select * from badges")
    self.render("badges.html", badges=badges, added_new=False, error=False)
    
class AddNewBadgeHandler(ProtoHandler):
  def post(self):
    try:
      name = self.get_argument("name")
      description = self.get_argument("description")
      parent = self.get_argument("parent")
      type = self.get_argument("type")
      
      if self.request.files:
        filename = self.request.files['image'][0]['filename']
        path = "./thumb/" + filename
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
          os.makedirs(directory)
        file = open(path, "w")
        file.write(self.request.files['image'][0]['body'])
        file.close()
        
        self.db.execute(
            "INSERT INTO badges (name, image_link, description, parent, type) "
            "VALUES (%s, %s, %s, %s, %s)",
            name, filename, description, parent, type)
        
        badges = self.db.query("select * from badges")
        self.render("badges.html", badges=badges, added_new=True, error=False)
      else:
        raise Exception
    except Exception:
      badges = self.db.query("select * from badges")
      self.render("badges.html", badges=badges, added_new=False, error=True)
      
class GetBadgeHandler(ProtoHandler):
  def get(self, bid):
    result = self.db.query("select * from badges where badge_id=%s", bid)
      
    self.write(json.dumps(result))
      
class DeleteBadgeHandler(ProtoHandler):
  def get(self, bid):
    try:
      result = self.db.query("select image_link from badges where badge_id=%s", bid)
      filename = result[0]['image_link']
      path = "./thumb/" + filename
      if os.path.isfile(path):
        os.remove(path)
        
      self.db.execute("delete from badges where badge_id=%s", bid)
      
    except Exception:
      badges = self.db.query("select * from badges")
      self.render("badges.html", badges=badges, added_new=False, error=True)

class GenerateTree(ProtoHandler):
  def genTreeRec( self, x, parent_ids, R ) :
    if x['badge_id'] not in parent_ids :
        return( {'node': x, 'children': None} )
    else :
        return( { 'node': x, 'children' : [ self.genTreeRec(x, parent_ids, R) for x in R[ x['badge_id'] ] ] } )

  def get(self):
    badges = self.db.query("select * from badges")

    R = dict()
    arg = 'parent'

    # creates dict with key=parent_id
    # value=list(all of the children of that parent)
    [ R.setdefault( x[arg], [] ).append(x) for x in badges ]

    parent_ids = R.keys()

    # root node always has id=0
    self.write( json.dumps( [ self.genTreeRec(x, parent_ids, R) for x in R[0]] ) )
    
class ListUsersHandler(ProtoHandler):
  def get(self):
    users = self.db.query("select * from users")
    self.render("users.html", users=users, added_new=False, error=False)
    
class AddNewUserHandler(ProtoHandler):
  def post(self):
    try:
      first_name = self.get_argument("first_name")
      last_name = self.get_argument("last_name")
      email = self.get_argument("email")
      
      if first_name and last_name and email:
        self.db.execute(
            "INSERT INTO users (first_name, last_name, email) "
            "VALUES (%s, %s, %s)",
            first_name, last_name, email)
        
        users = self.db.query("select * from users")
        self.render("users.html", users=users, added_new=True, error=False)
      else:
        raise Exception
    except Exception:
      users = self.db.query("select * from users")
      self.render("users.html", users=users, added_new=False, error=True)
      
class DeleteUserHandler(ProtoHandler):
  def get(self, uid):
    try:
      self.db.execute("delete from users where user_id=%s", uid)
      
    except Exception:
      users = self.db.query("select * from users")
      self.render("users.html", users=users, added_new=False, error=True)
      
class BadgesInUsersHandler(ProtoHandler):
  def get(self):
    users = self.db.query("select * from users")
    badges = self.db.query("select * from badges")
    badges_in_users = self.db.query("select * from badges_users")
    self.render("badges_in_users.html", badges_in_users=badges_in_users, users=users, badges=badges, updated=False, error=False)
    
  def post(self):
    # If somebody knows better solution - be my guest
    self.db.execute("delete from badges_users")
    for param in self.request.arguments:
      user_id = param[16:]
      for x in range(len(self.request.arguments[param])):
        badge_id = self.request.arguments[param][x]
        
        self.db.execute(
            "INSERT INTO badges_users (user_id, badge_id) "
            "VALUES (%s, %s)",
            user_id, badge_id)
    
    users = self.db.query("select * from users")
    badges = self.db.query("select * from badges")
    badges_in_users = self.db.query("select * from badges_users")
    self.render("badges_in_users.html", badges_in_users=badges_in_users, users=users, badges=badges, updated=True, error=False)

conf = confegg.get_config()
db = tornado.database.Connection(conf['mysql']['host'], conf['mysql']['database'], user=conf['mysql']['username'], password=conf['mysql']['password'])

settings = {
  "debug": True,
  "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
  (r"/", MainHandler, dict(db=db)),
  (r"/tree/get", GenerateTree, dict(db=db)),
  (r"/badges", ListBadgesHandler, dict(db=db)),
  (r"/badges/add", AddNewBadgeHandler, dict(db=db)),
  (r"/badges/get/([^/]+)", GetBadgeHandler, dict(db=db)),
  (r"/badges/delete/([^/]+)", DeleteBadgeHandler, dict(db=db)),
  (r"/users", ListUsersHandler, dict(db=db)),
  (r"/users/add", AddNewUserHandler, dict(db=db)),
  (r"/users/delete/([^/]+)", DeleteUserHandler, dict(db=db)),
  (r"/badges-in-users", BadgesInUsersHandler, dict(db=db)),
], **settings)

if __name__ == "__main__":
  application.listen(8880)
  ioloop = tornado.ioloop.IOLoop().instance()
  autoreload.start(ioloop)
  ioloop.start()
