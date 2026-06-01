from urllib.parse import quote
import src.app as app_mod


def test_get_activities(client):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body


def test_signup_success(client):
    # Arrange
    activity = "Tennis Club"
    email = "newstudent@mergington.edu"
    assert email not in app_mod.activities[activity]["participants"]

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email in app_mod.activities[activity]["participants"]
    assert f"Signed up {email}" in response.json()["message"]


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Tennis Club"
    email = "duplicate@mergington.edu"
    client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_missing_activity_returns_404(client):
    # Arrange
    activity = "Nonexistent Activity"
    email = "missing@mergington.edu"

    # Act
    response = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_success(client):
    # Arrange
    activity = "Tennis Club"
    email = "sarah@mergington.edu"
    assert email in app_mod.activities[activity]["participants"]

    # Act
    response = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert email not in app_mod.activities[activity]["participants"]
    assert "Unregistered" in response.json()["message"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity = "Tennis Club"
    email = "notfound@mergington.edu"
    assert email not in app_mod.activities[activity]["participants"]

    # Act
    response = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
