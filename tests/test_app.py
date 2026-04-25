import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No special setup needed as activities are predefined
    
    # Act: Make a GET request to fetch activities
    response = client.get("/activities")
    
    # Assert: Check the response status and structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    # Check structure of an activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success():
    # Arrange: Ensure a clean state (assuming no prior signups for this email)
    
    # Act: Attempt to sign up a new participant
    response = client.post("/activities/Chess%20Club/signup?email=test@example.com")
    
    # Assert: Verify successful signup and that the participant was added
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Chess Club" in data["message"]
    
    # Verify the participant was added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # Arrange: Sign up a participant first
    client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    
    # Act: Try to sign up the same email again
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@example.com")
    
    # Assert: Check that it fails with the appropriate error
    assert response.status_code == 400
    data = response.json()
    assert "Student is already signed up" in data["detail"]

def test_signup_invalid_activity():
    # Arrange: No setup needed
    
    # Act: Attempt to sign up for a non-existent activity
    response = client.post("/activities/Invalid%20Activity/signup?email=test@example.com")
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # Arrange: Sign up a participant first
    client.post("/activities/Chess%20Club/signup?email=unregister@example.com")
    
    # Act: Unregister the participant
    response = client.delete("/activities/Chess%20Club/signup?email=unregister@example.com")
    
    # Assert: Verify successful unregistration and removal
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Chess Club" in data["message"]
    
    # Verify the participant was removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Chess Club"]["participants"]

def test_unregister_not_signed_up():
    # Arrange: No setup needed (participant not signed up)
    
    # Act: Attempt to unregister a non-participant
    response = client.delete("/activities/Chess%20Club/signup?email=notsigned@example.com")
    
    # Assert: Check for 400 error
    assert response.status_code == 400
    data = response.json()
    assert "Student not signed up" in data["detail"]

def test_unregister_invalid_activity():
    # Arrange: No setup needed
    
    # Act: Attempt to unregister from a non-existent activity
    response = client.delete("/activities/Invalid%20Activity/signup?email=test@example.com")
    
    # Assert: Verify 404 error
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_root_redirect():
    # Arrange: No setup needed
    
    # Act: Make a GET request to the root
    response = client.get("/")
    
    # Assert: Check that it redirects (or serves the static file)
    assert response.status_code == 200
    # Note: In a real scenario, you might check for redirect status if not following redirects