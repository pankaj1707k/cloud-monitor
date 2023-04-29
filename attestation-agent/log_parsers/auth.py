import datetime

from log_parsers.base import Event, Parser
from log_parsers.utils import MONTHS


class AuthEvent(Event):
    """Event logged in `auth.log`"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class AuthParser(Parser):
    """Parser for authentication logs in `auth.log`"""

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)

    def _parse_event(self, __event: str) -> Event:
        _event_split = __event.split()
        _month, _date, _time = _event_split[:3]
        _proc_info = _event_split[4].split("[")

        return AuthEvent(
            date=self._parse_date(f"{_month} {_date}"),
            time=self._parse_time(_time),
            hostname=_event_split[3],
            process=_proc_info[0],
            pid=int(_proc_info[1][:-2]),
            action=" ".join(_event_split[5:]),
        )

    def _parse_date(self, __date: str) -> datetime.date:
        _month, _date = __date.split()
        _year = datetime.datetime.now().year
        return datetime.date(_year, MONTHS[_month.lower()], int(_date))

    def _parse_time(self, __time: str) -> datetime.time:
        _hour, _minute, _second = map(int, __time.split(":"))
        return datetime.time(_hour, _minute, _second)
