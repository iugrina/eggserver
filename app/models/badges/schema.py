from lib.voluptuous import voluptuous as val
import datetime
import decimal

def validate_int(obj):
  schema = val.Schema(int, required=True)
  return schema(obj)

def validate_profiles(obj):
  schema = val.Schema({
      "badge_id": int,
      "user_id": int,
      "description": val.all(str, val.length(max=1000)),
      "visibility": int,
  })
