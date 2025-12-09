# Copilot Instructions

- **Repo scope**: Collection of small Python assignments; nothing is packaged or installed. Run tools from each project root so imports like `eventflow` or `gradebook_lite` resolve via `PYTHONPATH`.
- **Python version/deps**: Pure stdlib; no external dependencies.

- **EventFlow (event scheduling)**: Live under `EventFlow/eventflow/`. Core dataclasses: `Room`, `Event`, `Organiser`, `Schedule` in `models/`. `Room` tracks hourly availability per weekday; `reserve` removes booked slots; `has_features` is case-insensitive. `Schedule` stores bookings keyed by `(weekday, room_code, slot)` and can pretty-display grouped slots.
- **EventFlow scheduler**: `scheduler/validator.py` enforces capacity, feature, free-time, organiser block-mode limit (max 2 block events), and dependency ordering. `scheduler/planner.py` orchestrates validation then reserves room and assigns schedule/organiser; note it calls `schedule.assign`, but `Schedule` only implements `reserve` (existing mismatch).
- **EventFlow storage**: `storage/fileio.py` reads/writes JSON under `eventflow/data/`. Files currently empty; `load_json` returns `{}` so `cli.load_sample_data` never seeds sample rooms (condition checks `is None`). Expect to seed data manually or adjust loader.
- **EventFlow CLI**: `eventflow/cli.py` holds in-memory dictionaries (`ROOMS`, `EVENTS`, `ORGANISERS`, `SCHEDULE`), helper `load_sample_data`, state persistence via `save_state()`, and a simple `print_rooms()`. `main.py` is empty; CLI is unfinished and untested.
- **EventFlow utils**: `utils/search.py` provides `linear_search` and `binary_search`; `utils/sort.py` implements `merge_sort`. Tests exercise these helpers directly.
- **EventFlow tests**: Under `EventFlow/tests/`; cover model behaviors, schedule booking logic, and search/sort. No coverage for CLI/planner, so be cautious changing them.
- **EventFlow test command**: From repo root, `PYTHONPATH=EventFlow pytest EventFlow/tests` (macOS zsh). Alternatively `cd EventFlow && PYTHONPATH=. pytest`.

- **Week 3 – Gradebook Lite**: `Week 3/gradebook_lite/core.py` exposes `validates_scores`, `mean`, `min_max`, `letter_grade`; validates scores are numeric 0–100 and raises `ValueError` otherwise. `gradebook_lite/cli.py` is an interactive loop using these helpers.
- **Gradebook tests**: `Week 3/tests/test_core.py`; run with `PYTHONPATH="Week 3" pytest "Week 3/tests"`.

- **Week5 – Tiny Notes**: `Week5/models/note.py` and `notebook.py` hold a minimal in-memory note list; IDs auto-increment. CLI at `Week5/cli/app.py` reads `add <text>` and `list`; no persistence.
- **Week5 tests**: `Week5/tests/test_notebook.py`; run with `PYTHONPATH=Week5 pytest Week5/tests`.

- **Data/IO expectations**: Everything is in-memory unless `storage/fileio.py` writes JSON. Data files are empty; creating or adjusting JSON structure is necessary before scheduling flows work end-to-end.
- **Conventions**: Prefer dataclasses for simple models; availability and bookings use plain dicts with primitive keys. Case-insensitive feature checks; durations are integer hours.
- **Edge awareness**: Missing seeding and Schedule/Planner method mismatch are known rough edges; avoid assuming CLI works without patching those.
- **General workflow**: Work per subproject; set `PYTHONPATH` accordingly; use `pytest` for feedback. Keep file paths quoted when spaces appear (e.g., `Week 3`).
