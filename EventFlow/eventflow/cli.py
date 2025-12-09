# eventflow/cli.py
from typing import Dict, List, Tuple
from .models import Room, Event, Organiser, Schedule
from .utils.sort import merge_sort
from .utils.search import linear_search
from eventflow.storage.fileio import load_json, save_json
import json
import sys

# Simple in-memory DB (a real app would use persistent storage)
ROOMS: Dict[str, Room] = {}
EVENTS: Dict[str, Event] = {}
ORGANISERS: Dict[str, Organiser] = {}
SCHEDULE = Schedule()

WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]


# -------------------------
# Helpers
# -------------------------
def load_sample_data():
    # create sample rooms if none exist
    if load_json("rooms.json") is None:
        r1 = Room("B1.201", "B1", 60, ["projector", "accessible"], "Regular")
        r2 = Room("B1.310", "B1", 28, ["lab", "projector"], "Block")
        r3 = Room("C2.105", "C2", 120, ["projector", "stage", "accessible"], "Regular")
        for r in (r1, r2, r3):
            r.initialize_week(weekdays=WEEKDAYS)
            ROOMS[r.room_code] = r
        save_json("rooms.json", [r.__dict__ for r in ROOMS.values()])

    loaded = load_json("rooms.json")
    if loaded:
        # recreate objects
        ROOMS.clear()
        for r in loaded:
            room = Room(
                r["room_code"],
                r["building"],
                r["capacity"],
                r["features"],
                r["mode"],
                r.get("available_slots", {}),
            )
            # If available_slots empty, initialize defaults:
            if not room.available_slots:
                room.initialize_week(weekdays=WEEKDAYS)
            ROOMS[room.room_code] = room


def save_state():
    save_json("rooms.json", [r.__dict__ for r in ROOMS.values()])
    save_json("events.json", [e.__dict__ for e in EVENTS.values()])
    save_json("schedule.json", {f"{k}": v for k, v in SCHEDULE.bookings.items()})
    save_json("organisers.json", {k: o.record for k, o in ORGANISERS.items()})


def print_rooms():
    print("\nRooms:")
    for r in ROOMS.values():
        print(f"{r.room_code} — {r.mode} — cap={r.capacity} — features={r.features}")


def register_organiser():
    name = input("Name: ").strip()
    oid = input("Organiser ID: ").strip()
    if oid in ORGANISERS:
        print("Organiser exists.")
        return
    ORGANISERS[oid] = Organiser(name, oid)
    print(f"Organiser profile created: {name} (ID: {oid})")


def add_room():
    code = input("Room Code: ").strip()
    if code in ROOMS:
        print("Room already exists.")
        return
    building = input("Building: ").strip()
    cap = int(input("Capacity: ").strip())
    features = [f.strip() for f in input("Features (comma): ").split(",") if f.strip()]
    mode = input("Mode (Block/Regular): ").strip().capitalize()
    room = Room(code, building, cap, features, mode)
    room.initialize_week(weekdays=WEEKDAYS)
    ROOMS[code] = room
    print(f"Room '{code}' added ({mode}, cap={cap}, features={features}).")


def add_event_template():
    code = input("Event Code: ").strip()
    if code in EVENTS:
        print("Event exists.")
        return
    name = input("Name: ").strip()
    org = input("Organiser ID: ").strip()
    if org not in ORGANISERS:
        print("Unknown organiser - create organiser first.")
        return
    attendees = int(input("Expected Attendees: ").strip())
    req_feats = [
        f.strip() for f in input("Required Features (comma): ").split(",") if f.strip()
    ]
    dur = int(input("Duration (hours): ").strip())
    mode = input("Mode (Block/Regular): ").strip().capitalize()
    deps = [d.strip() for d in input("Dependencies (comma): ").split(",") if d.strip()]
    ev = Event(code, name, org, attendees, req_feats, dur, mode, deps)
    EVENTS[code] = ev
    print(f"Event '{code} - {name}' created for organiser {org}.")


def search_menu():
    t = input("Search for (room/event): ").strip().lower()
    q = input("Code: ").strip()
    if t.startswith("r"):
        r = ROOMS.get(q)
        if r:
            print(
                f"Found Room: {r.room_code} — cap={r.capacity} — features={r.features}"
            )
        else:
            print("Not found.")
    else:
        e = EVENTS.get(q)
        if e:
            print(
                f"Found Event: {e.event_code} — {e.name} — {e.duration_hours}h — mode={e.mode}"
            )
        else:
            print("Not found.")


def sort_menu():
    target = input("Sort target (events/rooms): ").strip().lower()
    keyname = input(
        "Sort by (e.g., expected_attendees, duration_hours, room_code): "
    ).strip()
    if target.startswith("e"):
        arr = list(EVENTS.values())
        sorted_arr = merge_sort(arr, key=lambda ev: getattr(ev, keyname))
        print("Events sorted:")
        for ev in sorted_arr:
            print(f"{ev.event_code} — {ev.name} — {getattr(ev, keyname)}")
    else:
        arr = list(ROOMS.values())
        sorted_arr = merge_sort(arr, key=lambda r: getattr(r, keyname))
        for r in sorted_arr:
            print(f"{r.room_code} — {getattr(r, keyname)}")


# -------------------------
# Scheduling logic (Menu 7)
# -------------------------


def dependencies_satisfied(
    event: Event, day: str, start_slot: int
) -> tuple[bool, List[str]]:
    """
    Recursively verify that all dependencies for `event` are already scheduled earlier in the week.
    Returns (ok, missing_list).
    """
    missing = []
    # For each dependency, check scheduled slots in SCHEDULE
    for dep_code in event.dependencies:
        # find bookings for dep_code
        found = SCHEDULE.all_bookings_for_event(dep_code)
        if not found:
            missing.append(dep_code)
            continue
        # check that at least one booked slot is before (day,start_slot)
        # ordering: day index + slot numeric comparison
        day_idx = WEEKDAYS.index(day)
        dep_ok = False
        for d, room, slot in found:
            d_idx = WEEKDAYS.index(d)
            if d_idx < day_idx or (d_idx == day_idx and slot < start_slot):
                dep_ok = True
                break
        if not dep_ok:
            missing.append(dep_code)
        else:
            # recursively check dependencies (guarded by missing)
            dep_event = EVENTS.get(dep_code)
            if dep_event:
                ok, more_missing = dependencies_satisfied(dep_event, d, slot)
                if not ok:
                    missing.extend(more_missing)
    return (len(missing) == 0), list(set(missing))


def plan_weekly_schedule():
    organiser_id = input("Organiser ID: ").strip()
    org = ORGANISERS.get(organiser_id)
    if not org:
        print("Unknown organiser.")
        return
    print(
        f"Organiser {organiser_id} — Block events scheduled this week: {org.block_events_count(EVENTS)}"
    )
    ev_codes = input("Select events to schedule (comma separated event codes): ").split(
        ","
    )
    ev_codes = [c.strip() for c in ev_codes if c.strip()]
    for evc in ev_codes:
        ev = EVENTS.get(evc)
        if not ev:
            print(f"Unknown event {evc}")
            continue
        # duplicate check
        if evc in org.scheduled_events():
            print(f"Cannot schedule {evc}: already scheduled for this organiser.")
            continue
        # block cap enforcement
        if ev.mode.lower() == "block" and org.block_events_count(EVENTS) >= 2:
            print(f"Cannot schedule {evc}: organiser exceeds weekly Block limit (2).")
            continue
        # ask preferred day/slot
        day = input(f"Preferred weekday for {evc} (Mon..Fri): ").strip().capitalize()
        if day not in WEEKDAYS:
            print("Invalid weekday.")
            continue
        start = int(input("Start slot (hour, e.g., 9 for 9:00): ").strip())
        # Validate mode-specific constraints
        if ev.mode.lower() == "block":
            if ev.duration_hours % 3 != 0:
                print("Block events must have duration multiple of 3.")
                continue
            # ensure start aligns to 3-hour block (e.g., 9,12,15)
            if (start - 9) % 3 != 0:
                print("Block start must align to 3-hour blocks (9,12,15...).")
                continue
        # find candidate rooms meeting features and capacity and available
        candidates = []
        for room in ROOMS.values():
            if not room.has_capacity(ev.expected_attendees):
                continue
            if not room.has_features(ev.required_features):
                continue
            # check schedule (global) and room availability
            if room.is_free(day, start, ev.duration_hours) and SCHEDULE.is_slot_free(
                day, room.room_code, start, ev.duration_hours
            ):
                candidates.append(room)
        if not candidates:
            print(f"No candidate rooms available for {evc}.")
            continue
        print(f"Candidate rooms: {[r.room_code for r in candidates]}")
        chosen = input("Preferred room code (or blank to pick first): ").strip()
        if chosen == "":
            chosen_room = candidates[0]
        else:
            chosen_room = ROOMS.get(chosen)
            if not chosen_room:
                print("Invalid room choice.")
                continue
        # dependencies
        ok, missing = dependencies_satisfied(ev, day, start)
        if not ok:
            print(f"Cannot schedule {evc}: missing dependencies {missing}")
            continue
        # reserve in schedule and in room
        SCHEDULE.reserve(
            day, chosen_room.room_code, start, ev.duration_hours, ev.event_code
        )
        chosen_room.reserve(day, start, ev.duration_hours)
        org.record[ev.event_code] = "scheduled"
        print(
            f"Assigned: {ev.event_code} @ {day} {start}:00 in {chosen_room.room_code} ✔"
        )
    print("Scheduling done for requested events.")


# -------------------------
# CLI main
# -------------------------
def main_loop():
    load_sample_data()
    while True:
        print("\n========== EventFlow — Campus Scheduler ==========")
        print("1. Register Organiser")
        print("2. Add a Room")
        print("3. Add an Event Template")
        print("4. View All Rooms")
        print("5. Search (Event or Room)")
        print("6. Sort (Events or Rooms)")
        print("7. Plan Weekly Schedule (assign events)")
        print("8. Save Schedule to File")
        print("9. Load Schedule from File")
        print("10. View Organiser Record")
        print("11. Exit")
        choice = input("Enter your choice (1–11): ").strip()
        if choice == "1":
            register_organiser()
        elif choice == "2":
            add_room()
        elif choice == "3":
            add_event_template()
        elif choice == "4":
            print_rooms()
        elif choice == "5":
            search_menu()
        elif choice == "6":
            sort_menu()
        elif choice == "7":
            plan_weekly_schedule()
        elif choice == "8":
            save_state()
            print("Saved.")
        elif choice == "9":
            print("Load not implemented fully; restart to reload sample data.")
        elif choice == "10":
            oid = input("Organiser ID: ").strip()
            o = ORGANISERS.get(oid)
            if o:
                print(f"Record for {o.name}: {o.record}")
            else:
                print("Not found.")
        elif choice == "11":
            save_state()
            print("Exiting. Bye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main_loop()
