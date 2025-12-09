from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Room:
    room_code: str
    building: str
    capacity: int
    features: List[str]
    mode: str  # "Block" or "Regular"
    available_slots: Dict[str, list[int]] = field(default_factory=dict)

    def initialize_week(
        self, weekdays=("Mon", "Tue", "Wed", "Thu", "Fri"), start=9, end=18
    ):
        """Populate available_slots with slot indices (integers). Regular slots are hourly integers."""
        # For Regular mode, slots list contains each 1-hour integer from start..end-1
        # For Block mode, we'll still expose hourly indices but scheduling will enforce 3-hour alignment.

        for day in weekdays:
            self.available_slots.setdefault(day, list(range(start, end)))

    def has_features(self, required: list[str]) -> bool:
        return all(
            req.lower() in (f.lower() for f in self.features) for req in required
        )

    def has_capacity(self, attendees: int) -> bool:
        return self.capacity >= attendees

    def is_free(self, weekday: str, start_slot: int, duration_hours: int) -> bool:
        """Check that each required hourly slot exists in available_slots."""
        slots = self.available_slots.get(weekday, [])
        needed = list(range(start_slot, start_slot + duration_hours))
        return all(s in slots for s in needed)

    def reserve(self, weekday: str, start_slot: int, duration_hours: int):
        """Remove reserved slots from availability."""
        needed = set(range(start_slot, start_slot + duration_hours))
        self.available_slots[weekday] = [
            s for s in self.available_slots[weekday] if s not in needed
        ]
