from flask import url_for
from flask import session
from ...models import User
from flask_login import current_user
from werkzeug.security import check_password_hash

#################  Test de User #################

### Test de json

def test_user_json(client):
    User(email = "test@test.test", name = "test", group = 1, password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    assert User.find_by_email("test@test.test").json() == {"id":3,"email" : "test@test.test", "name" : "test", "group" : 1}


def test_user_find_by_email(client):
    User(email = "test@test.test", name = "test", group = 1, password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    assert User.find_by_email("test@test.test").name == "test"


