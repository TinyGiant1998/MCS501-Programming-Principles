from models.notebook import Notebook


def test_add_and_list():
    nb = Notebook()

    nb.add("buy milk")
    nb.add("study python")

    notes = nb.all()

    assert len(notes) == 2
    assert notes[0].text == "buy milk"
    assert notes[1].id == 2
