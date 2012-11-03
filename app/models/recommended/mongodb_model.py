from mongokit import Document

class Recommended(Document):
    __database__ = "eggdb"
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
