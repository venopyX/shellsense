import os
from datetime import datetime
import psutil
import socket

class SystemContext:
    @staticmethod
    def get_context():
        """Gather and return general utility information."""
        date_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        user = os.getenv("USER", "Unknown User")
        hostname = os.uname().nodename
        current_dir = os.getcwd()
        shell = os.getenv("SHELL", "Unknown Shell")
        term = os.getenv("TERM", "Unknown Terminal")
        ip = socket.gethostbyname(socket.gethostname())
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent

        return {
            "date_time": date_time,
            "user": user,
            "hostname": hostname,
            "current_dir": current_dir,
            "shell": shell,
            "term": term,
            "ip": ip,
            "cpu_usage": f"{cpu}%",
            "memory_usage": f"{memory}%",
            "disk_usage": f"{disk}%",
        }

# # Usage Example:
# context = SystemContext.get_context()
# for key, value in context.items():
#     print(f"{key}: {value}")
