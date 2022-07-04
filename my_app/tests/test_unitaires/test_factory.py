from flask import url_for
from flask import session
from ...models import User
from flask_login import current_user
from werkzeug.security import check_password_hash

# Test du fonctionnement du client de test

def test_configtest(app):
    print(app.blueprints.keys())
    assert "auth" in  app.blueprints
    assert "main" in  app.blueprints

    assert app.config["TESTING"] == True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == 'sqlite:////Users/charles/Documents/pythonProject/flask-app/app_test.db'

