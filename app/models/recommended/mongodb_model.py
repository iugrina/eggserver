from mongokit import Document

import confegg

class Recommended(Document):
    __database__ = confegg.get_config()['mongo']['database']
    __collection__ = "recommended"
    
    structure = {
        "user_id": int,
        "recommended": [ {
            "user_id": int,
            "score": float,
        } ]
    }

    required_fields = [ 'user_id' ]
    use_schemaless = True
