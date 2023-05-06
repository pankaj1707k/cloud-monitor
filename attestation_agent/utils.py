import json
import os
import sys

from attestation_agent.config import SESSION_FILEPATH

from rich.console import Console

# Rich console for prettier output
console = Console()


def load_session() -> dict:
    """
    Load agent state from the last saved session
    """
    data = None

    print("Checking for last session ... ", end="", flush=True)

    # Check if session file exists or not
    if not os.path.isfile(SESSION_FILEPATH):
        print("not found!")
        return

    print("found!\nResuming from last session ... ", end="", flush=True)

    try:
        with open(SESSION_FILEPATH) as fp:
            data = json.load(fp)

        print("done!")
    except (
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError
    ) as exc:
        print(
            (
                f"load_session: error while reading from session file, {exc = }"
                f"\nPlease check the bad config file: {SESSION_FILEPATH}"
            ),
            file=sys.stderr
        )
        return

    return data


def save_session(data: dict):
    """
    Save agent state to a session file
    """
    print("Saving current session ... ", end="", flush=True)

    try:
        with open(SESSION_FILEPATH, "w") as fp:
            json.dump(data, fp)

        print("done!")
    except (
        FileNotFoundError,
        PermissionError,
        json.JSONDecodeError
    ) as exc:
        print(
            f"save_session: error while writing to session file, {exc = }",
            file=sys.stderr
        )