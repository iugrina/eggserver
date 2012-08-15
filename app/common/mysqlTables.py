import sqlalchemy

class MySQLTables:
  def __init__(self, db):
    self.db = db
    tables = [
      "events",
      "event_badges",
      "event_badges_events",
      "event_participants",
      "event_participant_badges",
      "event_photos"
      ]

    for _table in tables:
      setattr(self, _table, sqlalchemy.Table(_table, self.db.metadata, autoload=True))
