import sqlalchemy
from common.mysqlTables import MySQLTables
from common import egg_errors
import schema as EventSchema


class Event:
  def __init__(self, db):
    "Takes sqlalchemy connector"
    self.db = db
    self.table = sqlalchemy.Table("events", self.db.metadata, autoload=True)
    self.mysqlTable = MySQLTables(db)

  def get_event(self, event_id):
    "Returns event with event_id"
    result = self.mysqlTable.events.select(self.mysqlTable.events.c.event_id == event_id).execute()
    if result.rowcount == 1:
      return result
    raise egg_errors.QueryNotPossible

  def add_event(self, params):
    "Creates a new event"
    EventSchema.validate_events(params)
    self.db.execute(self.mysqlTable.events.insert().values(params))
    

  def delete_event(self, event_id):
    "Deletes event with event_id"
    EventSchema.validate_int(event_id)
    if self.get_event(event_id).rowcount == 1:
      self.db.execute(self.mysqlTable.events.delete().where(self.mysqlTable.events.c.event_id == event_id))
    else:
      raise egg_errors.QueryNotPossible

  def update_event(self, event_id, params):
    "Updates event with event_id"
    EventSchema.validate_events(params)
    if self.get_event(event_id).rowcount == 1:
      self.db.execute(self.mysqlTable.events.update().where(self.mysqlTable.events.c.event_id == event_id)
                      .values(params))
    else:
      raise egg_errors.QueryNotPossible

  def add_event_user(self, event_id, user_id, params):
    "Adds new user to event"
    params["event_id"] = event_id
    params["user_id"] = user_id
    EventSchema.validate_event_participants(params)
    self.db.execute(self.mysqlTable.event_participants.insert().values(params))

  def update_event_user(self, event_id, user_id, params):
    params["event_id"] = event_id
    params["user_id"] = user_id
    EventSchema.validate_event_participans(params)
    self.db.execute(self.mysqlTable.event_participants.update().where(
        self.mysqlTable.event_participants.c.event_id == event_id).where(
        self.mysqlTable.event_participants.c.user_id == user_id).values(params))

  def delete_event_user(self, event_id, user_id):
    "Removes user from event"
    self.db.execute(self.mysqlTable.event_participants.delete().where(
        self.mysqlTable.event_participants.c.event_id == int(event_id)).where(
        self.mysqlTable.event_participants.c.user_id == int(user_id)))

  def add_event_rating(self, event_id, rating):
    pass

  def update_event_rating(self, event_id, rating):
    pass

  def get_event_ragin(self, event_id):
    pass
