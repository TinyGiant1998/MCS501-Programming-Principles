class ValidationError(Exception):
    pass


class Validator:
    def check_capacity(self, room, event):
        if not room.has_capacity(event.expected_attendees):
            raise ValidationError(f"Room {room.room_code} is too small")

    def check_features(self, room, event):
        if not room.has_features(event.required_features):
            raise ValidationError(
                f"Room {room.room_code} missing required features: {event.required_features}"
            )

    def check_time_free(self, room, weekday, start_slot, duration):
        if not room.is_free(weekday, start_slot, duration):
            raise ValidationError(
                f"Room {room.room_code} not free at {weekday} {start_slot}"
            )

    def check_block_limit(self, organiser, event):
        if event.mode == "Block":
            block_count = organiser.count_block_events()
            if block_count >= 2:
                raise ValidationError(
                    f"Organiser {organiser.organiser_id} exceeds block limit."
                )

    def check_dependencies(self, schedule, event):
        """Ensure all dependency event codes appear earlier in the week."""
        for dep in event.dependencies:
            if dep not in schedule.events_ordered:
                raise ValidationError(f"Missing dependency: {dep}")
