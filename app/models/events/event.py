import sqlalchemy
from common.mysqlTables import MySQLTables

class Event:
  def __init__(self, db):
    "Takes sqlalchemy connector"
    self.db = db
    self.table = sqlalchemy.Table("events", self.db.metadata, autoload=True)
    self.mysqlTable = MySQLTables(db)

  def get_event(self, event_id):
    "Returns event with event_id"
    return self.mysqlTable.events.select(self.mysqlTable.events.c.event_id == event_id).execute()

  def add_event(self, params):
    "Creates a new event"
    self.db.execute(self.mysqlTable.events.insert().values(params))

  def delete_event(self, event_id):
    "Deletes event with event_id"
    self.db.execute(self.mysqlTable.events.delete().where(self.mysqlTable.events.c.event_id == event_id))

  def update_event(self, event_id, params):
    "Updates event with event_id"
    self.db.execute(self.mysqlTable.events.update().where(self.mysqlTable.events.c.event_id == event_id)
                    .values(params))

  def update_event_user(self, event_id, user_id):
    pass

  def delete_user_from_event(self, event_id, user_id):
    pass

  def add_event_rating(self, event_id, rating):
    pass

  def update_event_rating(self, event_id, rating):
    pass

  def get_event_ragin(self, event_id):
    pass
