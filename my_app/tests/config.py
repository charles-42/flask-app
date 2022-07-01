import os
SECRET_KEY = 'votre_nouvelle_cle_secrete'


basedir = os.path.abspath(os.path.dirname(__file__))

# Nouvelle base de données pour les tests.
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app_test.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
EXPLAIN_TEMPLATE_LOADING =True
# Active le debogueur
DEBUG = True
TESTING = True
LIVESERVER_PORT = 8943
LIVESERVER_TIMEOUT = 10

