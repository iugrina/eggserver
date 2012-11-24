from common import egg_errors

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
            bp = self.db.Recommended.find({'user_id' : user_id})[0]
            if not bp :
                raise egg_errors.UnknownUserIDException

            r = bp['recommended']
            return sorted(r, key=lambda x: x['score'], reverse=True)
        except Exception as e:
            pass
            #self.log(e)
            raise egg_errors.QueryNotPossible
