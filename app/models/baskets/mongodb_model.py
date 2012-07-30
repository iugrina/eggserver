from mongokit import Document

class Basket(Document):
    __database__ = "eggdb"
    __collection__ = "baskets"
    
    structure = {
        "user_id": int,
        "baskets": [ {
            "basket_id": int,
            "basket_name": unicode,
            "basket_order_id": int,
            "users": [ {
                "user_id" : int,
                "user_order_id" : int,
            } ],
        } ]
    }


    required_fields = [ 'user_id' ]
    use_schemaless = True

