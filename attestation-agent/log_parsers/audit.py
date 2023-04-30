import re

from log_parsers.base import Event, Parser


class AuditEvent(Event):
    """Event logged by `auditd`"""

    log_file = "/var/log/audit/audit.log"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        for attr, value in kwargs.items():
            if attr not in self.__dict__.keys():
                setattr(self, attr, value)


class AuditParser(Parser):
    """Parser for logs generated by `auditd`"""

    timestamp_re = re.compile(r"\d{10}\.\d{3}")
    event_type_re = re.compile(r"type=(?P<type>[A-Z_]+)")

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)

        # record types which do not correspond to any property
        # parsing method only provide the record type and timestamp
        # as useful properties. For instance, `ANOM_LOGIN_FAILURES`
        # suggests that the number of login failures were exceeded
        # and thus do not require any more details to be parsed.
        self.EVENT_TYPES = {
            "CONFIG_CHANGE": None,
            "KERNEL": None,
            "EXECVE": None,
            "SERVICE_START": self._parse_service_start_stop,
            "SERVICE_STOP": self._parse_service_start_stop,
            "ADD_USER": None,
            "ADD_GROUP": None,
            "ANOM_LOGIN_FAILURES": None,
            "CHGRP_ID": self._parse_chgrp_id,
            "CHUSER_ID": self._parse_chuser_id,
            "USER_LOGIN": self._parse_user_login,
            "USER_ACCT": self._parse_user_acct,
            "USER_AUTH": self._parse_user_auth,
        }

    def _parse_event(self, __event: str) -> Event | None:
        timestamp = int(float(self.timestamp_re.search(__event).group(0)))
        event_type = self.event_type_re.search(__event).group("type")
        if event_type not in self.EVENT_TYPES:
            return None
        if self.EVENT_TYPES[event_type] == None:
            return AuditEvent(timestamp=timestamp, type=event_type, raw_content=__event)
        return self.EVENT_TYPES[event_type](
            __event,
            AuditEvent(timestamp=timestamp, type=event_type, raw_content=__event),
        )

    def _set_attrs(self, event_obj: AuditEvent, patterns: list[str]) -> AuditEvent:
        """
        Compile all patterns, search them in the raw event string and
        set the discovered attributes in the event object.
        """
        for pattern in patterns:
            p_obj = re.compile(pattern)
            try:
                for key, value in (
                    p_obj.search(event_obj.raw_content).groupdict().items()
                ):
                    value = value.strip('"')
                    value = int(value) if value.isdigit() else value
                    setattr(event_obj, key, value)
            except AttributeError:
                # raised if `p_obj.search()` returns None
                pass
        return event_obj

    def _parse_user_auth(self, event_obj: AuditEvent) -> AuditEvent:
        patterns = (
            r"""pid=(?P<pid>[0-9]+)""",
            r"""uid=(?P<uid>[0-9]+)""",
            r"""op=(?P<operation>[A-Za-z_:]+)""",
            r"""grantors=(?P<grantors>[A-Za-z_,]+)""",
            r"""acct=(?P<account>[A-Za-z_"\-]+)""",
            r"""exe=(?P<exec_path>[A-Za-z_/\-"]+)""",
            r"""hostname=(?P<hostname>[A-Za-z0-9_\-\?\.]+)""",
            r"""addr=(?P<address>[a-z0-9\.:]+)""",
            r"""terminal=(?P<terminal>[A-Za-z0-9/\-]+)""",
        )
        return self._set_attrs(event_obj, patterns)

    def _parse_user_acct(self, event_obj: AuditEvent) -> AuditEvent:
        return self._parse_user_auth(event_obj)

    def _parse_user_login(self, event_obj: AuditEvent) -> AuditEvent:
        id_pattern = re.compile(r"id=(?P<user_id>[0-9]+)")
        event_obj.user_id = id_pattern.search(event_obj.raw_content).group("user_id")
        return self._parse_user_auth(event_obj)

    def _parse_chuser_id(self, event_obj: AuditEvent) -> AuditEvent:
        patterns = (
            r"""op=(?P<operation>[a-zA-Z0-9_\-]+)""",
            r"""acct=(?P<account>[a-zA-Z_"\-]+)""",
            r"""exe=(?P<exec_path>[a-zA-Z_"\-/]+)""",
            r"""hostname=(?P<exec_path>[a-zA-Z_"\-\.\?]+)""",
            r"""addr=(?P<address>[a-z0-9\.:]+)""",
            r"""terminal=(?P<terminal>[A-Za-z0-9/\-]+)""",
            r"""old=(?P<old_value>[a-zA-Z0-9_"\-]+)""",
            r"""new=(?P<new_value>[a-zA-Z0-9_"\-]+)""",
        )
        return self._set_attrs(event_obj, patterns)

    def _parse_chgrp_id(self, event_obj: AuditEvent) -> AuditEvent:
        patterns = (
            r"""op=(?P<operation>[a-zA-Z0-9_\-]+)""",
            r"""target=(?P<target>[a-zA-Z0-9_\-"]+)""",
            r"""name=(?P<name>[a-zA-Z0-9_\-"]+)""",
        )
        return self._set_attrs(event_obj, patterns)

    def _parse_service_start_stop(self, event_obj: AuditEvent) -> AuditEvent:
        patterns = (
            r"""pid=(?P<pid>[0-9]+)""",
            r"""uid=(?P<uid>[0-9]+)""",
            r"""unit=(?P<unit>[a-zA-Z\-]+)""",
            r"""comm=(?P<command>[a-zA-Z\-"]+)""",
            r"""exe=(?P<exec_path>[a-zA-Z\-/"]+)""",
        )
        return self._set_attrs(event_obj, patterns)