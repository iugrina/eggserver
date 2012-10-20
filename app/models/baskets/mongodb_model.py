from mongokit import Document
import confegg

class Basket(Document):
    __database__ = confegg.get_config()['mongo']['database']
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

