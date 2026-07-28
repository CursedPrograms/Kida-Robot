# mode_manager.py — remote-controller stand-in for the robot's mode_manager
#
# The real scripts/mode_manager.py calls into arduino.py to stop motors on
# every mode change — that's robot-only hardware. This shim only mirrors
# the *current* mode (kept in sync by remote_client.py's /status poll into
# state.drive_mode) so hud_draw.py, which imports `mode_manager` and calls
# current_mode()/is_idle()/is_keyboard(), works unmodified on the
# controller. Actual mode switching happens on the robot via
# RemoteClient.send_action("mode_N").

import state
from state import DriveMode


def current_mode() -> DriveMode:
    return state.drive_mode


def is_idle() -> bool:
    return state.drive_mode == DriveMode.IDLE


def is_keyboard() -> bool:
    return state.drive_mode == DriveMode.KEYBOARD
