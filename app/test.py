import app
from utils import jsonify
from decimal import Decimal
import datetime

egg = app.Application()
events = app.sqlalchemy.Table('events', egg.metadata, autoload=True)
r = events.select().execute()
print jsonify(r)


#users = app.sqlalchemy.Table('users', egg.metadata, autoload=True)
#print jsonify(users.select().execute())
