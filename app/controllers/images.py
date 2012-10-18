#!/usr/bin/env python

import tornado.ioloop
import tornado.web
import tornado.escape

import json

import sqlalchemy
import controllers
from common import utils
import confegg
import common.egg_errors as eggErrors
from models.images.images import ProfileImages

class ProfileImagesHandler(tornado.web.RequestHandler):
    def initialize(self, profileimages, images_path, t=None  ):
        self.pi = profileimages
        self.t = t
        self.images_path = images_path

class GetAllProfileImagesHandler(ProfileImagesHandler):
    def get(self, user_id):
        user_id = int(user_id)
        try:
            r = self.pi.get_user_images(user_id)
            r2 = list()
            for x in r:
                r2.append( [self.images_path  + str(x[5]) + "/" + str(x[0]) + str(x[7]), x[2], x[3], x[4]] )
            self.write( json.dumps( r2, ensure_ascii=False) )
        except eggErrors.BaseException as e :
            self.write( e.get_json() )

class GetProfileImagesByTypeHandler(ProfileImagesHandler):
    def get(self, user_id):
        user_id = int(user_id)
        try:
            # profile i friend slike su iste samo razlicite velicine
            # te se nalaze u razlicitim direktorijima
            # pa zato ovaj mali mumbo jumbo
            if( self.t == 'friend' ) : t = 'profile'
            else : t = self.t
            r = self.pi.get_user_images_by_type(user_id, t)
            r2 = list()
            for x in r:
                if( self.t == 'friend' ) : tmp = 'friend'
                else : tmp = x[5]
                r2.append( [self.images_path + str(tmp) +"/" + str(x[0]) + str(x[7]), x[2], x[3], x[4]] )
            self.write( json.dumps( r2, ensure_ascii=False) )
        except eggErrors.BaseException as e :
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

    application = tornado.web.Application([
        (r"/profile/([0-9]+)/images", GetAllProfileImagesHandler, dict(profileimages=profileimages, images_path=images_path)),
        (r"/profile/([0-9]+)/images/friend", GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='friend')),
        (r"/profile/([0-9]+)/images/profile", GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='profile')),
        (r"/profile/([0-9]+)/images/other", GetProfileImagesByTypeHandler, dict(profileimages=profileimages, images_path=images_path, t='other')),
        (r"/static/images/(.*)", tornado.web.StaticFileHandler, {"path": conf['env']['static_path']+conf['images']['images_root']}),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()


