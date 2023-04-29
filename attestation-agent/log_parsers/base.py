import datetime
import os
import sys
from abc import ABCMeta, abstractmethod
from collections import deque


class Event:
    """
    Abstract class defining the general structure of a logged event.
    Inherit this class to prepare specific event structures for various logs.

    Attributes:
    - `date`: `datetime.date`
    - `time`: `datetime.time`
    - `hostname`: `str`
    - `process`: `str`
    - `pid`: `int`
    - `action`: `str`
    """

    def __init__(self, **kwargs) -> None:
        _defaults = {
            "date": None,
            "time": None,
            "hostname": os.uname().nodename,
            "process": None,
            "pid": None,
            "action": None,
        }

        for attr, def_value in _defaults.items():
            setattr(self, attr, kwargs.get(attr, def_value))

    def __str__(self) -> str:
        _obj_state = [f"{attr}: {value}" for attr, value in self.__dict__.items()]
        return "{\n\t" + "\n\t".join(_obj_state) + "}"


class Parser(ABCMeta):
    """
    Base class for all parsers. Initialization requires the absolute path
    to the log file to be parsed.
    """

    def __init__(self, filepath: str) -> None:
        # Absolute path of the log file
        self.filepath: str = filepath

        # Starting byte index of the log file.
        # Keeps track of how much of the file has been read.
        self._pos: int = 0

        # Facilitates faster removal from the front of queue after
        # an event has been analyzed. Removal is required to prevent
        # high memory consumption when machine runs for longer durations.
        self.events: deque[Event] = deque()

    def read_file(self) -> None:
        """
        Read the log file, parse events and add them to the event queue.
        """
        try:
            with open(self.filepath, "rb") as logfile:
                _ = logfile.seek(self._pos)
                _data = logfile.readlines()
                self._pos = logfile.tell()
        except FileNotFoundError:
            print(f"{self.filepath} does not exist...\nAbort.", file=sys.stderr)
            sys.exit(1)

        _data = list(map(lambda l: l.decode("utf-8").strip(), _data))
        self.events.extend(list(map(lambda e: self._parse_event(e), _data)))

    @abstractmethod
    def run(self) -> None:
        """Run the parser."""

    @abstractmethod
    def _parse_event(self, __event: str) -> Event:
        """
        Parse the event string and return an instance of `Event`.
        """

    @abstractmethod
    def _parse_date(self, __date: str) -> datetime.date:
        """
        Parse date in string format and return a `datetime.date` instance.
        """

    @abstractmethod
    def _parse_time(self, __time: str) -> datetime.time:
        """
        Parse time in string format and return a `datetime.time` instance.
        """
