# Port Scanner 🚀

A lightweight, multithreaded network and port scanning utility built with Python and featuring a modern CLI interactive menu and an optional Flask-based Web UI.

---

## Features ✨

- **Interactive CLI Menu**: Easy navigation between all scanner options using keyboard input and colors.
- **Multithreaded Port Scanner**: Scan port ranges concurrently for fast performance.
- **Single-threaded Port Scanner**: Linear port scan for targeted testing.
- **Live Host Scanner**: Scan a subnet range (e.g., active Windows hosts via port 135).
- **Web UI Representation**: Visual scan configuration and live result tracking via a Flask web server.

---

## Prerequisites 📋

Ensure you have the following installed:
- **Python**: `v3.x`
- **Flask**: `pip install flask` (required for running the Web UI)

---

## How to Run 🚀

### 1. Interactive CLI (Recommended)
Open a terminal and run the main controller script:
```bash
python src/scanner.py
```
This launches a beautiful interactive menu where you can choose between single-threaded/multithreaded scanning, live IP subnet scanning, or launching the Web UI.

### 2. Web UI Interface
To launch the Flask Web server directly:
```bash
python src/mainScanner.py
```
Then navigate to: `http://127.0.0.1:5000/` in your browser.

---

## Configuration ⚙️

Scan ranges and threading options are defined in [config.json](config.json):
```json
{
    "range": {
        "low": "1",
        "high": "8888"
    },
    "ipRange": {
        "low": "0",
        "high": "255"
    },
    "thread": {
        "count": "8"
    }
}
```
- `range.low` & `range.high`: Port range boundaries for the port scanner.
- `ipRange.low` & `ipRange.high`: Last octet subnet range for the live host scanner.
- `thread.count`: Number of concurrent threads to use during multithreaded scans.

---

## Disclaimer ⚠️

This utility is intended only for legal security testing on equipment you own or have explicit permission to test. The authors accept no liability for misuse.
