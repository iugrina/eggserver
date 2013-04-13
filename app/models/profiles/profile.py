import sqlalchemy
import bcrypt
import confegg
from common.mysqlTables import MySQLTables
from common import egg_errors
from common import utils
import schema as profile_schema

from models.images.images import ProfileImages
from models.friends.friends import Friends
from models.badges.badges import BadgesUsers
from models.status.status import Status


class Profile:
    def __init__(self, db):
        self.db = db
        self.table = sqlalchemy.Table("users", self.db.metadata, autoload=True)
        self.mysql_tables = MySQLTables(db)

    def get_user(self, user_id):
        "Returns user with user_id"
        result = self.mysql_tables.users.select(
            self.mysql_tables.users.c.user_id == user_id).execute()
        if result.rowcount == 1:
            return dict(result.fetchone().items())
        raise egg_errors.QueryNotPossible

    def get_users_ids(self, start_user_id, number):
        """Returns number of users starting from start_user_id"""
        result = self.mysql_tables.users.select(
            self.mysql_tables.users.c.user_id >= start_user_id).execute()
        if number > 0:
            r = min(result.rowcount, number)
        else:
            r = result.rowcount
        l = list()
        while r >= 1:
            l.append(dict(result.fetchone().items())['user_id'])
            r = r - 1

        return l

    def add_user(self, params):
        "Creates a new user"
        profile_schema.validate_profiles(params)
        self.db.execute(self.mysql_tables.users.insert().values(params))

    def delete_user(self, user_id):
        "Deletes user with user_id"
        profile_schema.validate_int(user_id)
        if self.get_user(user_id).rowcount == 1:
            self.db.execute(self.mysql_tables.users.delete().where(
                self.mysql_tables.users.c.user_id == user_id))
        else:
            raise egg_errors.QueryNotPossible

    def update_user(self, user_id, params):
        "Updates user with user_id"
        profile_schema.validate_profiles(params)
        if self.get_user(user_id).rowcount == 1:
            self.db.execute(self.mysql_tables.users.update().where(
                self.mysql_tables.users.c.user_id == user_id).values(params))
        else:
            raise egg_errors.QueryNotPossible

    def login(self, params):
        "Try to authorize user"
        user = self.mysql_tables.users.c
        result = self.mysql_tables.users.select((
            user.username == params['username'])).execute()
        row = result.fetchone()

        if row is not None:
            if bcrypt.hashpw(params['password'], row.password) == row.password:
                data = dict(row)
                data['created'] = str(data['created'])
                data['dob'] = str(data['dob'])
                data['password'] = None
                data['first_name'] = utils.str2unicode(data['first_name'])
                data['last_name'] = utils.str2unicode(data['last_name'])
                return data
            else:
                return False
            raise egg_errors.QueryNotPossible

    def signup(self, params):
        "Sign up the user"
        params['password'] = bcrypt.hashpw(
            params['password'], bcrypt.gensalt())
        profile_schema.validate_profiles(params)
        self.db.execute(self.mysql_tables.users.insert().values(params))


class ProfileData():
    def __init__(self, mysqldb, mongodb, f=None):
        self.db = mysqldb
        self.p = Profile(self.db)
        self.i = ProfileImages(self.db, f)
        self.f = Friends(self.db, f)
        self.bu = BadgesUsers(self.db, f)
        self.s = Status(mongodb)

        conf = confegg.get_config()
        self.images_path = conf['env'][
            'static_url_path'] + conf['images']['images_root']

    def get_user_info(self, user_id):
        """Returns this and that about user"""

        basic_user_info = self.p.get_user(user_id)

        # get profile_image/friend_image, badges, friends
        friends = self.f.get_friends(user_id)
        if self.i.get_user_images_by_type(user_id, 'profile'):
            profile_image = self.i.get_image_path(
                self.i.get_user_images_by_type(user_id, 'profile')[0])
            profile_image = self.images_path + profile_image
        else:
            profile_image = ""
        badges = self.bu.get_user_badges(user_id)

        # ovo bi trebalo prilagoditi kad napravimo kod za activity/online/eggs
        # status
        activity = True
        online = True
        eggs = 0

        speech_bubble = self.s.get_last_status(user_id)
        speech_bubble["datetime"] = unicode(speech_bubble["datetime"])
        speech_bubble["last_status"] = utils.str2unicode(
            speech_bubble["last_status"])

        r = {"user_id": basic_user_info['user_id'],
             "first_name": utils.str2unicode(basic_user_info['first_name']),
             "last_name": utils.str2unicode(basic_user_info['last_name']),
             "nickname": utils.str2unicode(basic_user_info['nickname']),
             "activity": activity,
             "online": online,
             "status": speech_bubble,
             "profile_image": profile_image,
             "friends": friends,
             "eggs": eggs,
             "badges": badges
             }

        return r

    def get_users_info(self, start_user_id, number):
        """Returns this and that about users"""

        user_ids = self.p.get_users_ids(start_user_id, number)

        d = dict()
        for uid in user_ids:
            d[uid] = self.get_user_info(uid)

        return d

    def get_users_info_filtered(self, start_userd_id, number, F):
        """Returns this and that about users
        filtered by dict F"""

        badges_ids = F['badges']

        "trenutno podrzava samo filtriranje po bedzevima"
        user_ids = self.bu.get_users_by_badges(badges_ids)

        d = dict()
        if number == 0: number = len(user_ids)
        for uid in user_ids[0:number]:
            d[uid] = self.get_user_info(uid)

        return d
