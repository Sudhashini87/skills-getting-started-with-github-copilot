"""Tests for POST /activities/{activity_name}/signup endpoint."""

import pytest


class TestSignupForActivity:
    """Test suite for activity signup endpoint."""

    def test_signup_new_student_returns_200(self, client):
        """Test that signing up a new student returns HTTP 200."""
        # Arrange
        activity_name = "Gym Class"
        email = "newstudent@mergington.edu"
        expected_status_code = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code

    def test_signup_adds_student_to_participants(self, client, app):
        """Test that signup actually adds the student to participants list."""
        # Arrange
        activity_name = "Gym Class"
        email = "newstudent@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert email in app.activities[activity_name]["participants"]

    def test_signup_returns_success_message(self, client):
        """Test that signup returns a success message."""
        # Arrange
        activity_name = "Gym Class"
        email = "newstudent@mergington.edu"
        expected_message_part = "Signed up"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert expected_message_part in data["message"]
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """Test that signing up for a nonexistent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        expected_status_code = 404

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code

    def test_signup_nonexistent_activity_returns_error_detail(self, client):
        """Test that error message is clear when activity not found."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        expected_detail = "Activity not found"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert data["detail"] == expected_detail

    def test_signup_already_registered_student_returns_400(self, client):
        """Test that signing up an already registered student returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        expected_status_code = 400

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code

    def test_signup_already_registered_student_returns_error_detail(self, client):
        """Test that duplicate signup error message is clear."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        expected_detail = "Student already signed up for this activity"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert data["detail"] == expected_detail

    def test_signup_multiple_students_to_same_activity(self, client, app):
        """Test that multiple students can sign up for the same activity."""
        # Arrange
        activity_name = "Gym Class"
        students = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]

        # Act
        for email in students:
            client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )

        # Assert
        activity_participants = app.activities[activity_name]["participants"]
        for email in students:
            assert email in activity_participants

    def test_signup_does_not_affect_other_activities(self, client, app):
        """Test that signing up for one activity doesn't affect others."""
        # Arrange
        activity1 = "Programming Class"
        activity2 = "Chess Club"
        email = "newstudent@mergington.edu"
        original_chess_count = len(app.activities["Chess Club"]["participants"])

        # Act
        client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )

        # Assert
        assert email in app.activities[activity1]["participants"]
        assert email not in app.activities[activity2]["participants"]
        assert len(app.activities["Chess Club"]["participants"]) == original_chess_count

    def test_signup_with_special_characters_in_email(self, client):
        """Test that email with special characters (URL encoding) works."""
        # Arrange
        activity_name = "Gym Class"
        email = "student+special@mergington.edu"
        expected_status_code = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == expected_status_code
