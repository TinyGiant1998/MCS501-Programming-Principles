from dataclasses import dataclass, field
from typing import List


@dataclass
class Event:
    event_code: str
    name: str
    organiser_id: str
    expected_attendees: int
    required_features: List[str]
    duration_hours: int
    mode: str  # "Block" or "Regular"
    dependencies: List[str] = field(default_factory=list)
