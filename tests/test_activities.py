"""
Tests for the GET /activities endpoint.
Validates activity retrieval and response structure.
"""

import pytest


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_contains_all_activities(self, client):
        """Test that all initial activities are present in response."""
        response = client.get("/activities")
        data = response.json()
        
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Swimming",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Robotics Club"
        ]
        
        for activity in expected_activities:
            assert activity in data

    def test_activity_has_required_fields(self, client):
        """Test that each activity has the required structure."""
        response = client.get("/activities")
        data = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"{activity_name} missing {field}"

    def test_participants_is_list(self, client):
        """Test that participants field is always a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"{activity_name} participants is not a list"

    def test_max_participants_is_int(self, client):
        """Test that max_participants field is an integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"{activity_name} max_participants is not an int"

    def test_contains_sample_participants(self, client):
        """Test that activities contain expected initial participant emails."""
        response = client.get("/activities")
        data = response.json()
        
        # Chess Club should have michael@mergington.edu
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        
        # Programming Class should have emma@mergington.edu
        assert "emma@mergington.edu" in data["Programming Class"]["participants"]
