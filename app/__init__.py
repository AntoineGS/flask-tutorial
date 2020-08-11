from config import Config
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()
config = Config


def create_app(config_class=Config):
    global config
    app = Flask(__name__)
    # Flask configs
    config = config_class
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
    app.testing = config.testing

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app import models
    from app.auth import routes
    from app.auth import bp as auth_bp
    from app.errors import bp as errors_bp
    from app.main import bp as main_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    if not app.debug and not app.testing and config.mailServer:
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

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(config.languages)