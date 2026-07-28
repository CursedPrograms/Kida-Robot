# ir_bridge.py — IR remote bridge, polled once per frame
#
# Reads state.irCommand / state.irMode (written by arduino.py) and
# dispatches to mode_control or motor commands.

import state
import config
import motor_lock
from state import DriveMode
from arduino import send_command, set_motor_speed, set_driving_lights, set_stopped_lights
import mode_manager

_last_ir_command = None
_last_ir_mode    = None
motor_speed_ref  = [config.DEFAULT_SPEED]   # mutable box shared with caller

_IR_MODE_MAP = {
    "IR_REMOTE":     DriveMode.IR_REMOTE,
    "KEYBOARD":      DriveMode.KEYBOARD,
    "AUTO":          DriveMode.AUTONOMOUS,
    "IDLE":          DriveMode.IDLE,
    "LINE_FOLLOWER": DriveMode.LINE_FOLLOWER,
    "WATCHDOG":      DriveMode.WATCHDOG,
}

def poll(motor_speed_box: list, music_ctrl=None) -> None:
    """
    Call once per frame from the main loop.
    motor_speed_box is a one-element list so the caller sees speed changes.
    music_ctrl is the MusicPlayer instance from ui.py (optional; safe to omit).
    """
    global _last_ir_command, _last_ir_mode

    # ── Mode change via IR ──
    ir_mode = getattr(state, "irMode", None)
    if ir_mode and ir_mode != _last_ir_mode:
        _last_ir_mode = ir_mode
        if ir_mode in _IR_MODE_MAP:
            mode_manager.set_mode(_IR_MODE_MAP[ir_mode])

    # ── Commands ──
    cmd = getattr(state, "irCommand", None)
    if cmd == _last_ir_command:
        return
    _last_ir_command = cmd
    if not cmd or cmd == "-":
        return

    print(f"🎮 IR cmd: {cmd}")

    # Motor lock — instant, no password, works regardless of drive mode
    if cmd == "LOCK":
        motor_lock.lock()
        return
    elif cmd == "UNLOCK":
        motor_lock.unlock_no_password()
        return

    # Music + speed + the mode-toggle button work regardless of which drive
    # mode is currently active — only actual movement needs to be gated to
    # IR_REMOTE mode below (previously these were nested under that gate too,
    # so e.g. the PLAY button silently did nothing unless already in IR mode).
    if cmd == "PLAY":
        if music_ctrl:
            if music_ctrl.is_playing():
                music_ctrl.skip()
            else:
                music_ctrl.start()
        return
    elif cmd == "SPEED_UP":
        motor_speed_box[0] = min(motor_speed_box[0] + config.SPEED_STEP,
                                 config.MAX_SPEED)
        set_motor_speed(motor_speed_box[0])
        return
    elif cmd == "SPEED_DOWN":
        motor_speed_box[0] = max(motor_speed_box[0] - config.SPEED_STEP,
                                 config.MIN_SPEED)
        set_motor_speed(motor_speed_box[0])
        return
    elif cmd == "NEXT_MODE":
        if mode_manager.is_ir():
            mode_manager.set_mode(DriveMode.KEYBOARD)
        else:
            mode_manager.set_mode(DriveMode.IR_REMOTE)
        return

    # Movement — IR_REMOTE mode only
    if not mode_manager.is_ir():
        return

    _MOVE_CMDS = {"FORWARD", "BACKWARD", "LEFT", "RIGHT"}
    if cmd in _MOVE_CMDS:
        send_command("dev00", cmd)
        set_driving_lights()
    elif cmd == "STOP":
        send_command("dev00", "STOP")
        set_stopped_lights()
