from datetime import datetime

from attestation_agent.config import AUTH_LOG

from .base import Event, Parser


class AuthEvent(Event):
    """Event logged in `auth.log`"""

    log_file = AUTH_LOG
    type = "AUTH"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)


class AuthParser(Parser):
    """Parser for authentication logs in `auth.log`"""

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)

    def _parse_event(self) -> Event:
        _event_split = self._data.split()
        _month, _date, _time = _event_split[:3]
        _proc_info = _event_split[4].split("[")

        return AuthEvent(
            timestamp=self._parse_date_time(f"{_month} {_date}", _time),
            hostname=_event_split[3],
            process=_proc_info[0],
            pid=int(_proc_info[1][:-2]) if len(_proc_info) > 1 else None,
            action=" ".join(_event_split[5:]),
            raw_content=self._data,
        )

    def _parse_date_time(self, __date: str, __time: str) -> int:
        _month, _date = __date.split()
        _month = datetime.strptime(_month, "%b").month
        _year = datetime.now().year
        _hour, _minute, _second = map(int, __time.split(":"))
        return int(
            datetime(
                _year, _month, int(_date), _hour, _minute, _second
            ).timestamp()
        )
