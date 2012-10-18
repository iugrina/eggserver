import sqlalchemy
from common.mysqlTables import MySQLTables
from common import egg_errors
import datetime

class ProfileImages:
    def __init__(self, db, logging_file=None):
        self.db = db
        self.mysql_tables = MySQLTables(db)
        self.table = self.mysql_tables.profile_images
        self.lf = logging_file

    def log(self, e):
        if self.lf :
            self.lf.write(str(datetime.datetime.utcnow()) + " :: " + str(e) + "\n")
            self.lf.flush()
        else:
            print str(datetime.datetime.utcnow()) + " :: " + str(e)

    def get_user_images(self, user_id):
        "Returns all images for given user"
        try:
            result = self.table.select(
                self.table.c.user_id == user_id ).execute()
            if result.rowcount >= 1:
                r = [x.values() for x in result]
                for x in r :
                    x[3] = str(x[3])
                return r
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

    def get_user_images_by_type(self, user_id, t):
        """Returns only those images that comply to given type
        for given user with user_id"""
        try:
            result = self.table.select(and_(
                self.table.c.user_id == user_id,
                self.table.c.type == t)).execute()
            if result.rowcount >= 1:
                r = [x.values() for x in result]
                for x in r :
                    x[3] = str(x[3])
                return r
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible


