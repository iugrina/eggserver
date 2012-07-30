from models.baskets.mongodb_model import Basket
from mongokit import *
import random

connection = Connection('localhost', 27017)
connection.register([Basket])

for i in range(1,1001) :
    user_id = i
    num_of_baskets = random.choice(range(1,9))
    baskets = list()

    for j in range(1,num_of_baskets+1) :
        basket_id = j
        basket_name = u"traka_" + str(j)
        basket_order_id = j

        users = list()
        num_of_users = random.choice(range(1,9))
        user_ids = range(1,i) + range(i+1,1001)
        user_ids = random.sample( user_ids, num_of_users)

        for k in range(0,num_of_users) :
            users.append({'user_id' : user_ids[k], 'user_order_id' : k+1})

        baskets.append( { 'basket_id':basket_id, 'basket_name':basket_name, \
                          'basket_order_id':basket_order_id, 'users':users } )

    bp = connection.Basket()
    bp['user_id'] = user_id
    bp['baskets'] = baskets
    bp.save()






