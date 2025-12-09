import pytest
from eventflow.models.organiser import Organiser


class DummyEvent:
    def __init__(self, mode):
        self.mode = mode


def test_organiser_initialization():
    org = Organiser(name="Alice", organiser_id="ORG1")
    assert org.name == "Alice"
    assert org.organiser_id == "ORG1"
    assert org.record == {}


def test_scheduled_events():
    org = Organiser(
        name="Bob",
        organiser_id="ORG2",
        record={"E1": "scheduled", "E2": "completed", "E3": "scheduled"},
    )
    assert set(org.scheduled_events()) == {"E1", "E3"}


def test_block_events_count():
    org = Organiser(
        name="Carol",
        organiser_id="ORG3",
        record={"E1": "scheduled", "E2": "scheduled", "E3": "completed"},
    )
    events_lookup = {
        "E1": DummyEvent("Block"),
        "E2": DummyEvent("Regular"),
        "E3": DummyEvent("Block"),
    }
    assert org.block_events_count(events_lookup) == 1
