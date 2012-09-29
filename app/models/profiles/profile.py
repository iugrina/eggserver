import sqlalchemy
from common.mysqlTables import MySQLTables
from common import egg_errors
import schema as profile_schema


class Profile:
  def __init__(self, db):
    self.db = db
    self.table = sqlalchemy.Table("users", self.db.metadata, autoload=True)
    self.mysql_tables = MySQLTables(db)
  
  def get_user(self, user_id):
    "Returns user with user_id"
    result = self.mysql_tables.users.select(self.mysql_tables.users.c.user_id == user_id).execute()
    if result.rowcount == 1:
      return result
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
    result = self.mysql_tables.users.select((user.email == params['email']) & (user.password == sqlalchemy.func.password(params['password']))).execute()
    if result.rowcount == 1:
      return result
    else:
      return False
    raise egg_errors.QueryNotPossible