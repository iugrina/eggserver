from lib.voluptuous import voluptuous as val

def delete_event(obj):
  schema = val.Schema(int, required=True)
  return schema(obj)
