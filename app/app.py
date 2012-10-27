# tornado
import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.options import options

# other python
import mongokit
import json
import sqlalchemy

# egg
import confegg
from common import utils, egg_errors, debugconstants
from lib.voluptuous import voluptuous as val

import controllers
import controllers.badges
import controllers.baskets
import controllers.blacklist
import controllers.friends
import controllers.images
import controllers.profiles
import controllers.recommended

import models
import models.baskets.dbproxy as dbproxy
from models.baskets.mongodb_model import Basket
from models.badges.badges import BadgesUsers, Badges
from models.blacklist.blacklist import Blacklist
from models.friends.friends import Friends
from models.images.images import ProfileImages
from models.profiles.profile import Profile, ProfileData
from models.recommended.mongodb_model import Recommended



class Application(tornado.web.Application):
  def __init__(self):
    conf = confegg.get_config()

    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #db.echo = "debug"

    handlers = []

    images_path = conf['env']['static_url_path'] + conf['images']['images_root']

    #
    # badges
    #
    fbadges = open(conf['log']['static_path']+conf['log']['badges'], "wa")

    badges_path = images_path + conf['images']['badges']

    badgesusers = BadgesUsers(db, fbadges)
    badges = Badges(db, logging_file=fbadges, images_path=badges_path)

    # koristit cemo vec gotovu listu i dict jer ce se bedzevi
    # uredjivati sa zasebnim alatom u "maintenance mode"-u
    badgeslist = badges.get_badges()
    badgestree = badges.get_badges_as_tree()

    handlers.extend([
        (r"/badges", controllers.badges.GetBadgesHandler, dict(badges=badges, badgeslist=badgeslist, badgestree=badgestree)),
        (r"/badges/tree", controllers.badges.GetBadgesTreeHandler, dict(badges=badges, badgeslist=badgeslist, badgestree=badgestree)),
        (r"/profile/([0-9]+)/badges", controllers.badges.GetBadgesForUserHandler, dict(badgesusers=badgesusers)),
        (r"/profile/([0-9]+)/badges/([0-9]+)", controllers.badges.AddChangeDeleteBadgesForUserHandler, dict(badgesusers=badgesusers))
        ])

    #
    # baskets
    #
    conBas = mongokit.Connection(conf['mongo']['host'], conf['mongo']['port'])
    conBas.register([Basket])

    baskets_dbp = dbproxy.DbProxy( conBas, None)

    handlers.extend([
        (r"/profile/([0-9]+)/baskets", controllers.baskets.GetChangeOrderBasketsHandler, dict(dbp=baskets_dbp)),
        (r"/profile/([0-9]+)/basket", controllers.baskets.AddBasketHandler, dict(dbp=baskets_dbp)),
        (r"/profile/([0-9]+)/basket/([0-9]+)", controllers.baskets.GetDelChangeOrderBasketHandler, dict(dbp=baskets_dbp)),
        (r"/profile/([0-9]+)/basket/([0-9]+)/([0-9]+)", controllers.baskets.AddDelUserFromBasketHandler, dict(dbp=baskets_dbp)),
        ])

    #
    # blacklist
    #
    fblacklist = open(conf['log']['static_path']+conf['log']['blacklist'], "wa")

    blacklist2db = Blacklist(db, fblacklist)
    # radi brzine radimo s dict-om !!!
    blacklist2dic = blacklist2db.get_all_blacklisted_as_dict()

    handlers.extend([
        (r"/profile/([0-9]+)/blacklist", controllers.blacklist.GetBlacklistHandler, dict(blacklist2db=blacklist2db, blacklist2dic=blacklist2dic)),
        (r"/profile/([0-9]+)/blacklist/([0-9]+)", controllers.blacklist.AddDeleteBlacklistedForUserHandler, dict(blacklist2db=blacklist2db, blacklist2dic=blacklist2dic)),
        ])

    #
    # friends
    #
    ffriends = open(conf['log']['static_path']+conf['log']['friends'], "wa")
    friends = Friends(db, ffriends)

    handlers.extend([
        (r"/profile/([0-9]+)/friends", controllers.friends.GetFriendsHandler, dict(friends=friends)),
        (r"/profile/([0-9]+)/friends/([0-9]+)", controllers.friends.AddDeleteFriendHandler, dict(friends=friends)),
        (r"/profile/([0-9]+)/friends/approve/([0-9]+)", controllers.friends.ApproveFriendHandler, dict(friends=friends)),
        ])
    
    #
    # images
    #
    fimages = open(conf['log']['static_path']+conf['log']['images'], "wa")

    profileimages = ProfileImages(db, fimages)

    handlers.extend( [
        (r"/profile/([0-9]+)/photos", controllers.images.GetAllProfileImagesHandler, dict(profileimages=profileimages, images_path=images_path)),
        (r"/profile/([0-9]+)/photos/friend", controllers.images.GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='friend')),
        (r"/profile/([0-9]+)/photos/profile", controllers.images.GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='profile')),
        (r"/profile/([0-9]+)/photos/other", controllers.images.GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='other')),
        (r""+images_path+"/(.*)", tornado.web.StaticFileHandler, {"path": conf['env']['static_path']+conf['images']['images_root']}),
    ] )

    # 
    # profiles
    #
    fprofile = open(conf['log']['static_path']+conf['log']['profiles'], "wa")
    profiledata = ProfileData( db, fprofile )

    handlers.extend([
        (r"/profile/", controllers.profiles.ProfilesHandler, dict(db=db)),
        (r"/profile/([0-9]+)", controllers.profiles.ProfileHandler, dict(db=db, profiledata=profiledata)),
        (r"/profile/login/", controllers.profiles.LoginHandler, dict(db=db)),
        (r"/profile/signup/", controllers.profiles.SignupHandler, dict(db=db))
        ])

    #
    # recommended
    #
    conRec = mongokit.Connection(conf['mongo']['host'], conf['mongo']['port'])
    conRec.register([Recommended])

    recommended_dbp = models.recommended.recommended.Recommended( conRec)

    handlers.extend( [
        (r"/profile/([0-9]+)/recommended", controllers.recommended.GetRecommendedHandler, dict(dbp=recommended_dbp)),
        ])
    
    #
    # events
    #
    handlers.extend( [
      (r"/event/", controllers.events.EventsHandler, dict(db=db)),
      (r"/event/([0-9]+)", controllers.events.EventHandler, dict(db=db)),
      (r"/event/([0-9]+)/user/([0-9]+)", controllers.events.EventUserHandler, dict(db=db)),
    ] )



    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

