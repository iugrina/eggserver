from lib.voluptuous import voluptuous as val
import datetime
import decimal

def validate_int(obj):
  schema = val.Schema(int, required=True)
  return schema(obj)

def validate_profiles(obj):
  schema = val.Schema({
      "first_name": val.all(str, val.length(max=255)),
      "last_name": val.all(str, val.length(max=255)),
      "email": val.all(str, val.length(max=255)),
      "password": val.all(str, val.length(max=255)),
  })