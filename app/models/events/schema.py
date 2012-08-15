from lib.voluptuous import voluptuous as val

def get_event(obj):
  schema = val.Schema(int, required=True)
  return schema(obj)

def delete_event(obj):
  schema = val.Schema(int, required=True)
  return schema(obj)
