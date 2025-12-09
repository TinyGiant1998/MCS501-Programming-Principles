from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Organiser:
    name: str
    organiser_id: str
    record: Dict[str, str] = field(default_factory=dict)
    # record will map event_code to status ("scheduled", "completed", "cancelled")

    def scheduled_events(self) -> List[str]:
        return [code for code, status in self.record.items() if status == "scheduled"]

    def block_events_count(self, events_lookup) -> int:
        """Count scheduled block-mode events for this organiser in this week.
        events_lookup: dict event_code -> Event (to look up mode)"""

        cnt = 0
        for code in self.scheduled_events():
            ev = events_lookup.get(code)
            if ev and ev.mode.lower() == "block":
                cnt += 1
        return cnt
