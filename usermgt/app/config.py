import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    USERNAME = os.environ.get('USERNAME') or 'postgres'
    PASSWORD = os.environ.get('PASSWORD') or 'postgres'
    URL = os.environ.get('HOST') or 'localhost:5432'
    DATABASE_NAME = os.environ.get('DATABASE_NAME') or 'usermgt'
    DATABASE_CONNECTION_URI = 'postgresql://' + USERNAME+':'+PASSWORD+'@'+URL+'/'+DATABASE_NAME
    TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13

