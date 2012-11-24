from common import egg_errors
from common.utils import ExceptionLogger

class Recommended(ExceptionLogger):
    """Recommended class does mangling with MongoDB
    to get recommended users"""

    def __init__(self, db, logging_file=None):
        self.db = db
        self.identifier = "Recommended class"
        self.lf = logging_file

    def log(self, e):
        if self.lf :
            self.lf.write(str(datetime.datetime.utcnow()) + " :: " + str(e) + "\n")
            self.lf.flush()

    def get_recommended(self, user_id, start_id=0, size=0):
        try:
            bp = self.db.Recommended.find({'user_id' : user_id})[0]
            if not bp :
                raise egg_errors.UnknownUserIDException

            r = bp['recommended']
            rs = sorted(r, key=lambda x: x['score'], reverse=True)
            l = len(rs)

            print l
            print size

            # start_id == 0 -> from beginning
            if 0 == start_id :
                if 0 == size :
                    return rs
                else :
                    return rs[0:min(l,size)]
            else:
                ind = 0
                for x in rs:
                    if x['user_id'] == start_id :
                        break
                    ind += 1
                if 0 == size :
                    return rs
                else :
                    return rs[ind:min(l,ind+size)]

        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

