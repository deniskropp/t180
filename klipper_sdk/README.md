# Klipper SDK

A Python SDK for the KDE Klipper clipboard manager.

## Installation
```bash
pip install jeepney pydantic
```

## Usage
```python
from klipper_sdk import KlipperClient

# Initialize client
client = KlipperClient()

# Get clipboard history
history = client.get_history()

# Set current clipboard content
client.set_clipboard("Hello from Python!")

# Clear history
client.clear_history()
```

## Requirements
- KDE Klipper running on a Linux system with D-Bus.
