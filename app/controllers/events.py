import tornado.web
from models.events.event import Event
from common import utils
from pprint import pprint as pp

class EventBase(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db
    self.event = Event(self.db)

  @property
  def params(self):
    params = {}
    for param in self.request.arguments:
      params[param] = self.request.arguments[param][0]

    return params

class EventsHandler(EventBase):
  
  def get(self):
    "Not currently defined (used for filtering)"
    pass

  def post(self):
    "Creates a new event"
    self.event.add_event(self.params)
    self.write(utils.json.dumps(self.params))


    #CURL test
    #curl -F "name=testiram" -F "description=ovo je description" -F "scheduled_for=2012-09-23T00:00:00" -F "expected_duration=17:00:00" -F "registration_deadline=2012-09-18T00:00:00" -F "location=Zagreb"  -F "hide_location=1" -F "registration_price=300" -F "creation_price=200" -F "is_active=1" -F "phase=before_event" localhost:8888/event/

class EventHandler(EventBase):
  def get(self, event_id):
    "Retrieves event with event_id"
    result = self.event.get_event(event_id)
    json = utils.jsonResult(result)
    self.write(json)

  def delete(self, event_id):
    "Removed event with event_id"
    self.event.delete_event(event_id)

  def put(self, event_id):
    "Updates event information"
    self.event.update_event(event_id, self.params)

