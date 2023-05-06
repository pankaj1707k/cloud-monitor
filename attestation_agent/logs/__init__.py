import os
import sys
import time
from abc import ABC, abstractmethod
from collections import deque
from threading import Lock

from rich.table import Table

from attestation_agent.utils import console


class Event(ABC):
    """
    Abstract class defining the general structure of a logged event.
    Inherit this class to prepare specific event structures for various logs.

    Attributes:
    - `timestamp`: `int`
    - `hostname`: `str`
    - `process`: `str`
    - `pid`: `int`
    - `action`: `str`
    - `raw_content`: `str`
    """

    def __init__(self, **kwargs) -> None:
        _defaults = {
            "timestamp": None,
            "action": None,
            "raw_content": None,
        }

        for attr, def_value in _defaults.items():
            setattr(self, attr, kwargs.get(attr, def_value))

    def __str__(self) -> str:
        _obj_state = [f"{attr}: {value}" for attr, value in self.__dict__.items()]
        return "{\n\t" + "\n\t".join(_obj_state) + "}"


class Parser(ABC):
    """
    Base class for all parsers. Initialization requires the absolute path
    to the log file to be parsed.
    """

    def __init__(self, filepath: str) -> None:
        # Raise error if the log file doesn't exist
        if not os.path.isfile(filepath):
            raise ParseError(msg=f"Log file '{self.filepath}' does not exist.")

        # Store the state of parser
        self._running: bool = True

        # Absolute path of the log file
        self.filepath: str = filepath

        # Open the file and keep it open during the whole runtime
        self.file = open(self.filepath, "rb")

        # Starting byte index of the log file.
        # Keeps track of how much of the file has been read.
        self._pos: int = 0
        self._line: int = 0

        # Parser state while parsing, for error handling
        self._data: str = None

        # Create a mutex lock used to pause the parser to flush generated events
        self.lock: Lock = Lock()

        # Facilitates faster removal from the front of queue after
        # an event has been analyzed. Removal is required to prevent
        # high memory consumption when machine runs for longer durations.
        self.events: deque[Event] = deque()

    def flush(self) -> list[Event]:
        """
        Return the generated events and clear the current list
        """
        events = self.events.copy()
        self.events.clear()
        return events

    def parse_line(self) -> bool:
        """
        Read a line from the log file, parse it and add it to the event queue.
        """
        # Skip the parsed bytes, read a line and store
        # the current cursor position in the file
        self.file.seek(self._pos)
        line = self.file.readline()
        self._pos = self.file.tell()

        # Check if there is no data, if we have reached the EOF
        if line is None or len(line) == 0:
            return False

        # Convert to UTF-8 and parse the line
        self._data = line.decode("utf-8").strip()
        event = self._parse_event()

        if event is not None:
            self.events.append(event)

        return True

    def run(self) -> None:
        """Run the parser."""
        # While the parser can run, it will read
        # and parse the log files to generate events
        while self._running:
            # Whether to wait for next line or not (when EOF is reached)
            wait_for_nextline = False

            with self.lock:
                # Try to parse a line and catch any error
                # and re-raise it as a `ParseError`
                try:
                    wait_for_nextline = not self.parse_line()
                except Exception as exc:
                    print(
                        ParseError(
                            msg="error while parsing line",
                            line=self._line,
                            position=self._pos,
                            data=self._data,
                            exc=exc
                        ),
                        file=sys.stderr
                    )
                finally:
                    # Keep track of the number of lines parsed so far
                    self._line += 1

            # Check if we have reached the EOF of the log file
            if wait_for_nextline:
                # The below sleep should allow any new content to appear
                # and the main program to acquire `self.lock` to read `self.events`
                time.sleep(1)

    def get_state(self):
        """
        Return a `dict` of the state variables
        """
        return {
            "line": self._line,
            "position": self._pos,
        }

    def set_state(self, state={}):
        """
        Set the state variables of the parser: _line, _pos
        """
        with self.lock:
            self._line = state.get("line", self._line)
            self._pos = state.get("position", self._pos)

    def stop(self):
        """
        Set the parser state to stopped
        """
        self._running = False

    @abstractmethod
    def _parse_event(self) -> Event:
        """
        Parse the event string and return an instance of `Event`.
        """
        raise NotImplementedError("Must implement event parsing function")


class ParseError(Exception):
    """
    Generic failure of a parser.
    """

    def __init__(self, msg="generic parse error", **kwargs):
        super().__init__(msg)
        self.kwargs = kwargs

    def __str__(self) -> str:
        with console.capture() as capture:
            table = Table(
                *self.kwargs.keys(),
                title="ParseError"
            )

            table.add_row(*map(lambda attr: str(attr), self.kwargs.values()))
            console.print(table)

        return capture.get()
