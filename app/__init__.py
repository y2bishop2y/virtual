import os
from flask import Flask
from flask.ext.openid import OpenID 
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.babel import Babel, lazy_gettext

from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from momentjs import momentjs


app = Flask(__name__)
app.config.from_object('config')
app.jinja_env.globals['momentjs'] = momentjs

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
lm.login_message = lazy_gettext('Please log in to access this page.')

oid = OpenID(app, os.path.join(basedir, 'tmp'))

mail = Mail(app)
babel = Babel(app)


from app import views, models

if not app.debug:
	import logging

	from logging.handlers import RotatingFileHandler

	file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)

	file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('microblog startup')
	




"""
EMAIL LOGGING
if not app.debug
	import logging

	from logging.handler import SMTPHandler
	credentials = None

	if MAIL_USERNAME or MAIL_PASSWORD:
		credentials = (MAIL_USER_NAME, MAIL_PASSWORD )

	mail_handler = SMTPHandler(MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'failure', credentials)

	mail_handler.setLEvel(logging.ERROR)
	app.logger.addHandler(mail_handler)
"""
