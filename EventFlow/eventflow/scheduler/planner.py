from dataclasses import dataclass, field
from .validator import Validator, ValidationError


@dataclass
class Planner:
    schedule: any  # type: ignore
    validator: Validator = field(default_factory=Validator)

    def plan_event(self, event, organiser, room, weekday, start_slot):
        duration = event.duration_hours

        # Validation checks
        self.validator.check_capacity(room, event)
        self.validator.check_features(room, event)
        self.validator.check_time_free(room, weekday, start_slot, duration)
        self.validator.check_block_limit(organiser, event)
        self.validator.check_dependencies(self.schedule, event)

        # Reserve the room
        room.reserve(weekday, start_slot, duration)

        # Add to schedule mapping
        self.schedule.assign(weekday, room.room_code, start_slot, event.event_code)

        # Mark organiser record
        organiser.events_scheduled.append(event.event_code)

        return True
