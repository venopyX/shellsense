import logging
import os
import socket
from datetime import datetime

import psutil

logger = logging.getLogger(__name__)


class SystemContext:
    """
    Utility class for gathering system context information.
    """

    @staticmethod
    def get_context() -> dict:
        """
        Gather and return general utility information about the system.

        Returns:
            dict: A dictionary containing system information including:
                - date_time: Current date and time
                - user: Current user
                - hostname: System hostname
                - current_dir: Current working directory
                - shell: Current shell
                - term: Current terminal
                - ip: System IP address
                - cpu_usage: CPU usage percentage
                - memory_usage: Memory usage percentage
                - disk_usage: Disk usage percentage

        Raises:
            OSError: If unable to gather system information
            psutil.Error: If unable to gather system metrics
        """
        try:
            logger.info("Gathering system context information")
            date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            user = os.getenv("USER", "Unknown User")
            hostname = os.uname().nodename
            current_dir = os.getcwd()
            shell = os.getenv("SHELL", "Unknown Shell")
            term = os.getenv("TERM", "Unknown Terminal")

            try:
                ip = socket.gethostbyname(socket.gethostname())
            except socket.error:
                logger.warning("Unable to get IP address")
                ip = "Unknown"

            try:
                cpu = psutil.cpu_percent()
                memory = psutil.virtual_memory().percent
                disk = psutil.disk_usage("/").percent
            except psutil.Error as e:
                logger.error(f"Failed to gather system metrics: {str(e)}")
                cpu = memory = disk = "Unknown"

            context = {
                "date_time": date_time,
                "user": user,
                "hostname": hostname,
                "current_dir": current_dir,
                "shell": shell,
                "term": term,
                "ip": ip,
                "cpu_usage": f"{cpu}%" if isinstance(cpu, (int, float)) else cpu,
                "memory_usage": (
                    f"{memory}%" if isinstance(memory, (int, float)) else memory
                ),
                "disk_usage": f"{disk}%" if isinstance(disk, (int, float)) else disk,
            }

            logger.debug("Successfully gathered system context")
            return context

        except Exception as e:
            logger.error(f"Failed to gather system context: {str(e)}")
            return {
                "error": f"Failed to gather system context: {str(e)}",
                "date_time": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            }


# Usage Example:
# context = SystemContext.get_context()
# for key, value in context.items():
#     print(f"{key}: {value}")
