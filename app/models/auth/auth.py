import sqlalchemy
from common.mysqlTables import MySQLTables
from common import egg_errors


class Auth:
  def __init__(self, db):
    "Takes sqlalchemy connector"
    self.db = db
    self.table = sqlalchemy.Table("users", self.db.metadata, autoload=True)
    self.mysqlTable = MySQLTables(db)

  def login(self, params):
    "Try to authorize user"
    user = self.mysqlTable.users.c
    result = self.mysqlTable.users.select((user.email == params['email']) & (user.password == sqlalchemy.func.password(params['password']))).execute()
    if result.rowcount == 1:
      return result
    else:
      return False
    raise egg_errors.QueryNotPossible