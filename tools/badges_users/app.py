import os
import sys
import traceback
import json
import tornado.ioloop
import tornado.web
import tornado.database
from tornado import autoreload

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

 
# user egg is more secure than user root
db = tornado.database.Connection("localhost", "eggdb", user="egg", password="")

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
  #(r"/users/add", AddNewUserHandler, dict(db=db)),
  #(r"/users/get/([^/]+)", GetUserHandler, dict(db=db)),
  #(r"/users/delete/([^/]+)", DeleteUserHandler, dict(db=db)),
], **settings)

if __name__ == "__main__":
  application.listen(8880)
  ioloop = tornado.ioloop.IOLoop().instance()
  autoreload.start(ioloop)
  ioloop.start()
