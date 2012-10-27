import sqlalchemy
from sqlalchemy import and_
from common.mysqlTables import MySQLTables
from common import egg_errors
from common.utils import ExceptionLogger, str2unicode
#import schema as badges_users_schema


class BadgesUsers( ExceptionLogger ):
    def __init__(self, db, logging_file=None):
        self.db = db
        self.mysql_tables = MySQLTables(db)
        self.table = self.mysql_tables.badges_users
        self.lf = logging_file

    def get_user_badges(self, user_id):
        "Returns badges for given user with user_id"
        try:
            result = self.table.select(
                self.table.c.user_id == user_id ).execute()
            if result.rowcount >= 1:
                return [dict(x.items()) for x in result]
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

    def get_user_badges_by_visibility(self, user_id, visibility):
        """Returns only those badges that comply to give visibility
        for given user with user_id"""
        try:
            result = self.table.select(and_(
                self.table.c.user_id == user_id,
                self.table.c.visibility == visibility )).execute()
            if result.rowcount >= 1:
                return [dict(x.items()) for x in result]
            elif result.rowcount == 0:
                return []
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

    def addchange_user_badge(self, user_id, badge_id, desc=None, visibility=0):
        """Adds/changes user badge"""
        try:
            self.table.insert().values( badge_id=badge_id, user_id=user_id,
                description=desc, visibility=visibility).execute()
        except sqlalchemy.exc.IntegrityError as e:
            # ako imamo duplicate entry onda je to promjena
            if e.orig.args[0] == 1062 :
                try:
                    self.table.update().where(and_(
                        self.table.c.user_id == user_id,
                        self.table.c.badge_id == badge_id)).values(
                            badge_id=badge_id, user_id=user_id,
                            description=desc, visibility=visibility).execute()
                except Exception as e:
                    self.log(e)
                    raise egg_errors.QueryNotPossible
            elif e.orig.args[0] == 1452 :
                self.log(e)
                raise egg_errors.UnknownUserOrBadgeIDException
            else:
                self.log(e)
                raise egg_errors.QueryNotPossible
        except:
            self.log(e)
            raise egg_errors.QueryNotPossible


    def delete_user_badge(self, user_id, badge_id):
        """Delete given badge for a user"""
        try:
            self.table.delete(and_(
                self.table.c.user_id == user_id,
                self.table.c.badge_id == badge_id )).execute() 
        except:
            self.log(e)
            raise egg_errors.QueryNotPossible


class Badges( ExceptionLogger ):
    def __init__(self, db, logging_file=None, images_path=None):
        self.db = db
        self.mysql_tables = MySQLTables(db)
        self.table = self.mysql_tables.badges
        self.lf = logging_file
        self.images_path = images_path

    def get_badges(self):
        try:
            badges = self.table.select().execute()
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

        if badges.rowcount == 0 :
            return []

        res = [dict(x) for x in badges]

        for r in res :
            if self.images_path :
                r['image_link'] = self.images_path + "/" + r['image_link']
            r['name'] = str2unicode(r['name'])
            r['description'] = str2unicode(r['description'])

        return res

    def __genTreeRec__( self, x, parent_ids, R ) :
        """Helper function for get_badges_as_tree"""
        if x['badge_id'] not in parent_ids :
            return( {'node': x, 'children': None} )
        else :
            return( { 'node': x, 'children' : [ self.__genTreeRec__(x, parent_ids, R) for x in R[ x['badge_id'] ] ] } )

    def get_badges_as_tree(self):
        """Generate badges tree"""
        try:
            badges = self.table.select().execute()
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

        if badges.rowcount == 0 :
            return []

        res = [dict(x) for x in badges]

        for r in res :
            if self.images_path :
                r['image_link'] = self.images_path + "/" + r['image_link']
            r['name'] = str2unicode(r['name'])
            r['description'] = str2unicode(r['description'])

        R = dict()

        # creates dict with key=parent_id
        # value=list(all of the children of that parent)
        [ R.setdefault( x['parent'], [] ).append(x) for x in res ]

        parent_ids = R.keys()

        # root node always has id=0
        return [ self.__genTreeRec__(x, parent_ids, R) for x in R[0]] 


