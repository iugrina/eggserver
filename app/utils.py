#convets sqlalchemy.ResultProxy to array
def jsonify(result):
  json = []
  for row in result:
    row = row.items()
    dic = {}
    for item in row:
      dic[item[0]] = item[1]

    json.append(dic)
  return json
    
