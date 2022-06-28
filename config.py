
import os
from dotenv import load_dotenv

load_dotenv(override=True)



# Database initialization
if os.environ.get('PRODUCTION') is None:
# Test config
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SECRET_KEY = '#d#JCqTTW\nilK\\7m\x0bp#\tj~#H'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
else:
# Production config
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ.get('PRODUCTION')