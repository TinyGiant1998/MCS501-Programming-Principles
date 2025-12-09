import pytest
from eventflow.models.event import Event


def test_event_initialization_defaults():
    event = Event(
        event_code="E001",
        name="Annual Meeting",
        organiser_id="ORG123",
        expected_attendees=100,
        required_features=["Projector", "Microphone"],
        duration_hours=2,
        mode="Regular",
    )
    assert event.event_code == "E001"
    assert event.name == "Annual Meeting"
    assert event.organiser_id == "ORG123"
    assert event.expected_attendees == 100
    assert event.required_features == ["Projector", "Microphone"]
    assert event.duration_hours == 2
    assert event.mode == "Regular"
    assert event.dependencies == []


def test_event_with_dependencies():
    event = Event(
        event_code="E002",
        name="Workshop",
        organiser_id="ORG124",
        expected_attendees=50,
        required_features=["Whiteboard"],
        duration_hours=3,
        mode="Block",
        dependencies=["E001"],
    )
    assert event.dependencies == ["E001"]
