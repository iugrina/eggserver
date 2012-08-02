import tornado.web
from models.events.event import Event
from common import utils

class EventsHandler(tornado.web.RequestHandler):
  def initialize(self, db):
    self.db = db
    self.event = Event(self.db)

  def get(self):
    result = self.event.get_event(1)
    json = utils.jsonResult(result)
    self.write(json)

  def post(self):
    name = self.get_argument("name")
    description = self.get_argument("description")
    scheduled_for = self.get_argument("scheduled_for")
    expected_duration = self.get_argument("expected_duration")
    registration_deadline = self.get_argument("registration_deadline")
    location = self.get_argument("location")
    hide_location = self.get_argument("hide_location")
    registration_price = self.get_argument("registration_price")
    creation_price = self.get_argument("creation_price")
    is_active = self.get_argument("is_active")
    phase = self.get_argument("phase")

    
