import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'some-secret-string'
    DEBUG = True
    CSRF_ENABLED = True

class Configdb(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                                  'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Configjwt(object):
    JWT_SECRET_KEY = 'jwt-secret-string'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_USER_CLAIMS = "User"
    JWT_ACCESS_TOKEN_EXPIRES = 3 * 60 * 60
    JWT_REFRESH_TOKEN_EXPIRES = 7 * 24 * 60 * 60

class Run(Config, Configjwt, Configdb):
    pass