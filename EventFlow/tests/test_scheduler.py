import pytest
from eventflow.models.schedule import Schedule


def test_is_slot_free_and_reserve():
    sched = Schedule()
    # Initially, all slots are free
    assert sched.is_slot_free("Mon", "R101", 9, 2) is True

    # Reserve 9-10 for E1
    sched.reserve("Mon", "R101", 9, 2, "E1")
    # Now 9 and 10 are booked
    assert sched.is_slot_free("Mon", "R101", 9, 1) is False
    assert sched.is_slot_free("Mon", "R101", 10, 1) is False
    assert sched.is_slot_free("Mon", "R101", 11, 1) is True


def test_all_bookings_for_event():
    sched = Schedule()
    sched.reserve("Tue", "R102", 10, 2, "E2")
    sched.reserve("Tue", "R102", 12, 1, "E3")
    keys = sched.all_bookings_for_event("E2")
    assert ("Tue", "R102", 10) in keys
    assert ("Tue", "R102", 11) in keys
    assert ("Tue", "R102", 12) not in keys


def test_preety_display():
    sched = Schedule()
    sched.reserve("Wed", "R201", 8, 2, "E4")
    display = sched.preety_display()
    # Should group by (day, room)
    assert ("Wed", "R201") in display
    slots = display[("Wed", "R201")]
    assert (8, "E4") in slots
    assert (9, "E4") in slots
