import socket
import subprocess
import re
from typing import List, Dict

def discover_devices(network_range: str = "192.168.1.0/24") -> List[Dict]:
    devices = []
    try:
        for i in range(1, 255):
            ip = f"192.168.1.{i}"
            if ping_host(ip):
                mac = get_mac(ip)
                hostname = get_hostname(ip)
                devices.append({
                    'ip': ip,
                    'mac': mac,
                    'hostname': hostname,
                    'vendor': get_vendor(mac)
                })
    except Exception as e:
        print(f"Error scanning network: {e}")
    return devices

def ping_host(ip: str) -> bool:
    try:
        output = subprocess.run(['ping', '-n', '1', '-w', '500', ip], 
                              capture_output=True, text=True)
        return output.returncode == 0
    except:
        return False

def get_mac(ip: str) -> str:
    try:
        output = subprocess.run(['arp', '-a', ip], 
                              capture_output=True, text=True)
        if output.returncode == 0:
            match = re.search(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})', 
                            output.stdout.upper())
            return match.group(0) if match else "Unknown"
        return "Unknown"
    except:
        return "Unknown"

def get_hostname(ip: str) -> str:
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return "Unknown"

def get_vendor(mac: str) -> str:
    # Basic vendor lookup - expand with MAC vendor database
    vendors = {
        "00:50:56": "VMware",
        "00:0C:29": "VMware",
        # Add more vendor prefixes
    }
    if mac != "Unknown":
        prefix = mac[:8].upper()
        return vendors.get(prefix, "Unknown")
    return "Unknown"