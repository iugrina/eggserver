import sqlalchemy

class Event:
  
  def __init__(self, db):
    "Takes sqlalchemy connector"
    self.db = db
    self.table = sqlalchemy.Table("events", db.metadata, autoload=True)

  def get_event(self, event_id):
    "Returns event with event_id"
    return self.table.select(self.table.c.event_id=int(event_id)).execute()

  def add_event(self):
    

  def delete_event(self, event_id):
    pass

  def update_event(self, event_id):
    pass

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
