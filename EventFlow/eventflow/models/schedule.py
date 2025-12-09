from dataclasses import dataclass, field
from typing import Dict, Tuple, Optional


@dataclass
class Schedule:
    # mapping event_code with (weekday, room_code, start_slot)
    bookings: Dict[Tuple[str, str, int], str] = field(default_factory=dict)

    def is_slot_free(
        self, weekday: str, room_code: str, start_slot: int, duration_hours: int
    ) -> bool:
        """check that none of the hourly slots overlap existing booking in the same room"""
        for s in range(start_slot, start_slot + duration_hours):
            if (weekday, room_code, s) in self.bookings:
                return False
        return True

    def reserve(
        self,
        weekday: str,
        room_code: str,
        start_slot: int,
        duration_hours: int,
        event_code: str,
    ):
        """Reserve hourly slots for an event (store event_code at each hourly slot key)"""
        for s in range(start_slot, start_slot + duration_hours):
            self.bookings[(weekday, room_code, s)] = event_code

    def all_bookings_for_event(self, event_code: str):
        return [key for key, ev in self.bookings.items() if ev == event_code]

    def preety_display(self):
        out = {}
        for (day, room, slot), ev in sorted(self.bookings.items()):
            out.setdefault((day, room), []).append((slot, ev))
        return out
