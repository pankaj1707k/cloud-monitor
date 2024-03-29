import sys
import time
from abc import ABC, abstractmethod
from collections import deque
from threading import Lock

from attestation_agent.errors import LogError


class Logger(ABC):
    """
    Base class for all loggers.
    """

    def __init__(self) -> None:
        # Store the state of logger
        self._running: bool = True

        # Save the machine ID for socket communication to identify the device
        self.machine_id: str = None

        # Create a mutex lock used to pause the parser to flush generated events
        self.lock: Lock = Lock()

        # Facilitates faster removal from the front of queue after
        # log has been analyzed. Removal is required to prevent
        # high memory consumption when machine runs for longer durations.
        self.logs: deque[str] = deque()

    def run(self, machine_id: str, sio: "socketio.Client") -> None:
        """
        Run the logger.
        """
        # Save the machine ID
        self.machine_id = machine_id

        # While the logger can run, it will collect
        # usage metrics and send them to the attestation server
        while self._running:
            # Try to collect usage metrics and catch any error
            # and print it as LogError
            try:
                data = self._collect_log()
            except Exception as exc:
                print(
                    LogError(
                        msg="error while collecting usage metrics",
                        exc=exc
                    ),
                    file=sys.stderr
                )
            finally:
                # Send the data to the attestation server
                self._send_log(sio, data)

            # Wait for some time
            # NOTE: Can be adjusted: SLOW, NORMAL, FAST
            time.sleep(1)

    @abstractmethod
    def _collect_log(self) -> dict:
        """
        Collect data to be logged
        For example:
         - application usage
         - system usage
        """
        raise NotImplementedError("Implementation required for: _collect_log")

    def _send_log(self, sio: "socketio.Client", data: dict) -> None:
        """
        Sends data to the attestation server
        """
        # Create a timestamp at which the log was recorded
        timestamp = int(time.time())

        try:
            sio.emit("collect_log", (self.machine_id, timestamp, self.type, data))
        except Exception as exc:
            print(
                LogError(
                    msg="error while sending logs",
                    exc=exc
                ),
                file=sys.stderr
            )

    def resume(self):
        """
        Set the logger state to running
        """
        self._running = True

    def stop(self):
        """
        Set the logger state to stopped
        """
        self._running = False
