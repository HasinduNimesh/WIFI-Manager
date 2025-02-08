import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import json
from src.scanner.wifi_scanner import scan_wifi
from src.devices.device_discovery import discover_devices
from src.network.network_controller import deauth_device

class WifiManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Network Manager")
        self.root.geometry("1000x600")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create tabs
        self.networks_tab = ttk.Frame(self.notebook)
        self.devices_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.networks_tab, text='Networks')
        self.notebook.add(self.devices_tab, text='Devices & Control')
        
        self._setup_networks_tab()
        self._setup_devices_tab()

    def _setup_networks_tab(self):
        # Scan button
        scan_btn = ttk.Button(self.networks_tab, text="Scan Networks", 
                            command=self._scan_networks)
        scan_btn.pack(pady=5)
        
        # Results area
        self.networks_text = scrolledtext.ScrolledText(self.networks_tab, 
                                                     height=20, width=70)
        self.networks_text.pack(padx=5, pady=5)

    def _setup_devices_tab(self):
        # Left frame for device list
        left_frame = ttk.Frame(self.devices_tab)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Right frame for controls
        right_frame = ttk.Frame(self.devices_tab)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5, pady=5)
        
        # Device list
        ttk.Label(left_frame, text="Connected Devices").pack(pady=5)
        self.device_tree = ttk.Treeview(left_frame, columns=('IP', 'MAC', 'Hostname', 'Vendor'), 
                                      show='headings', height=15)
        
        # Define columns
        self.device_tree.heading('IP', text='IP Address')
        self.device_tree.heading('MAC', text='MAC Address')
        self.device_tree.heading('Hostname', text='Hostname')
        self.device_tree.heading('Vendor', text='Vendor')
        
        self.device_tree.column('IP', width=120)
        self.device_tree.column('MAC', width=140)
        self.device_tree.column('Hostname', width=150)
        self.device_tree.column('Vendor', width=100)
        
        self.device_tree.pack(pady=5, fill=tk.BOTH, expand=True)
        
        # Scan button
        scan_btn = ttk.Button(left_frame, text="Discover Devices", 
                             command=self._discover_devices)
        scan_btn.pack(pady=5)
        
        # Control frame
        ttk.Label(right_frame, text="Device Control").pack(pady=5)
        
        # Interface selection
        ttk.Label(right_frame, text="Interface:").pack(pady=5)
        self.interface_entry = ttk.Entry(right_frame)
        self.interface_entry.insert(0, "wlan0")
        self.interface_entry.pack(pady=5)
        
        # Deauth button
        deauth_btn = ttk.Button(right_frame, text="Deauthenticate Selected", 
                               command=self._deauth_selected)
        deauth_btn.pack(pady=10)
        
        # Status area
        self.status_text = scrolledtext.ScrolledText(right_frame, 
                                                   height=10, width=40)
        self.status_text.pack(padx=5, pady=5)

    def _scan_networks(self):
        def scan():
            self.networks_text.delete(1.0, tk.END)
            self.networks_text.insert(tk.END, "Scanning networks...\n")
            networks = scan_wifi()
            self.networks_text.delete(1.0, tk.END)
            self.networks_text.insert(tk.END, 
                                    json.dumps(networks, indent=4))
        
        threading.Thread(target=scan, daemon=True).start()

    def _discover_devices(self):
        def discover():
            # Clear existing items
            for item in self.device_tree.get_children():
                self.device_tree.delete(item)
            
            self.status_text.insert(tk.END, "Discovering devices...\n")
            devices = discover_devices()
            
            # Add devices to tree
            for device in devices:
                self.device_tree.insert('', tk.END, values=(
                    device['ip'],
                    device['mac'],
                    device['hostname'],
                    device['vendor']
                ))
            
            self.status_text.insert(tk.END, f"Found {len(devices)} devices\n")
        
        threading.Thread(target=discover, daemon=True).start()

    def _deauth_selected(self):
        selected = self.device_tree.selection()
        if not selected:
            self.status_text.insert(tk.END, "Error: No device selected\n")
            return
        
        # Get MAC address from selected item
        values = self.device_tree.item(selected[0])['values']
        mac = values[1]  # MAC is second column
        interface = self.interface_entry.get()
        
        def deauth():
            self.status_text.insert(tk.END, 
                                  f"Deauthenticating {mac}...\n")
            result = deauth_device(mac, interface)
            self.status_text.insert(tk.END, f"{result}\n")
        
        threading.Thread(target=deauth, daemon=True).start()

def main():
    root = tk.Tk()
    app = WifiManagerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()