from models.notebook import Notebook


def show_menu():
    print("\nTiny Notes Manager")
    print("Type 'add <text>' to create a note")
    print("Type 'list' to show all notes")
    print("Type 'quit' to exit")


def run_cli():
    notebook = Notebook()

    show_menu()

    while True:
        command = input("\n>").strip()

        if command.lower().strip() == "quit":
            print("Goodbye ✌️")
            break

        elif command.lower().startswith("add"):
            text = command[3:].strip()

            if not text:
                print("Error: Note text cannot be empty.")
            else:
                note = notebook.add(text)
                print(f"Added: {note}")

            show_menu()

        elif command.lower().strip() == "list":
            notes = notebook.all()
            if not notes:
                print("No notes yet 😢")
            else:
                for note in notes:
                    print(note)
            show_menu()

        else:
            print("Unknown command. Usage:")
            show_menu()
