from src.app import activities


def test_signup_prevents_duplicates(client):
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@example.com"

    # Act
    first_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    second_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Already signed up"


def test_unregister_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "testuser@example.com"
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act
    delete_response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]