import json
from decimal import Decimal
import datetime

def parse(obj):
  if isinstance(obj, Decimal):
    return float(obj)
  if hasattr(obj, 'isoformat'):
    return obj.isoformat()
  return obj


#convets sqlalchemy.ResultProxy to json
def jsonify(result):
  jsonr = []

  for row in result.fetchall():
    dic = {}
    i = 0
    for key in row.keys():
      dic[key] = parse(row[i])
      i += 1
    jsonr.append(dic)
  return jsonr
