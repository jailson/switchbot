# SwitchBot API

This project exposes a simple HTTP webhook to trigger a SwitchBot press via BLE.

## Prerequisites

- Linux or Windows machine with a working Bluetooth adapter
- Python 3.10+ (venv already configured in the project)
- `make` command (optional, but recommended)

## Finding Your SwitchBot MAC Address

**Option 1: Use the API scan endpoint (easiest)**

Start the API:
```bash
make start
```

Then in another terminal, scan for SwitchBot devices:
```bash
# Scan for SwitchBots
curl http://localhost:5000/devices
```

Response example:
```json
{
  "status": "success",
  "devices": [
    {"mac": "XX:XX:XX:XX:XX:XX", "name": "SwitchBot", "rssi": -45}
  ],
  "count": 1
}
```

**Option 2: Run scan.py directly (without API)**

```bash
.venv/bin/python src/scan.py
```

Output:
```
Scanning for SwitchBot devices (5 seconds)...
Found X SwitchBots:
  MAC: XX:XX:XX:XX:XX:XX
  Name: SwitchBot
```

**Option 3: Use bluetoothctl (Linux only)**

```bash
bluetoothctl scan on
# Tap your SwitchBot - look for: [NEW] Device XX:XX:XX:XX:XX:XX
bluetoothctl scan off
```

**Option 4: Use Settings app (Windows)**
- Settings → Bluetooth & devices → Devices

## Quick start

1. Create the virtual environment (if needed) and install dependencies:

```bash
make install
```

`make install` runs `python3 -m venv .venv` automatically the first time. If your system uses another interpreter name, run `make install PYTHON=python`.

2. Activate the project venv when you plan to run scripts directly:

```bash
source .venv/bin/activate  # On Linux/macOS
# or on Windows:
.venv\Scripts\activate
```

3. Start the API (binds to all interfaces on port 5000):

```bash
make start
```

4. Test locally with curl:

```bash
# Replace XX:XX:XX:XX:XX:XX with your bot's MAC address
curl -X POST http://localhost:5000/devices/XX:XX:XX:XX:XX:XX/press
```

5. Test from another machine on your LAN:

- Find this machine's IP:

```bash
hostname -I
```

- Then from another computer run:

```bash
curl -X POST http://<YOUR_IP>:5000/devices/XX:XX:XX:XX:XX:XX/press
```

Replace `<YOUR_IP>` with the IP from `hostname -I` (e.g. `192.168.1.100`) and `XX:XX:XX:XX:XX:XX` with your bot's MAC.

## Run as a background service (simple)

Use `nohup` to run in background:

```bash
nohup .venv/bin/python src/api.py &
```

For production, create a `systemd` service that runs the venv Python and restricts access.

## Security recommendations

- Only use on local networks (port 5000 not exposed to the internet)
- Restrict access to the port with a firewall (ufw/iptables)
- If you need external access, use a VPN or reverse proxy with authentication

## Troubleshooting

- If Bluetooth scanning fails, ensure adapter is powered and you are in the `bluetooth` group:

```bash
sudo systemctl restart bluetooth
sudo usermod -aG bluetooth $USER
```

## Files

- `src/scan.py` — Standalone BLE device scanner (can be used without the API)
- `src/press.py` — Executes the press command via BLE
- `src/api.py` — Flask webhook API
- `Makefile` — Build/run commands
- `requirements.txt` — Python dependencies

## API Endpoints

### GET /devices

Scan for SwitchBot devices in range.

```bash
curl http://localhost:5000/devices
```

Response (200):
```json
{
  "status": "success",
  "devices": [
    {"mac": "XX:XX:XX:XX:XX:XX", "name": "SwitchBot", "uuids": ["..."]}
  ],
  "count": 1
}
```

### POST /devices/{mac}/press

Press the SwitchBot with the given MAC address.

```bash
curl -X POST http://localhost:5000/devices/XX:XX:XX:XX:XX:XX/press
```

Response Success (200):
```json
{
  "status": "success",
  "message": "SwitchBot (XX:XX:XX:XX:XX:XX) pressed successfully"
}
```

Response Error (500):
```json
{
  "status": "error",
  "message": "Failed to press SwitchBot (XX:XX:XX:XX:XX:XX)",
  "error": "Connection failed"
}
```

---

Works on Linux and Windows with Bluetooth adapters.
