
import os
from dotenv import load_dotenv
import tempfile
load_dotenv()


class Config(object):
    TESTING = False
    
    SECRET_KEY = '#d#JCqTTW\nilK\\7m\x0bp#\tj~#H'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "ma super base de prode"

class DevelopmentConfig(Config):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

class TestingConfig(Config):
    db_fd, db_path = tempfile.mkstemp()
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + db_path
    TESTING = True
    LIVESERVER_PORT = 8943
    LIVESERVER_TIMEOUT = 10
    




