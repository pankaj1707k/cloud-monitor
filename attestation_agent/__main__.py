"""
Main driver code that runs the agent.
This file is autorun on `python attestation_agent` command.
"""

import json
import time
from collections import deque

import requests

from .config import *
from .log_parsers import *

with open(MACHINE_ID_PATH) as fd:
    MACHINE_ID = fd.read().strip()


parsers = (
    AuthParser(AUTH_LOG),
    AuditParser(AUDIT_LOG),
)


def handle_events(events: deque[Event]) -> None:
    """
    Iterate over the events, convert their data to the appropriate format
    and send to the attestation server.
    """
    headers = {"Content-type": "application/json"}
    while events:
        event = events.popleft()

        # send parsed event
        event_dict = {
            "machine_id": MACHINE_ID,
            "timestamp": event.timestamp,
            "type": event.type,
            "log_filepath": event.log_file,
            "props": "",
        }

        event_props = {
            key: value for key, value in event.__dict__.items() if key not in event_dict
        }
        event_dict["props"] = json.dumps(event_props)
        _ = requests.post(
            url=f"{BASE_URL}/api/event/add", json=event_dict, headers=headers
        )

        # send raw event log
        event_log = event_dict.copy()
        _ = event_log.pop("props")
        event_log["content"] = event.raw_content
        _ = requests.post(
            url=f"{BASE_URL}/api/log/add", json=event_log, headers=headers
        )


while True:
    for parser in parsers:
        parser.run()
        handle_events(parser.events)

    time.sleep(60)
