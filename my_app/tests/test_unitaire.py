def test_configtest(app):
    assert app.config["TESTING"] == True

def test_easy(client):
    route = "/"
    rv = client.get(route)
    assert rv.status_code == 200
