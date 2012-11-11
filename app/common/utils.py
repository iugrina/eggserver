import json
import datetime
from decimal import Decimal

from common import debugconstants

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


class ExceptionLogger():
    """Class that should be used as the superclass
    to enable some exception logging to file or standard output"""
    def __init__(self, logging_file_pointer=None) :
        self.lf = logging_file_pointer

    def log(self,  e, identifier=None):
        if not debugconstants.eggLogExceptions :
            return

        if self.lf :
            self.lf.write( identifier + ">>" + str(datetime.datetime.utcnow()) + " :: " + str(e) + "\n")
            self.lf.flush()
        else:
            print  identifier + ">>" +str(datetime.datetime.utcnow()) + " :: " + str(e)

def str2unicode(s, charset='utf-8'):
    """Converts str object to unicode object
       Useful with results from sqlalchemy/MySQL
    """
    if s != None :
        return unicode( s.decode(charset) )

