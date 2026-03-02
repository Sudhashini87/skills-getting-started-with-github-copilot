"""Tests for GET /activities endpoint."""

import pytest


class TestGetActivities:
    """Test suite for activities retrieval endpoint."""

    def test_get_all_activities_returns_200(self, client):
        """Test that GET /activities returns HTTP 200 status."""
        # Arrange
        expected_status_code = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status_code

    def test_get_all_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary of activities."""
        # Arrange
        expected_type = dict

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, expected_type)

    def test_get_all_activities_contains_expected_keys(self, client):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert all(field in activity_data for field in required_fields), \
                f"Activity '{activity_name}' missing required fields"

    def test_get_all_activities_participants_is_list(self, client):
        """Test that participants field is always a list."""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Participants for '{activity_name}' should be a list"

    def test_get_all_activities_contains_test_data(self, client, test_activities_db):
        """Test that API returns the test database activities."""
        # Arrange
        expected_activities = set(test_activities_db.keys())

        # Act
        response = client.get("/activities")
        activities = response.json()
        actual_activities = set(activities.keys())

        # Assert
        assert actual_activities == expected_activities

    def test_get_activities_chess_club_has_two_participants(self, client):
        """Test that Chess Club has the expected participants."""
        # Arrange
        expected_participants = {"michael@mergington.edu", "daniel@mergington.edu"}

        # Act
        response = client.get("/activities")
        activities = response.json()
        chess_club = activities["Chess Club"]
        actual_participants = set(chess_club["participants"])

        # Assert
        assert actual_participants == expected_participants

    def test_get_activities_gym_class_has_no_participants(self, client):
        """Test that Gym Class has no participants initially."""
        # Arrange
        expected_participant_count = 0

        # Act
        response = client.get("/activities")
        activities = response.json()
        gym_class = activities["Gym Class"]

        # Assert
        assert len(gym_class["participants"]) == expected_participant_count
