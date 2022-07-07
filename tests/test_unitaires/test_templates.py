from my_app.models import User

def test_profile_template_context(client, captured_templates) -> None:
    User(email = "test@test.test", name = "test", password = 'sha256$zU9nb9Fu6i2pLdmP$a1587105ab6efe3dd726cade3e95ab3ac039d58c0ecf40395871a0a071948c8f').save_to_db()
    route = "/profile"
    
    with client:
        client.post("/login", data={"email": "test@test.test", "password" : "auser"})
        # session is still accessible
        response = client.get(route) 
        assert response.status_code == 200 #unauthorize
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == "profile.html"
        assert context["name"] == "test"

