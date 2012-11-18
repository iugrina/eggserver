from mongokit import Document
import datetime

class StatusModel(Document):
    __database__ = "eggdb"
    __collection__ = "status"
    
    structure = {
        "user_id": int,
        "statuses": [ {
            "status_id": int,
            "status": unicode,
            "datetime": datetime.datetime,
        } ],
        "last_status_id": int,
        "last_status": unicode,
        "last_status_datetime": datetime.datetime,
    }

    required_fields = [ 'user_id' ]
    use_schemaless = True
