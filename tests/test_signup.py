"""
Tests for the POST /activities/{activity_name}/signup endpoint.
Validates student signup functionality and error handling.
"""

import pytest


class TestSignupForActivity:
    """Test suite for signing up a student for an activity."""

    def test_signup_new_student_returns_200(self, client):
        """Test that a new student can successfully sign up for an activity."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        assert response.status_code == 200

    def test_signup_new_student_returns_success_message(self, client):
        """Test that signup returns a confirmation message."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "newstudent@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant_to_list(self, client):
        """Test that signup actually adds the student to the activity."""
        email = "newstudent@mergington.edu"
        
        # Sign up
        client.post("/activities/Chess Club/signup", params={"email": email})
        
        # Verify participant was added
        response = client.get("/activities")
        data = response.json()
        assert email in data["Chess Club"]["participants"]

    def test_signup_already_registered_returns_400(self, client):
        """Test that signing up twice returns a 400 error."""
        email = "duplicate@mergington.edu"
        
        # First signup (should succeed)
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second signup with same email (should fail)
        response2 = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        assert response2.status_code == 400

    def test_signup_already_registered_error_message(self, client):
        """Test that duplicate signup returns appropriate error message."""
        email = "duplicate@mergington.edu"
        
        # First signup
        client.post("/activities/Chess Club/signup", params={"email": email})
        
        # Second signup
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": email}
        )
        data = response.json()
        assert "detail" in data
        assert "already" in data["detail"].lower()

    def test_signup_existing_participant_cannot_signup_again(self, client):
        """Test that an already registered participant cannot sign up again."""
        # michael@mergington.edu is already in Chess Club
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 400

    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signing up for non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404

    def test_signup_invalid_activity_error_message(self, client):
        """Test that non-existent activity returns appropriate error message."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_multiple_students_same_activity(self, client):
        """Test that multiple different students can sign up for the same activity."""
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        for email in emails:
            response = client.post(
                "/activities/Chess Club/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all were added
        response = client.get("/activities")
        data = response.json()
        for email in emails:
            assert email in data["Chess Club"]["participants"]

    def test_signup_same_student_different_activities(self, client):
        """Test that the same student can sign up for different activities."""
        email = "versatile@mergington.edu"
        activities = ["Chess Club", "Programming Class", "Gym Class"]
        
        for activity in activities:
            response = client.post(
                f"/activities/{activity}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify student is in all activities
        response = client.get("/activities")
        data = response.json()
        for activity in activities:
            assert email in data[activity]["participants"]
