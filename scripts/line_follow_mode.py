# line_follow_mode.py — Line follower mode with proper thread management

import threading
import time
import logging

import state
from arduino import send_command

logger = logging.getLogger(__name__)

LOOP_DELAY     = 0.05   # 50 ms
LINE_THRESHOLD = 500

_stop_event = threading.Event()
_thread: threading.Thread | None = None


def _parse_sensor(value):
    if value is None:
        return None
    try:
        if isinstance(value, str) and ": " in value:
            return int(value.split(": ")[1])
        return int(float(str(value)))
    except (ValueError, IndexError, AttributeError):
        return None


def _read_sensors():
    return (
        _parse_sensor(getattr(state, 'lfLeftValue', None)),
        _parse_sensor(getattr(state, 'lfMidValue',  None)),
        _parse_sensor(getattr(state, 'lfRightValue', None)),
    )


def _detect_position(left, middle, right):
    def on(v):
        return v is not None and v > LINE_THRESHOLD
    l, m, r = on(left), on(middle), on(right)
    if m:
        if l and r:  return "CENTER_WIDE"
        if l:        return "SLIGHT_LEFT"
        if r:        return "SLIGHT_RIGHT"
        return "CENTER"
    if l and not r:  return "LEFT"
    if r and not l:  return "RIGHT"
    return "LOST"


_CMD_MAP = {
    "CENTER":       "FORWARD",
    "CENTER_WIDE":  "FORWARD",
    "SLIGHT_LEFT":  "SLIGHT_LEFT",
    "SLIGHT_RIGHT": "SLIGHT_RIGHT",
    "LEFT":         "LEFT",
    "RIGHT":        "RIGHT",
    "LOST":         "STOP",
}


def _run():
    logger.info("Line follower thread started")
    state.systemStatus = "LineFollower: RUNNING"
    while not _stop_event.is_set():
        try:
            l, m, r = _read_sensors()
            pos = _detect_position(l, m, r)
            cmd = _CMD_MAP.get(pos, "STOP")
            send_command("dev00", cmd)
            state.systemStatus = f"LF: {cmd} | {pos} | L={l} M={m} R={r}"
        except Exception as e:
            logger.error("Line follower step error: %s", e)
            send_command("dev00", "STOP")
        time.sleep(LOOP_DELAY)
    send_command("dev00", "STOP")
    state.systemStatus = "LineFollower: STOPPED"
    logger.info("Line follower thread stopped")


def start() -> None:
    global _thread
    if _thread and _thread.is_alive():
        return
    _stop_event.clear()
    _thread = threading.Thread(target=_run, daemon=True, name="LineFollower")
    _thread.start()


def stop() -> None:
    _stop_event.set()
    if _thread:
        _thread.join(timeout=1.0)
