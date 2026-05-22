from fastapi.testclient import TestClient
from src import app
from src.app import activities


def setup_function():
    # ensure test email is not present before each test
    email = "testuser@example.com"
    for activity in activities.values():
        if email in activity["participants"]:
            activity["participants"].remove(email)


def test_signup_prevents_duplicates():
    client = TestClient(app.app)
    activity_name = "Chess Club"
    email = "testuser@example.com"

    # first signup should succeed
    r1 = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert r1.status_code == 200
    assert activities[activity_name]["participants"].count(email) == 1

    # second signup should be rejected
    r2 = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert r2.status_code == 400
    assert activities[activity_name]["participants"].count(email) == 1


def test_unregister_participant():
    client = TestClient(app.app)
    activity_name = "Chess Club"
    email = "testuser@example.com"

    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]

    delete_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})
    assert delete_response.status_code == 200
    assert email not in activities[activity_name]["participants"]
