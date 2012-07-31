import tornado.web

class BaseEventHandler(tornado.web.RequestHandler):
  @property
  def db(self):
    return self.application.db

  @property
  def metadata(self):
    return self.application.metadata


class EventsHandler(BaseHandler):
  @property
  def table(self):
    return sqlalchemy.Table("events", self.metadata, autoload=True)

  def get(self):
    r = self.table.select().execute()
    self.write(json.dumps(utils.jsonResult(r)))

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

    
