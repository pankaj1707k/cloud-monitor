import time

from psutil import (
    # For system uptime
    boot_time,

    # For CPU utilization
    cpu_freq,

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

from attestation_agent.logs import Logger


class UsageLogger(Logger):
    """Logger for system usage logging"""

    type = "USAGE"

    def _collect_log(self) -> dict:
        """
        Collect various system usage metrics
        """
        uptime = boot_time()
        cpu_usage = cpu_freq()[0]

        sm = swap_memory()
        vm = virtual_memory()

        mem_usage = {
            "primary": {
                "available": vm.available,
                "total": vm.total
            },
            "swap": {
                "available": sm.free,
                "total": sm.total
            }
        }

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

        # NOTE: We are using VMs, they don't have any physical batteries (but virtual)
        #battery_percentage = sensors_battery().percent
        battery_percentage = 100

        # NOTE: Same reason as above
        #temperatures = sensors_temperatures()["coretemp"]
        #avg_temperature = sum(map(lambda temp: temp.current, temperatures)) / len(temperatures)
        avg_temperature = 25.0

        return {
            "timestamp": int(time.time()),
            "uptime": uptime,
            "battery": battery_percentage,
            "cpu": cpu_usage,
            "memory": mem_usage,
            "disk": disk_usage,
            "network": network_usage,
            "temperature": avg_temperature,
        }
