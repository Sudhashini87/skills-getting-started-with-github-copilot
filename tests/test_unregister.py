"""Tests for DELETE /activities/{activity_name}/unregister endpoint."""

import pytest


class TestUnregisterFromActivity:
    """Test suite for activity unregister endpoint."""

    def test_unregister_existing_participant_returns_200(self, client):
        """Test that unregistering an existing participant returns HTTP 200."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        expected_status_code = 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code

    def test_unregister_removes_participant_from_list(self, client, app):
        """Test that unregistering actually removes the student from participants."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert email not in app.activities[activity_name]["participants"]

    def test_unregister_returns_success_message(self, client):
        """Test that unregister returns a success message."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        expected_message_part = "Unregistered"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert expected_message_part in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from a nonexistent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        expected_status_code = 404

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code

    def test_unregister_nonexistent_activity_returns_error_detail(self, client):
        """Test that error message is clear when activity not found."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        expected_detail = "Activity not found"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert data["detail"] == expected_detail

    def test_unregister_non_participant_returns_400(self, client):
        """Test that unregistering a non-participant returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "nonparticipant@mergington.edu"  # Not in Chess Club
        expected_status_code = 400

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code

    def test_unregister_non_participant_returns_error_detail(self, client):
        """Test that non-participant error message is clear."""
        # Arrange
        activity_name = "Chess Club"
        email = "nonparticipant@mergington.edu"
        expected_detail = "Student is not signed up for this activity"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert data["detail"] == expected_detail

    def test_unregister_does_not_affect_other_participants(self, client, app):
        """Test that unregistering one participant doesn't affect others."""
        # Arrange
        activity_name = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        other_email = "daniel@mergington.edu"
        original_count = len(app.activities[activity_name]["participants"])

        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email_to_remove}
        )

        # Assert
        assert email_to_remove not in app.activities[activity_name]["participants"]
        assert other_email in app.activities[activity_name]["participants"]
        assert len(app.activities[activity_name]["participants"]) == original_count - 1

    def test_unregister_does_not_affect_other_activities(self, client, app):
        """Test that unregistering from one activity doesn't affect others."""
        # Arrange
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        email = "michael@mergington.edu"
        original_programming_count = len(app.activities[activity2]["participants"])

        # Act
        client.delete(
            f"/activities/{activity1}/unregister",
            params={"email": email}
        )

        # Assert
        assert email not in app.activities[activity1]["participants"]
        assert len(app.activities[activity2]["participants"]) == original_programming_count

    def test_unregister_then_signup_again(self, client, app):
        """Test that a student can unregister and then sign up again."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act: Unregister
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        assert email not in app.activities[activity_name]["participants"]

        # Act: Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert email in app.activities[activity_name]["participants"]

    def test_unregister_decreases_participant_count(self, client, app):
        """Test that unregistering decreases the participant count."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        original_count = len(app.activities[activity_name]["participants"])

        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        new_count = len(app.activities[activity_name]["participants"])

        # Assert
        assert new_count == original_count - 1
