import sqlalchemy
from sqlalchemy import and_
from common.mysqlTables import MySQLTables
from common import egg_errors
from common.utils import ExceptionLogger
import datetime

class ProfileImages( ExceptionLogger ):
    def __init__(self, db, logging_file=None):
        self.db = db
        self.mysql_tables = MySQLTables(db)
        self.table = self.mysql_tables.profile_images

        # superclass 
        self.lf = logging_file

        self.identifier = "ProfileImages class"

    def get_user_images(self, user_id):
        "Returns all images for given user"
        try:
            result = self.table.select(
                self.table.c.user_id == user_id ).execute()
            if result.rowcount >= 1:
                r = [dict(x.items()) for x in result]
                for x in r :
                    x['created'] = str(x['created'])
                return r
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def get_user_images_by_type(self, user_id, t):
        """Returns only those images that comply to given type
        for given user with user_id"""
        try:
            result = self.table.select(and_(
                self.table.c.user_id == user_id,
                self.table.c.type == t)).execute()
            if result.rowcount >= 1:
                r = [dict(x.items()) for x in result]
                for x in r :
                    x['created'] = str(x['created'])
                return r
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def get_image_path(self, pi, forced_type=None):
        """Creates path to the image without root part
           e.g. /profile/123456701.jpg
                /friend/123456701.jpg
                /other/123456789.jpg

           pi should be an image obtained by get_user_images*
           if forced_type is ! None then it will be used in path
        """
        if not forced_type :
            return "/" + str(pi['type']) + "/" + str(pi['image_id']) + str(pi['extension'])
        else :
            return "/" + str(forced_type) + "/" + str(pi['image_id']) + str(pi['extension'])

