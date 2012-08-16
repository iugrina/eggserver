import sqlalchemy
from common.mysqlTables import MySQLTables
from common import egg_errors
import schema as profile_schema

class Profile:
  def __init__(self, db):
    self.db = db
    self.table = sqlalchemy.Table("users", self.db.metadata, autoload=True)
    self.mysql_tables = MySQLTables(db)

  def add_user(self, params):
    """ TODO """
    profile_schema.validate(params)
    self.db.execute(self.table.insert().values(params))
