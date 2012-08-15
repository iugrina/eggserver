import json
from decimal import Decimal
import datetime

def parseRow(obj):
  if isinstance(obj, Decimal):
    return float(obj)
  if hasattr(obj, 'isoformat'):
    return obj.isoformat()
  return obj

def jsonRow(row):
  dic = {}
  i = 0
  for key in row.keys():
    dic[key] = parseRow(row[i])
    i += 1
  return dic

#convets sqlalchemy.ResultProxy to json
def jsonResult(result):
  jsonr = []

  for row in result.fetchall():
    dic = {}
    i = 0
    jsonr.append(jsonRow(row))
  return json.dumps(jsonr)
