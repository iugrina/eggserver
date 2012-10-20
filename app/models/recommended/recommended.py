from common import egg_errors as eggErrors

class Recommended:
    """Recommended class does mangling with MongoDB
    to get recommended users"""

    def __init__(self, db):
        self.db = db

    def log(self, e):
        if self.lf :
            self.lf.write(str(datetime.datetime.utcnow()) + " :: " + str(e) + "\n")
            self.lf.flush()

    def get_recommended(self, user_id):
        try:
            bp = self.db.Recommended.find_one({'user_id' : user_id})
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

        if not bp :
            raise eggErrors.UnknownUserIDException

        return bp['recommended']


