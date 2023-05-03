"""
Main driver code that runs the agent.
This file is autorun on `python attestation-agent` command.
"""

import json
import time
from collections import deque

import requests
from log_parsers import *

AUTH_LOG = "/var/log/auth.log"
AUDIT_LOG = "/var/log/audit/audit.log"
MACHINE_ID_PATH = "/etc/machine-id"
ATTESTATION_HOST = ""
ATTESTATION_PORT = "8080"
BASE_URL = f"http://{ATTESTATION_HOST}:{ATTESTATION_PORT}"

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
            "data": "",
        }
        event_props = {
            key: value for key, value in event.__dict__.items() if key not in event_dict
        }
        event_dict["data"] = json.dumps(event_props)
        _ = requests.post(
            url=f"{BASE_URL}/api/event/add", data=event_dict, headers=headers
        )

        # send raw event log
        event_log = event_dict.copy()
        _ = event_log.pop("log_filepath")
        _ = event_log.pop("data")
        event_log["content"] = event.raw_content
        _ = requests.post(
            url=f"{BASE_URL}/api/log/add", data=event_log, headers=headers
        )


while True:
    for parser in parsers:
        parser.run()
        handle_events(parser.events)

    time.sleep(60)