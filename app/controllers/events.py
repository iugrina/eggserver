import tornado.web
from models.events.event import Event
from common import utils
from pprint import pprint as pp

class EventBase(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db
    self.event = Event(self.db)

class EventsHandler(EventBase):
  def get(self):
    event_id = self.get_argument("event_id")
    result = self.event.get_event(event_id)
    json = utils.jsonResult(result)
    self.write(json)

  def post(self):
    params = {}
    for param in self.request.arguments:
      params[param] = self.request.arguments[param][0]
    self.write(utils.json.dumps(params))

class EventHandler(EventBase):
  pass

    #CURL test
    #curl -F "name=testiram" -F "description=ovo je description" -F "scheduled_for=2012-09-23T00:00:00" -F "expected_duration=17:00:00" -F "registration_deadline=2012-09-18T00:00:00" -F "location=Zagreb"  -F "hide_location=1" -F "registration_price=300" -F "creation_price=200" -F "is_active=1" -F "phase=before_event" localhost:8888/events/

    
