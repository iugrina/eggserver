import json

class BaseException(Exception):
    def __init__(self):
        Exception.__init__(self)
        self.error_code = 0
        self.error_message = u""

    def get_json(self) :
        return json.dumps( {'error_code':self.error_code, \
                            'error_message':self.error_message} )


# 
# global exceptions 100-999
#

class UnknownUserIDException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 100
        self.error_message = u"Unknown User ID"

class UnknownBasketIDException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 101
        self.error_message = u"User does not have a basket with that basket_id"


class QueryNotPossible(BaseException):
  def __init__(self):
    BaseException.__init__(self)
    self.error_code = 1000
    self.error_message = u"Error"

#
# Basket mangling exceptions 10000-10199
#

class LastBasketDeleteException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10000
        self.error_message = u"Trying to delete last basket"

class UserAlreadyInBasketException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10001
        self.error_message = u"User is already in that basket"

class UserNotInBasketException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10002
        self.error_message = u"User is not in that basket"

class SortingValuesNonUniqueException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10003
        self.error_message = u"Values used in sorting of baskets/users are not unique"

class SortingValuesRangeException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10004
        self.error_message = u"Values used in sorting must be 1,...,number of baskets"


class IncorrectNumberOfBasketsException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10005
        self.error_message = u"Incorrect number of baskets for basket sorting"

class IncorrectNumberOfUsersException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10006
        self.error_message = u"Incorrect number of baskets for basket sorting"

class MismatchBasketIDException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10007
        self.error_message = u"Basket ids used for sorting are incorrect"

class MismatchUserIDException(BaseException):
    def __init__(self):
        BaseException.__init__(self)
        self.error_code = 10008
        self.error_message = u"User ids used for sorting are incorrect"






