from .note import Note


class Notebook:
    """Manage all the note"""

    def __init__(self):
        self._notes = []
        self._next_id = 1

    def add(self, text: str) -> Note:
        new_note = Note(self._next_id, text)
        self._notes.append(new_note)
        self._next_id += 1
        return new_note

    def all(self) -> list[Note]:
        return self._notes
