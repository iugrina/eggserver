import json
import os

def get_config():
  config_file_location = os.path.join(os.path.dirname(__file__), 'app.json')
  with open(config_file_location) as config_file:
    config = json.loads(config_file.read())
    return config
