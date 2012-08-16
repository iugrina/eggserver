from lib.voluptuous import voluptuous as val
import datetime
import decimal

def validate_int(obj):
  schema = val.Schema(int, required=True)
  return schema(obj)

def validate_events(obj):
  schema = val.Schema({
      "name": val.all(str, val.length(max=255)),
      "description": val.all(str, val.length(max=2000)),
      "scheduled_for": datetime.datetime,
      "expected_duration": datetime.time,
      "registration_deadline": datetime.datetime,
      "location": val.all(str, val.length(max=255)),
      "hide_location": val.all(int, val.range(min=0, max=1)),
      "registration_price": decimal.Decimal,
      "creation_price": decimal.Decimal,
      "is_active": val.all(int, val.range(min=0, max=1)),
      "phase":  val.any("before_deadline", "before_event", "during_event", "after_event")
  })

  if "scheduled_for" in obj:
    obj["scheduled_for"] = datetime.datetime.strptime(obj["scheduled_for"], "%Y-%m-%dT%H:%M:%S")
  if "expected_duration" in obj:
    tmp = datetime.datetime.strptime(obj["expected_duration"], "%H:%M:%S")
    obj["expected_duration"] = datetime.time(tmp.hour, tmp.minute, tmp.second)
  if "registration_deadline" in obj:
    obj["registration_deadline"] = datetime.datetime.strptime(
      obj["registration_deadline"], "%Y-%m-%dT%H:%M:%S")
  if "hide_location" in obj:
    obj["hide_location"] = int(obj["hide_location"])
  if "registration_price" in obj:
    obj["registration_price"] = decimal.Decimal(obj["registration_price"])
  if "creation_price" in obj:
    obj["creation_price"] = decimal.Decimal(obj["creation_price"])
  if "is_active" in obj:
    obj["is_active"] = int(obj["is_active"])
  schema(obj)

def validate_event_participants(obj):
  schema = val.Schema({
      "event_id": val.all(int, val.length(max=20)),
      "user_id": val.all(int, val.length(max=20)),
      "participant_type": val.any("organizer", "guest", "other"),
      "attending": val.any("yes", "no", "maybe", "unaccepted", "undecided"),
      "other_participant_type": val.any("random", "guest_decision")
  })

  if "event_id" in obj:
    obj["event_id"] = int(obj("event_id"))
  if "user_id" in obj:
    obj["user_id"] = int(obj("user_id"))

  schema(obj)
