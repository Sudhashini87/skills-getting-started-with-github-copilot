"""Pytest configuration and fixtures for API tests."""

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient


@pytest.fixture
def test_activities_db():
    """
    Fixture: Arrange - Create a fresh test activities database for each test.
    Returns a clean copy of the activities dataset.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": []
        },
    }


@pytest.fixture
def app(test_activities_db):
    """
    Fixture: Arrange - Create a test FastAPI app instance with isolated test data.
    Each test gets a fresh app with the test database.
    """
    from fastapi.responses import RedirectResponse

    app = FastAPI(title="Test API")

    # Use the test database instead of the production one
    app.activities = test_activities_db

    @app.get("/")
    def root():
        return RedirectResponse(url="/static/index.html")

    @app.get("/activities")
    def get_activities():
        return app.activities

    @app.post("/activities/{activity_name}/signup")
    def signup_for_activity(activity_name: str, email: str):
        """Sign up a student for an activity"""
        # Validate activity exists
        if activity_name not in app.activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Get the specific activity
        activity = app.activities[activity_name]
        # Validate student is not already signed up
        if email in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student already signed up for this activity")

        # Add student
        activity["participants"].append(email)
        return {"message": f"Signed up {email} for {activity_name}"}

    @app.delete("/activities/{activity_name}/unregister")
    def unregister_from_activity(activity_name: str, email: str):
        """Unregister a student from an activity"""
        # Validate activity exists
        if activity_name not in app.activities:
            raise HTTPException(status_code=404, detail="Activity not found")

        # Get the specific activity
        activity = app.activities[activity_name]
        # Validate student is signed up
        if email not in activity["participants"]:
            raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

        # Remove student
        activity["participants"].remove(email)
        return {"message": f"Unregistered {email} from {activity_name}"}

    return app


@pytest.fixture
def client(app):
    """
    Fixture: Arrange - Create a TestClient for making HTTP requests to the test app.
    """
    return TestClient(app)
