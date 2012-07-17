import os
import sys
import traceback
import tornado.ioloop
import tornado.web
import tornado.database
from tornado import autoreload

class ProtoHandler(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db

class MainHandler(ProtoHandler):
  def get(self):
    badges = self.db.query("select * from badges")
    self.render("badges.html", badges=badges, added_new=False, error=False)
    
class AddNewHandler(ProtoHandler):
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
            "INSERT INTO badges (name, link, description, parent, type) "
            "VALUES (%s, %s, %s, %s, %s)",
            name, filename, description, parent, type)
        
        badges = self.db.query("select * from badges")
        self.render("badges.html", badges=badges, added_new=True, error=False)
      else:
        raise Exception
    except Exception:
      badges = self.db.query("select * from badges")
      self.render("badges.html", badges=badges, added_new=False, error=True)

db = tornado.database.Connection("localhost", "eggdb", user="root", password="root")

settings = {
  "debug": True,
  "static_path": os.path.join(os.path.dirname(__file__), "static"),
}

application = tornado.web.Application([
  (r"/", MainHandler, dict(db=db)),
  (r"/badges/add", AddNewHandler, dict(db=db)),
], **settings)

if __name__ == "__main__":
  application.listen(8880)
  ioloop = tornado.ioloop.IOLoop().instance()
  autoreload.start(ioloop)
  ioloop.start()
