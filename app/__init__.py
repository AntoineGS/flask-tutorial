from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment

config = Config
app = Flask(__name__)
# Flask configs
app.config['SECRET_KEY'] = config.secretKey
# SQLAlchemy configs
app.config['SQLALCHEMY_DATABASE_URI'] = config.sqlAlchemyDatabaseUri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Flask Mail configs
app.config['MAIL_SERVER'] = config.mailServer
app.config['MAIL_PORT'] = config.mailPort
app.config['MAIL_USE_TLS'] = config.mailUseTls
app.config['MAIL_USERNAME'] = config.mailUsername
app.config['MAIL_PASSWORD'] = config.mailPassword

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

from app import routes, models, errors

if not app.debug:
    if config.mailServer:
        auth = None
        if config.mailUsername or config.mailPassword:
            auth = (config.mailUsername, config.mailPassword)
        secure = None
        if config.mailUseTls:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(config.mailServer, config.mailPort),
            fromaddr='no-reply@' + config.mailServer,
            toaddrs=config.admins, subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
