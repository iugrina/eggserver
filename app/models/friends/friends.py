import sqlalchemy
from sqlalchemy import and_
from common.mysqlTables import MySQLTables
from common import egg_errors


#
# trebala bi postojati negdje provjera
# za paramtre user_id, friend_id !!!
# mozda bi bilo najpametnije to staviti
# u common i raditi kod primanja paramatera
# u samom app-u
#


class Friends:
    def __init__(self, db, logging_file=None):
        self.db = db
        self.mysql_tables = MySQLTables(db)
        self.table = self.mysql_tables.friends
        self.lf = logging_file

    def log(self, e):
        if self.lf :
            self.lf.write(str(datetime.datetime.utcnow()) + " :: " + str(e) + "\n")
            self.lf.flush()


    def get_friends(self, user_id):
        "Returns friends for user with user_id"
        try:
	        result = self.table.select(
	            self.table.c.user_id == user_id ).execute()
	        if result.rowcount >= 1:
	            # ovdje bi sad trebalo dohvatiti za sve friendove
	            # njihove profile i onda ih vratiti natrag kao listu
	            return [x.values() for x in result]
	        elif result.rowcount == 0:
	            return []
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

    def add_friend(self, user_id, friend_id):
        "Adds friend with friend_id to user with user_id"
        # pretpostavljamo da postoji korisnici user_id, friend_id
        try: 
            self.table.insert().values( user_id=user_id, friend_id=friend_id, approved=0 ).execute()
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

    def delete_friend(self, user_id, friend_id):
        "Delete friend with friend_id from user with user_id"
        try: 
            self.table.delete().where(and_(self.table.c.user_id == user_id,
                self.table.c.friend_id == friend_id)).execute()
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible

    def approve_friend(self, user_id, friend_id):
        "Approve friendship friend_id -> user_id"
        try: 
            self.table.update().where(and_(self.table.c.user_id == user_id,
                self.table.c.friend_id == friend_id)).values(approved=1).execute()
        except Exception as e:
            self.log(e)
            raise egg_errors.QueryNotPossible


