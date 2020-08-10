import os
basedir = os.path.abspath(os.path.dirname(__file__))


# class Config(object):
class Config:
    secretKey = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    sqlAlchemyDatabaseUri = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    mailServer = os.environ.get('MAIL_SERVER')
    mailPort = int(os.environ.get('MAIL_PORT') or 25)
    mailUseTls = os.environ.get('MAIL_USE_TLS') is not None
    mailUsername = os.environ.get('MAIL_USERNAME')
    mailPassword = os.environ.get('MAIL_PASSWORD')
    admins = ['antoineg.simard@gmail.com']
    postsPerPage = 25
    languages = ['en', 'es']
