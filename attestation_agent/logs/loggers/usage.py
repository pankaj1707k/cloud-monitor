import time

from psutil import (
    # For system uptime
    boot_time,

    # For CPU utilization
    cpu_percent,

    # For memory utilization
    swap_memory,
    virtual_memory,

    # For disk and network counters
    disk_io_counters,
    net_io_counters,

    # For battery percentage and device temperature
    sensors_battery,
    sensors_temperatures
)

from .base import Logger


class UsageLogger(Logger):
    """Logger for system usage logging"""

    type = "USAGE"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._data = self._record_io_data()

    def _record_io_data(self) -> dict[str, dict[str,int]]:
        du = disk_io_counters()
        disk_usage = {
            "read_count": du.read_count,
            "write_count": du.write_count,
            "read_bytes": du.read_bytes,
            "write_bytes": du.write_bytes,
            "busy_time": du.busy_time
        }

        nu = net_io_counters()
        network_usage = {
            "bytes_sent": nu.bytes_sent,
            "bytes_recv": nu.bytes_recv,
            "packets_sent": nu.packets_sent,
            "packets_recv": nu.packets_recv
        }

        data = {
            "disk": disk_usage,
            "network": network_usage,
        }
        return data

    def _collect_log(self) -> dict:
        """
        Collect various system usage metrics
        """
        uptime = boot_time()
        cpu_usage = cpu_percent()

        sm = swap_memory()
        vm = virtual_memory()
        mem_usage = {
            "primary": vm.percent,
            "swap": sm.percent
        }

        # Record IO data
        current_data = self._record_io_data()

        data = {
            category: {
                key: current_data[category][key] - self._data[category][key]
                for (key, value) in self._data[category].items()
            } for category in current_data
        }

        self._data = current_data

        # NOTE: We are using VMs, they don't have any physical batteries (but virtual)
        #battery_percentage = sensors_battery().percent
        battery_percentage = 100

        # NOTE: Same reason as above
        #temperatures = sensors_temperatures()["coretemp"]
        #avg_temperature = sum(map(lambda temp: temp.current, temperatures)) / len(temperatures)
        avg_temperature = 25.0

        log = {
            "timestamp": int(time.time()),
            "uptime": uptime,
            "battery": battery_percentage,
            "cpu": cpu_usage,
            "memory": mem_usage
        }
        log.update(data)
        return log