#!/usr/bin/env python

# tornado
import tornado.ioloop
import tornado.web
import tornado.escape

# other python
import json
import sqlalchemy

# egg
import confegg
from common import utils, debugconstants, egg_errors

import controllers
from models.images.images import ProfileImages

class ProfileImagesHandler(tornado.web.RequestHandler):
    def initialize(self, profileimages, images_path, t=None  ):
        self.pi = profileimages
        # t = type
        self.t = t
        self.images_path = images_path

    def get_current_user(self):
        return self.get_secure_cookie("id")

    def prepare(self):
        if debugconstants.eggAuthenticate==True and not self.current_user :
            self.write( egg_errors.UnauthenticatedException().get_json() )
            self.finish()


class GetAllProfileImagesHandler(ProfileImagesHandler):
    def get(self, user_id):
        user_id = int(user_id)
        try:
            r = self.pi.get_user_images(user_id)
            for x in r:
                x['url'] = self.images_path + self.pi.get_image_path(x)
            self.write( json.dumps( r, ensure_ascii=False) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )

class GetProfileImagesByTypeHandler(ProfileImagesHandler):
    def get(self, user_id):
        user_id = int(user_id)
        try:
            # profile i friend slike su iste samo razlicite velicine
            # te se nalaze u razlicitim direktorijima
            # pa zato ovaj mali mumbo jumbo
            if self.t == 'friend' :
                r = self.pi.get_user_images_by_type(user_id, 'profile')
            else: 
                r = self.pi.get_user_images_by_type(user_id, self.t)
            for x in r:
                if( self.t == 'friend' ) : 
                    x['url'] = self.images_path + self.pi.get_image_path(x, 'friend')
                else :
                    x['url'] = self.images_path + self.pi.get_image_path(x)
            self.write( json.dumps( r, ensure_ascii=False) )
        except egg_errors.BaseException as e :
            self.write( e.get_json() )


if __name__ == "__main__":

    conf = confegg.get_config()
    db = sqlalchemy.create_engine("mysql://" + conf['mysql']['username'] + ":" +
                                       conf['mysql']['password'] + "@" + conf['mysql']['host'] + "/" +
                                       conf['mysql']['database'])
    db.metadata  = sqlalchemy.MetaData(bind=db)
    #self.db.echo = "debug"

    f = open(conf['log']['static_path']+conf['log']['images'], "wa")

    profileimages = ProfileImages(db, f)
    images_path = conf['env']['static_url_path'] + conf['images']['images_root']

    settings = dict(
      debug=debugconstants.debug,
      cookie_secret=debugconstants.cookie_secret,
    )

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/photos", GetAllProfileImagesHandler, dict(profileimages=profileimages, images_path=images_path)),
        (r"/profile/([0-9]+)/photos/friend", GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='friend')),
        (r"/profile/([0-9]+)/photos/profile", GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='profile')),
        (r"/profile/([0-9]+)/photos/other", GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='other')),
        (r""+images_path+"/(.*)", tornado.web.StaticFileHandler, {"path": conf['env']['static_path']+conf['images']['images_root']}),
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

