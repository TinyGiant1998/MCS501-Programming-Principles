class Note:
    """A simple note module containing id and text"""

    def __init__(self, note_id: int, text: str):
        self.id = note_id
        self.text = text

    def __str__(self):
        return f"[{self.id}] - {self.text}"
