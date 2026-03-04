"""
Pytest configuration and fixtures for FastAPI tests.
Provides a clean app instance and TestClient for each test.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient with fresh activities data per test.
    This ensures each test starts with a clean slate and doesn't affect others.
    """
    # Reset activities to initial state before each test
    initial_activities = {
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
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for interscholastic play",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Swimming": {
            "description": "Competitive swimming and water sports",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["alex@mergington.edu", "mia@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["charlotte@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in formal debates and develop public speaking skills",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["ethan@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots to compete in STEM competitions",
            "schedule": "Thursdays, 3:30 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        }
    }

    # Clear activities and re-populate with initial state
    activities.clear()
    activities.update(initial_activities)

    # Yield the TestClient for the test
    return TestClient(app)
