import tornado.web
from models.events.event import Event
from common import utils, egg_errors
from pprint import pprint as pp
from lib.voluptuous import voluptuous as val

class EventBase(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db
    self.event = Event(self.db)

    self.params = {}
    for param in self.request.arguments:
      self.params[param] = self.request.arguments[param][0]

    return self.params

class EventsHandler(EventBase):
  "API endpoint: /event/"
  
  def get(self):
    "Not currently defined (used for filtering)"
    pass

  def post(self):
    "Creates a new event"
    try:
      self.event.add_event(self.params)
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())


    #CURL test
    #curl -X POST -F "name=testiram" -F "description=ovo je description" -F "scheduled_for=2012-09-23T00:00:00" -F "expected_duration=17:00:00" -F "registration_deadline=2012-09-18T00:00:00" -F "location=Zagreb"  -F "hide_location=1" -F "registration_price=300" -F "creation_price=200" -F "is_active=1" -F "phase=before_event" localhost:8888/event/

class EventHandler(EventBase):
  """Handles single event interaction
  API endpoint: /event/:id"""
  def get(self, event_id):
    "Retrieves event with event_id"
    try:
      result = self.event.get_event(int(event_id))
      json = utils.jsonResult(result)
      self.write(json)
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())

  def delete(self, event_id):
    "Removed event with event_id"
    try:
      self.event.delete_event(int(event_id))
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())


  def put(self, event_id):
    "Updates event information"
    self.event.update_event(event_id, self.params)


class EventUserHandler(EventBase):
  """Handles interaction between user and event
  API endpoint /event/:id/user/:id"""
  def post(self, event_id, user_id):
    try:
      self.event.add_event_user(event_id, user_id, self.params)
      self.write(utils.json.dumps(self.params))
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())

    #curl -X POST -F "participant_type=guest" -F "attending=yes" -F "other_participant_type=random" localhost:8888/event/10/user/2
  
  def delete(self, event_id, user_id):
    try:
      self.event.delete_event_user(event_id, user_id)
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())


  def put(self, event_id, user_id):
    try:
      self.event.update_event_user(event_id, user_id, self.params)
    #validation error
    except val.InvalidList as e:
      self.write(utils.json.dumps(str(e)))
    #query error
    except egg_errors.QueryNotPossible as e:
      self.write(e.get_json())

