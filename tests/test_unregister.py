"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.
Validates student unregistration functionality and error handling.
"""

import pytest


class TestUnregisterFromActivity:
    """Test suite for removing a student from an activity."""

    def test_unregister_existing_participant_returns_200(self, client):
        """Test that removing an existing participant returns 200."""
        # michael@mergington.edu is already in Chess Club
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        assert response.status_code == 200

    def test_unregister_existing_participant_returns_message(self, client):
        """Test that unregister returns a confirmation message."""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "michael@mergington.edu"}
        )
        data = response.json()
        assert "message" in data
        assert "michael@mergington.edu" in data["message"]
        assert "Chess Club" in data["message"]

    def test_unregister_removes_participant_from_list(self, client):
        """Test that unregister actually removes the student from activity."""
        email = "michael@mergington.edu"
        
        # Verify they're in the list before deletion
        response = client.get("/activities")
        assert email in response.json()["Chess Club"]["participants"]
        
        # Remove them
        client.delete("/activities/Chess Club/signup", params={"email": email})
        
        # Verify they're not in the list after deletion
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]

    def test_unregister_non_existent_participant_returns_404(self, client):
        """Test that unregistering a student not in activity returns 404."""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "notregistered@mergington.edu"}
        )
        assert response.status_code == 404

    def test_unregister_non_existent_participant_error_message(self, client):
        """Test that non-existent participant returns appropriate error message."""
        response = client.delete(
            "/activities/Chess Club/signup",
            params={"email": "notregistered@mergington.edu"}
        )
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregistering from non-existent activity returns 404."""
        response = client.delete(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404

    def test_unregister_invalid_activity_error_message(self, client):
        """Test that non-existent activity returns appropriate error message."""
        response = client.delete(
            "/activities/Nonexistent Activity/signup",
            params={"email": "student@mergington.edu"}
        )
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_then_signup_again(self, client):
        """Test that a student can unregister and then re-register."""
        email = "flexible@mergington.edu"
        activity = "Chess Club"
        
        # Sign up
        response1 = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response1.status_code == 200
        
        # Unregister
        response2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
        assert response2.status_code == 200
        
        # Sign up again
        response3 = client.post(f"/activities/{activity}/signup", params={"email": email})
        assert response3.status_code == 200
        
        # Verify they're registered
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

    def test_unregister_multiple_participants(self, client):
        """Test removing multiple participants from an activity."""
        # Chess Club has michael@mergington.edu and daniel@mergington.edu
        emails = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        for email in emails:
            response = client.delete(
                "/activities/Chess Club/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify both are removed
        response = client.get("/activities")
        participants = response.json()["Chess Club"]["participants"]
        for email in emails:
            assert email not in participants

    def test_unregister_preserves_other_participants(self, client):
        """Test that unregistering one student doesn't affect others."""
        # Chess Club has michael@mergington.edu and daniel@mergington.edu
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        # Remove one
        client.delete("/activities/Chess Club/signup", params={"email": email_to_remove})
        
        # Verify the other is still there
        response = client.get("/activities")
        participants = response.json()["Chess Club"]["participants"]
        assert email_to_remove not in participants
        assert email_to_keep in participants

    def test_unregister_from_one_activity_doesnt_affect_others(self, client):
        """Test that unregistering from one activity doesn't affect other activities."""
        email = "emma@mergington.edu"  # In Programming Class
        
        # Add to Chess Club too
        client.post("/activities/Chess Club/signup", params={"email": email})
        
        # Remove from Chess Club
        client.delete("/activities/Chess Club/signup", params={"email": email})
        
        # Verify still in Programming Class
        response = client.get("/activities")
        data = response.json()
        assert email not in data["Chess Club"]["participants"]
        assert email in data["Programming Class"]["participants"]
