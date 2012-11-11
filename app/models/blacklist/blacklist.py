import sqlalchemy
from sqlalchemy import and_
from common.mysqlTables import MySQLTables
from common import egg_errors
import datetime


class Blacklist:
    def __init__(self, db, logging_file=None):
        self.db = db
        self.mysql_tables = MySQLTables(db)
        self.table = self.mysql_tables.blacklist
        self.lf = logging_file
        self.identifier = "BadgesUsers class"

    def log(self, e):
        if self.lf :
            self.lf.write(str(datetime.datetime.utcnow()) + " :: " + str(e) + "\n")
            self.lf.flush()

    def get_all_blacklisted_as_list(self):
        """Returns all blacklist pairs"""
        try:
            result = self.table.select().execute()
            if result.rowcount >= 1:
                return [x.values() for x in result]
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def get_all_blacklisted_as_dict(self):
        """Returns all blacklist pairs"""
        blacklist = self.get_all_blacklisted_as_list()
        R = dict()
        [ R.setdefault( x[0], [] ).append(x[1]) for x in blacklist ]
        return R


    def get_user_blacklisted(self, user_id):
        "Returns all blacklisted users for user with user_id"
        try:
            result = self.table.select(
                self.table.c.user_id == user_id ).execute()
            if result.rowcount >= 1:
                return [x.values()[1] for x in result]
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def add_to_blacklist(self, user_id, blacklist_user_id):
        """Adds user with blacklist_user_id to blacklisted users
        for given user with user_id"""
        try:
            self.table.insert().values( user_id=user_id,
                blacklisted_id=blacklist_user_id).execute()
        except sqlalchemy.exc.IntegrityError as e:
            if e.orig.args[0] == 1062 :
                # duplicate entry, don't care !
                pass
            elif e.orig.args[0] == 1452 :
                self.log(e, self.identifier)
                raise egg_errors.UnknownUserOrBadgeIDException
            else:
                self.log(e, self.identifier)
                raise egg_errors.QueryNotPossible
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible


    def delete_from_blacklist(self, user_id, blacklist_user_id):
        """Delete user with blacklist_user_id from blacklisted users
        for a user with user_id"""
        try:
            self.table.delete().where(and_(
                self.table.c.user_id == user_id,
                self.table.c.blacklisted_id == blacklist_user_id )).execute() 
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

    def is_blacklisted(self, user_id, blacklist_user_id):
        """Check if user with blacklist_user_id is among blacklisted users
        for a user with user_id"""
        try:
            result = self.table.select(and_(
                self.table.c.user_id == user_id,
                self.table.c.blacklisted_id == blacklist_user_id)).execute()
            if result.rowcount >= 1:
                return True
            elif result.rowcount == 0:
                return False
        except Exception as e:
            self.log(e, self.identifier)
            raise egg_errors.QueryNotPossible

