import json
from pathlib import Path

from schemas import LearnerState


STATE_FILE = Path("data/learner_state.json")


def save_state(state: LearnerState):
    STATE_FILE.parent.mkdir(exist_ok=True)

    with open(STATE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            state.model_dump(),
            file,
            indent=4
        )


def load_state() -> LearnerState | None:
    if not STATE_FILE.exists():
        return None

    with open(STATE_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return LearnerState(**data)