import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data"


def load_json(filename):
    path = BASE / filename
    if not path.exists():
        return {}
    with open(path, "r") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)


def save_json(filename, data):
    path = BASE / filename
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_rooms():
    return load_json("rooms.json")


def save_rooms(data):
    save_json("rooms.json", data)


def load_events():
    return load_json("events.json")


def save_events(data):
    save_json("events.json", data)


def load_organisers():
    return load_json("organisers.json")


def save_organisers(data):
    save_json("organisers.json", data)


def load_schedule():
    return load_json("schedule.json")


def save_schedule(data):
    save_json("schedule.json", data)
