from common import egg_errors as eggErrors
from mongodb_model import Basket

class MongoConnector:
    """MongoConnector class does mangling with MongoDB"""

    def __init__(self, db):
        self.db = db

    def get_baskets(self, user_id):
        "Returns all baskets for user with user_id"

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        return bp['baskets']

    def get_basket(self, user_id, basket_id):
        "Returns basket with basket_id for user_id"

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        for item in bp['baskets'] :
            if item['basket_id'] == basket_id :
                return item

        raise eggErrors.UnknownBasketIDException


    def add_basket(self, user_id, basket_name):
        "Creates new basket with basket_name for user with user_id"

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        baskets = bp['baskets']
        l = len(baskets)

        #
        # new baskets are added as last in the order of the baskets
        #

        # max basketid
        maxBID = 0
        # max basketorderid
        maxBOID = 0

        for ind in range(0,l) :
            maxBID = max(maxBID, baskets[ind]['basket_id'])
            maxBOID = max(maxBOID, baskets[ind]['basket_order_id'])

        baskets.append({'basket_name': unicode(basket_name), 'basket_id': maxBID+1, \
                        'basket_order_id' : maxBOID+1, 'users':[]})

        bp['baskets'] = baskets
        try:
            bp.save()
        except:
            # make tests!
            pass

    def delete_basket(self, user_id, basket_id):
        """Removes basket with basket_id from user with user_id
        Deletion of the last basket is forbidden"""

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        baskets = bp['baskets']
        l = len(baskets)

        if 1 == l :
            raise eggErrors.LastBasketDeleteException

        for ind in range(0, l):
            if baskets[ind]['basket_id'] == basket_id :
                del baskets[ind]
                break

        if l == len(baskets) : 
            raise eggErrors.UnknownBasketIDException
                
        try:
            bp['baskets'] = baskets
            bp.save()
        except:
            # make tests!
            pass

    def __check_sorting(self, l ) :
        "Check if sorting values are unique"
        # l = [(id,order_id),...]

        order_ids = [x[1] for x in l]
        order_ids.sort()

        for ind in range(0, len(order_ids)-1) :
            if not order_ids[ind] < order_ids[ind+1] :
                raise eggErrors.SortingValuesNonUniqueException


    def change_order_of_baskets(self, user_id, new_order):
        "Changes the order of baskets for user with user_id"

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        baskets = bp['baskets']

        if not len(new_order) == len(baskets) :
            raise eggErrors.IncorrectNumberOfBasketsException

        self.__check_sorting( new_order )

        # sorted_new_order_by_basketid
        s1 = sorted( new_order, key=lambda x: x[0])

        # sorted_baskets_by_basketid
        s2 = sorted(baskets, key=lambda x: x['basket_id'])

        new_baskets = range(0,len(baskets))

        for ind in range(0, len(baskets)) :
            if s1[ind][0] != s2[ind]['basket_id'] :
                raise eggErrors.MismatchBasketIDException
            else :
                s2[ind]['basket_order_id'] = s1[ind][1]

                try:
                    new_baskets[ s1[ind][1]-1 ] = s2[ind]
                except IndexError :
                    raise eggErrors.SortingValuesRangeException
                
        bp['baskets'] = new_baskets
        try:
            bp.save()
        except:
            # make tests!
            pass

        
    def change_order_of_users_in_basket(self, user_id, basket_id, new_order):
        "Changes the order of users in basket with basket_id for user with user_id"

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        baskets = bp['baskets']

        b = None
        for bas in baskets :
            if bas['basket_id'] == basket_id :
                b = bas
                break

        if not b :
            raise eggErrors.UnknownBasketIDException

        users = b['users']
        L = len(users)

        if not len(new_order) == len(users) :
            raise eggErrors.IncorrectNumberOfUsersException

        self.__check_sorting( new_order )

        # sorted_new_order_by_userid
        s1 = sorted( new_order, key=lambda x: x[0])

        # sorted_users_by_userid
        s2 = sorted( users, key=lambda x: x['user_id'])

        new_users = range(0,len(users))

        for ind in range(0, len(users)) :
            if s1[ind][0] != s2[ind]['user_id'] :
                raise eggErrors.MismatchUserIDException
            else :
                s2[ind]['user_order_id'] = s1[ind][1]

                try:
                    new_users[ s1[ind][1]-1 ] = s2[ind]
                except IndexError :
                    raise eggErrors.SortingValuesRangeException

        b['users'] = new_users
        try:
            bp.save()
        except:
            # make tests!
            pass


    def add_user_to_basket(self, user_id, basket_id, new_user_id):
        "Adds user with new_user_id to basket with basket_id for user with user_id"

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        baskets = bp['baskets']
        l = len(baskets)

        tmp = None
        for b in baskets :
            if b['basket_id'] == basket_id :
                tmp = b
                break

        if not tmp :
            raise eggErrors.UnknownBasketIDException

        users = tmp['users']

        #
        # new users are added as last in the order of the users
        #

        # max userorderid
        maxUOID = 0

        for u in users : 
            if u['user_id'] == new_user_id : 
                raise eggErrors.UserAlreadyInBasketException

            maxUOID = max(maxUOID, u['user_order_id'])

        users.append( {'user_id':new_user_id, 'user_order_id':maxUOID+1} )

        tmp['users'] = users

        try:
            bp['baskets'] = baskets
            bp.save()
        except:
            # make tests!
            pass


    def delete_user_from_basket(self, user_id, basket_id, del_user_id):
        """Removes user with del_user_id from basket with basket_id
        for user with user_id."""

        try:
            bp = self.db.Basket.find_one({'user_id' : user_id})
        except:
            # make tests!
            pass

        if not bp :
            raise eggErrors.UnknownUserIDException

        baskets = bp['baskets']
        l = len(baskets)

        tmp = None
        for b in baskets :
            if b['basket_id'] == basket_id :
                tmp = b
                break

        if not tmp :
            raise eggErrors.UnknownBasketIDException

        users = tmp['users']
        L = len(users)

        for ind in range(0, L) : 
            if users[ind]['user_id'] == del_user_id : 
                del users[ind]
                break

        if L == len(users) :
            raise eggErrors.UserNotInBasketException

        tmp['users'] = users
        bp['baskets'] = baskets

        try:
            bp.save()
        except:
            # make tests!
            pass


