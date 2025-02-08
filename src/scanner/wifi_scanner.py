import subprocess
import re
from typing import List, Dict

def scan_wifi() -> List[Dict]:
    try:
        output = subprocess.run(['netsh', 'wlan', 'show', 'networks', 'mode=Bssid'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if output.returncode != 0:
            return []

        networks = []
        current_network = {}
        
        for line in output.stdout.split('\n'):
            line = line.strip()
            
            if 'SSID' in line and 'BSSID' not in line:
                if current_network:
                    networks.append(current_network)
                current_network = {'ssid': line.split(':')[1].strip()}
            
            elif 'Signal' in line:
                current_network['signal'] = line.split(':')[1].strip()
            
            elif 'BSSID' in line:
                current_network['bssid'] = line.split(':')[1].strip()
            
            elif 'Authentication' in line:
                current_network['security'] = line.split(':')[1].strip()
                
        if current_network:
            networks.append(current_network)
            
        return networks
    except Exception as e:
        print(f"Error scanning networks: {e}")
        return []