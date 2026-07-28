# motor_lock.py — motor lock logic, shared by the local buttons (buttons.py)
# and the network bridge (web_bridge.py) so there's one place that decides
# what "locked" means.
#
# The actual enforcement lives in arduino.send_command(), which refuses
# every dev00 (motor) command except STOP while state.motor_lock is True —
# that's what makes "motors will never move" true regardless of which mode
# or input source (keyboard, IR, autonomous, line follower, watchdog, lane
# detect, or a remote controller) is trying to drive.
#
# Locking is instant and free (safety should never require a password).
# Unlocking requires config.MOTOR_LOCK_PASSWORD.

import config
import state
from arduino import send_command, set_stopped_lights


def is_locked() -> bool:
    return state.motor_lock


def lock() -> None:
    state.motor_lock = True
    send_command("dev00", "STOP")
    set_stopped_lights()
    print("🔒 Motor lock ENGAGED")


def try_unlock(password: str) -> bool:
    """Disengage the lock if the password matches. Returns success."""
    if password == config.MOTOR_LOCK_PASSWORD:
        state.motor_lock = False
        print("🔓 Motor lock released")
        return True
    print("⚠️ Motor lock: wrong password")
    return False


def unlock_no_password() -> None:
    """Disengage the lock with no password check — only for the IR remote,
    where holding the physical remote in hand is itself the credential."""
    state.motor_lock = False
    print("🔓 Motor lock released (IR)")
