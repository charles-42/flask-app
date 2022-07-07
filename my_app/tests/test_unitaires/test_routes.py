from flask import url_for
from flask import session
from ...models import User
from flask_login import current_user
from werkzeug.security import check_password_hash



##################### Test des routes de main #####################

### Test de Index

def test_index(client):
    route = "/"
    response = client.get(route)
    assert response.status_code == 200
    assert b"<title>Index page</title>" in response.data

### Test de Profile

### Test de Profile sans être connecté

def test_profile_not_logged(client):
    route = "/profile"
    # sans login le profile nous redirige vers le login, on utilise le paramètre follow_redirects)
    response = client.get(route, follow_redirects=True) 
    assert response.status_code == 200 #unauthorize
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # On vérifie qu'on est bien redirigé vers le login
    assert response.request.path == "/login"

### Test de Profile en étant connecté

def test_profile_logged(client,captured_templates):
    
    User(email = "test@test.test", name = "test", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    route = "/profile"
    # on va utiliser le mécanisme de session pour faire une première requete de log
    # puis les requetes que l'on recherche.
    with client:
        client.post("/login", data={"email": "test@test.test", "password" : "auser"})
        # session is still accessible
        response = client.get(route) 
        assert response.status_code == 200 #unauthorize
        assert response.request.path == "/profile"
        template, context = captured_templates[0]
        # On teste si on utilise le bon template
        assert template.name == "profile.html"
        # On teste maintenant si on envoie les bonnes informations au template
        assert context["name"] == "test"
### Test de Admin

### Test de Admin sans être connecté

def test_admin_not_logged(client):
    route = "/admin"
    # sans login le profile nous redirige vers le login, on utilise le paramètre follow_redirects)
    response = client.get(route, follow_redirects=True) 
    assert response.status_code == 200 #unauthorize
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # On vérifie qu'on est bien redirigé vers le login
    assert response.request.path == "/login"

### Test de Admin en étant connecté non admin

def test_admin_logged_not_admin(client):
    
    User(email = "test@test.test", group = 1, password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    route = "/admin"
    # on va utiliser le mécanisme de session pour faire une première requete de log
    # puis les requetes que l'on recherche.
    with client:
        client.post("/login", data={"email": "test@test.test", "password" : "auser"})
        # session is still accessible
        response = client.get(route, follow_redirects=True) 
        assert response.status_code == 200 #unauthorize
        assert response.request.path == "/profile"
        assert b"have permission to access this resource." in response.data


### Test de Admin en étant connecté comme admin

def test_admin_logged_as_admin(client, captured_templates):
    
    User(email = "test@test.test", group = 0, name= "test", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    route = "/admin"
    # on va utiliser le mécanisme de session pour faire une première requete de log
    # puis les requetes que l'on recherche.
    with client:
        client.post("/login", data={"email": "test@test.test", "password" : "auser"})
        # session is still accessible
        response = client.get(route) 
        assert response.status_code == 200 #unauthorize
        assert response.request.path == "/admin"
        template, context = captured_templates[0]
        # On teste si on utilise le bon template
        assert template.name == "admin_profile.html"
        # On teste maintenant si on envoie les bonnes informations au template
        assert context["name"] == "test"
        



##################### Test des routes de auth #####################

### Test de login

##### Test de login - GET

def test_login_get(client):
    route = "/login"
    response = client.get(route)
    assert response.status_code == 200
    assert b"<title>Login page</title>" in response.data
    

##### Test de Login - POST

def test_login_post_success(client):
    User(email = "test@test.test", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()  
    route = "/login"
    response = client.post(route, data={"email": "test@test.test", "password" : "auser"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/profile"

def test_login_post_not_existing(client):
    route = "/login"
    response = client.post(route, data={"email": "wronguser@test.test", "password" : "auser"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
    # on vérifie que le message d'erreur flask s'est bien créé
    assert b"Please check your login details and try again." in response.data

def test_login_post_wrong_password(client):
    User(email = "test@test.test", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()  
    route = "/login"
    response = client.post(route, data={"email": "test@test.test", "password" : "wrongpassword"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"
    # on vérifie que le message d'erreur flask s'est bien créé
    assert b"Please check your login details and try again." in response.data

### Test de Signup

##### Test de Signup - GET

def test_Signup_get(client):
    route = "/signup"
    response = client.get(route)
    assert response.status_code == 200
    assert b"<title>Signup page</title>" in response.data
    

##### Test de Signup - POST

def test_Signup_post_success(client):
    route = "/signup"
    with client:
        response = client.post(route, data={"email": "test@test.test", "password" : "test"}, follow_redirects=True)
        assert response.status_code == 200
        assert response.request.path == "/login"
        # on vérifie qu'un client a été créé dans la data base
        created_user = User.find_by_email("test@test.test") 
        assert created_user.email == "test@test.test"
        assert created_user.group == 1
        assert check_password_hash(created_user.password, "test") 
        

# On ne fait pas de test sur le validateur de l'email car ce dernier est dans le fichier html
# Il faudra donc le tester au moment des tests fonctionnels
def test_Signup_post_wrong_email(client):
    route = "/signup"
    response = client.post(route, data={"email": "test", "password" : "test"}, follow_redirects=True)
    assert response.status_code == 200
    assert response.request.path == "/login"


# On teste que si on ajoute deux fois le meme utilisateur, cela renvoie une erreur
def test_Signup_post_already_a_user(client):
    User(email = "test@test.test", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()  
    route = "/signup"
    response = client.post(route, data={"email": "test@test.test", "password" : "test"}, follow_redirects=True)
    assert response.status_code == 200
    # en cas d'erreur on est redirigé sur le sign up
    assert response.request.path == "/signup"
    # on vérifie que le message d'erreur flask s'est bien créé
    assert b"Email address already exists" in response.data

### Test de Logout

##### Test de Logout - GET

def test_logout_get(client):
    with client:
        client.post("/login", data={"email": "cb@gmail.com", "password" : "auser"})
         # on vérifie qu'on est bien connecté
        assert current_user.email == "cb@gmail.com"
        route = "/logout"
        response = client.get(route, follow_redirects=True) 
        # on vérifie qu'on est bien déconnecté
        assert current_user.is_anonymous == True
        assert response.status_code == 200 #unauthorize
        assert response.request.path == "/"