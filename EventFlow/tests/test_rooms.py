import pytest

from eventflow.models.room import Room


def make_room():
    return Room(
        room_code="R101",
        building="Main",
        capacity=50,
        features=["Projector", "Whiteboard", "HDMI"],
        mode="Regular",
    )


def test_initialize_week_populates_slots():
    room = make_room()
    room.initialize_week(start=9, end=12)

    assert set(room.available_slots.keys()) == {"Mon", "Tue", "Wed", "Thu", "Fri"}
    assert room.available_slots["Mon"] == [9, 10, 11]


def test_has_features_is_case_insensitive():
    room = make_room()
    assert room.has_features(["projector", "hdmi"]) is True
    assert room.has_features(["projector", "speaker"]) is False


def test_has_capacity_checks_attendees():
    room = make_room()
    assert room.has_capacity(40) is True
    assert room.has_capacity(60) is False


def test_is_free_and_reserve_updates_availability():
    room = make_room()
    room.initialize_week(weekdays=("Mon",), start=9, end=12)

    assert room.is_free("Mon", start_slot=9, duration_hours=2) is True

    room.reserve("Mon", start_slot=9, duration_hours=2)

    assert room.available_slots["Mon"] == [11]
    assert room.is_free("Mon", start_slot=9, duration_hours=1) is False
    assert room.is_free("Mon", start_slot=11, duration_hours=1) is True
