```markdown
# WiFi Manager

WiFi Manager is a Python-based tool designed for educational and authorized network management. It provides functionalities to:

- **Scan for Wi-Fi Networks:** List available Wi-Fi networks using system commands.
- **Discover Connected Devices:** Identify devices on your network using Nmap.
- **Network Control (Advanced):** Perform actions like deauthentication (requires root/administrator privileges).

> **Important:** The network control features (e.g., deauthentication) are provided for educational purposes only. **Unauthorized use is illegal and unethical.** Always ensure you have explicit permission before performing any network control operations.

## Project Structure

```
wifi_manager/
├── src/
│   ├── scanner/
│   │   ├── __init__.py
│   │   └── wifi_scanner.py       # Wi-Fi scanning module
│   ├── devices/
│   │   ├── __init__.py
│   │   └── device_discovery.py   # Device discovery module
│   ├── network/
│   │   ├── __init__.py
│   │   └── network_controller.py # Network control module (advanced)
│   └── utils/
│       ├── __init__.py
│       └── helpers.py            # Utility functions
├── config/
│   └── router_config.json        # Router configuration file (optional)
├── main.py                       # Main application entry point
└── requirements.txt              # Project dependencies
```

## Features

- **Wi-Fi Scanning:** Uses OS-specific commands (Windows, Linux, macOS) to scan for available Wi-Fi networks.
- **Device Discovery:** Leverages Nmap to identify active devices on the network.
- **Network Control:** Uses Scapy to send deauthentication packets (*requires root/administrator privileges*).

## Requirements

- **Python 3.x**
- **Nmap:** Must be installed on your system.  
  - **Linux:** `sudo apt-get install nmap`
  - **macOS:** `brew install nmap`
  - **Windows:** [Download from Nmap's website](https://nmap.org/download.html)
- **Root/Administrator Privileges:** Required for advanced network operations (e.g., deauthentication).
- **Wi-Fi Adapter:** For scanning and, if needed, monitor mode operations.

### Python Dependencies

See `requirements.txt`:

```
python-nmap==0.7.1
scapy==2.5.0
```

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/HasinduNimesh/wifi_manager.git
   cd wifi_manager
   ```

2. **(Optional) Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application with:

```bash
python main.py
```

### What It Does:

- **Wi-Fi Scanning:**  
  The tool will list available Wi-Fi networks detected by your system.
  
- **Device Discovery:**  
  It scans the local network (default: `192.168.1.0/24`) to identify connected devices.

- **Network Control (Optional):**  
  Uncomment and modify the deauthentication example in `main.py` to kick a device off the network (*only with explicit permission and root privileges*).

## Configuration

- **Router Configuration:**  
  If needed, update `config/router_config.json` with your router settings.

- **Network Controller Settings:**  
  Modify the placeholder MAC addresses in `src/network/network_controller.py` to match your network environment.

## Legal and Ethical Disclaimer

**WARNING:**  
The deauthentication functionality is **only** for educational and authorized testing purposes. Using these tools on networks without explicit permission is illegal and unethical. **Always ensure you have proper authorization before testing.**

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/HasinduNimesh/wifi_manager/issues).

## License

This project is provided for educational purposes only. Use it at your own risk.
```
