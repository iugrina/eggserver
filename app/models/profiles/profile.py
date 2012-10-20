import sqlalchemy
import bcrypt
import copy

import confegg
from common.mysqlTables import MySQLTables
from common import egg_errors
from common import utils
import schema as profile_schema

from models.images.images import ProfileImages
from models.friends.friends import Friends
from models.badges.badges import BadgesUsers

class Profile:
  def __init__(self, db):
    self.db = db
    self.table = sqlalchemy.Table("users", self.db.metadata, autoload=True)
    self.mysql_tables = MySQLTables(db)
  
  def get_user(self, user_id):
    "Returns user with user_id"
    result = self.mysql_tables.users.select(self.mysql_tables.users.c.user_id == user_id).execute()
    if result.rowcount == 1:
        return dict(result.fetchone().items())
    raise egg_errors.QueryNotPossible

  def add_user(self, params):
    "Creates a new user"
    profile_schema.validate_profiles(params)
    self.db.execute(self.mysql_tables.users.insert().values(params))

  def delete_user(self, user_id):
    "Deletes user with user_id"
    profile_schema.validate_int(user_id)
    if self.get_user(user_id).rowcount == 1:
      self.db.execute(self.mysql_tables.users.delete().where(self.mysql_tables.users.c.user_id == user_id))
    else:
      raise egg_errors.QueryNotPossible

  def update_user(self, user_id, params):
    "Updates user with user_id"
    profile_schema.validate_profiles(params)
    if self.get_user(user_id).rowcount == 1:
      self.db.execute(self.mysql_tables.users.update().where(self.mysql_tables.users.c.user_id == user_id)
                      .values(params))
    else:
      raise egg_errors.QueryNotPossible
    
  def login(self, params):
    "Try to authorize user"
    user = self.mysql_tables.users.c
    result = self.mysql_tables.users.select((user.username == params['username'])).execute()
    row = result.fetchone()

    if bcrypt.hashpw(params['password'], row.password) == row.password:
      return dict(row)
    else:
      return False
    raise egg_errors.QueryNotPossible
  
  def signup(self, params):
    "Sign up the user"
    profile_schema.validate_profiles(params)
    self.db.execute(self.mysql_tables.users.insert().values(params))



class ProfileData():
    def __init__(self, db):
        self.db = db
        self.p = Profile(self.db)
        self.i = ProfileImages(self.db)
        self.f = Friends(self.db)
        self.bu = BadgesUsers(self.db)

        conf = confegg.get_config()
        self.images_path = conf['env']['static_url_path'] + conf['images']['images_root']

    def get_user_info(self, user_id):
        """Returns this and that about user"""

        basic_user_info = self.p.get_user(user_id)

        # get profile_image/friend_image, badges, friends
        friends = self.f.get_friends(user_id)
        profile_image = self.i.get_image_path( self.i.get_user_images_by_type(user_id, 'profile')[0] )
        profile_image = self.images_path + profile_image
        badges = self.bu.get_user_badges(user_id)

        # ovo bi trebalo prilagoditi kad napravimo kod za activity/online/eggs status
        activity = True
        online = True
        eggs = 0

        #ovo bi trebalo prilagoditi kad napravimo kod za speech bubble
        speech_bubble = "evo " +  basic_user_info['first_name'] + " nesto prica"

        r = { "user_id": basic_user_info['user_id'], "first_name": basic_user_info['first_name'],
            "last_name": basic_user_info['last_name'], "nickname": basic_user_info['nickname'],
            "activity": activity, "online": online, "status": speech_bubble,
            "profile_image": profile_image,
            "friends": friends, "eggs": eggs,
            "badges": badges }

        return r

