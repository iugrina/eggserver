import app
import utils
from decimal import Decimal
import datetime

egg = app.Application()
events = app.sqlalchemy.Table('events', egg.metadata, autoload=True)
print dir(events.insert)
#r = events.select().execute()
#print utils.jsonResult(r)


#users = app.sqlalchemy.Table('users', egg.metadata, autoload=True)
#print jsonify(users.select().execute())
