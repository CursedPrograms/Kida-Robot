# bluetooth.py — Bluetooth broadcast/discoverability control for KIDA
#
# For now this only makes the Pi visible over Bluetooth as BLUETOOTH_NAME
# (e.g. "KIDA01") so nearby devices can find and pair with it. Multi-robot
# pairing and the Unity/website integration are future work, not handled here.

import subprocess

import config


def _bluetoothctl(*args) -> bool:
    try:
        result = subprocess.run(
            ["bluetoothctl", *args],
            capture_output=True, text=True, timeout=5,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️ bluetoothctl {' '.join(args)} failed: {e}")
        return False


def start_broadcast(name: str = None) -> None:
    """Power on the adapter and make it discoverable/pairable indefinitely."""
    name = name or config.BLUETOOTH_NAME
    _bluetoothctl("power", "on")
    _bluetoothctl("system-alias", name)
    _bluetoothctl("discoverable-timeout", "0")
    _bluetoothctl("discoverable", "on")
    _bluetoothctl("pairable", "on")
    print(f"📶 Bluetooth broadcasting as '{name}'")


def stop_broadcast() -> None:
    _bluetoothctl("discoverable", "off")
    print("📶 Bluetooth broadcast stopped")
