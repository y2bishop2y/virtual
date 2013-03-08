# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))



CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]



SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


#------------------------
# Mail server settings
#------------------------
MAIL_SERVER = 'localhost'
MAIL_PORT   = 25
MAIL_USE_TLS = False
MAIL_USE_SSL = False
MAIL_USERNAME = 'test'
MAIL_PASSWORD = 'test-passw'

#------------------------
# Administrator List
#------------------------
ADMINS = ['emiliano@medlista.com']


#------------------------
#------------------------
POST_PER_PAGE = 3


#------------------------
# Search
#------------------------
WHOOSH_BASE = os.path.join(basedir, 'search.db')
MAX_SEARCH_RESULTS = 50


#------------------------
#------------------------
LANGUAGES = {
	'en' : 'English',
	'es': 'EspaÃ±ol'
}




