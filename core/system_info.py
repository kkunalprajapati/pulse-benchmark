import platform
import psutil
import cpuinfo
import os

def read_file(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except:
        return "Unavailable"

def get_system_info():
    cpu = cpuinfo.get_cpu_info()
    mem = psutil.virtual_memory()

    info = {
        "System Summary": {
            "OS": platform.system() + " " + platform.release(),
            "Kernel Version": platform.version(),
            "Architecture": platform.machine(),
            "Hostname": platform.node(),
            "Manufacturer": read_file("/sys/devices/virtual/dmi/id/sys_vendor"),
            "Model": read_file("/sys/devices/virtual/dmi/id/product_name"),
            "Serial Number": get_serial_number(),
        },
        "Processor & Memory": {
            "CPU": cpu.get("brand_raw", "Unavailable"),
            "Physical Cores": psutil.cpu_count(logical=False),
            "Logical Cores": psutil.cpu_count(logical=True),
            "CPU Frequency": cpu.get("hz_advertised_friendly", "Unavailable"),
            "Total RAM": f"{round(mem.total / (1024 ** 3), 2)} GB",
            "Available RAM": f"{round(mem.available / (1024 ** 3), 2)} GB",
        },
        "Storage Devices": {
            "Disk Layout": os.popen("lsblk -o NAME,SIZE,TYPE,MOUNTPOINT -e7 --noheadings").read().strip()
        }
    }

    return info


def get_serial_number():
    path = "/sys/devices/virtual/dmi/id/product_serial"
    try:
        with open(path, 'r') as f:
            serial = f.read().strip()
            if serial and serial.lower() != "none":
                return serial
            else:
                return "Unavailable (try running as sudo)"
    except PermissionError:
        return "Permission denied (run Pulse as sudo to view)"
    except:
        return "Unavailable"