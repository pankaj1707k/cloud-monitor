import os

# Path to a session file to save the state of the attestation agent
# so that we can resume last session without re-parsing already parsed logs
SESSION_FILEPATH = os.path.expanduser("~/.attestation-agent.session")

# Path to various log files
AUTH_LOG = "/var/log/auth.log"
AUDIT_LOG = "/var/log/audit/audit.log"

# Path to obtain a device identifier
MACHINE_ID_PATH = "/etc/machine-id"

# Attestation server related configurations
ATTESTATION_HOST = "10.10.10.185"
ATTESTATION_PORT = "3000"
BASE_URL = f"http://{ATTESTATION_HOST}:{ATTESTATION_PORT}"
