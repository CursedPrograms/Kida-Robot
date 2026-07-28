# ambient_narration.py — periodic "let me tell you what I see" flavor lines
#
# KIDA is wake-word activated for conversation, but this lets her speak up
# unprompted every so often to describe her surroundings using live sensor
# state — camera detections, distance sensors, motion. Off by default.
#
# Enable via voice ("start narrating" / "stop narrating" / "what do you
# see"), or directly: ambient_narration.set_enabled(True).

import random
import threading

import state
import voice_engine

_MIN_INTERVAL_S = 45
_MAX_INTERVAL_S = 90

_thread: threading.Thread | None = None
_stop_event = threading.Event()


def _as_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _describe_now() -> str:
    parts = []

    labels = getattr(state, "detection_labels", None)
    if labels:
        names = ", ".join(sorted({n for n, _ in labels}))
        parts.append(f"I can see {names}")
    else:
        parts.append("Nothing interesting in view right now")

    us0 = _as_float(getattr(state, "ultrasonic0Value", None))
    us1 = _as_float(getattr(state, "ultrasonic1Value", None))
    candidates = [d for d in (us0, us1) if d is not None]
    if candidates:
        closest = min(candidates)
        if closest < 20:
            parts.append("and something's right in front of me")
        elif closest < 60:
            parts.append(f"and there's something about {int(closest)} centimeters out")

    if str(getattr(state, "motionValue", "0")) in ("1", "HIGH", "True"):
        parts.append("I'm picking up motion nearby")

    return ", ".join(parts) + "."


def describe_now(block: bool = False) -> None:
    """Speak one surroundings description immediately, regardless of the enabled flag."""
    voice_engine.speak_line(_describe_now(), block=block)


def _loop():
    while True:
        if _stop_event.wait(random.uniform(_MIN_INTERVAL_S, _MAX_INTERVAL_S)):
            break
        if voice_engine.DESCRIBE_SURROUNDINGS:
            try:
                describe_now()
            except Exception as e:
                print(f"⚠️ ambient_narration error: {e}")


def start() -> None:
    """
    Start the background timer thread. Safe to call once at boot — actual
    narration only happens while voice_engine.DESCRIBE_SURROUNDINGS is True.
    """
    global _thread
    if _thread and _thread.is_alive():
        return
    _stop_event.clear()
    _thread = threading.Thread(target=_loop, daemon=True)
    _thread.start()
    print("🗣 Ambient narration thread started (currently "
          f"{'ON' if voice_engine.DESCRIBE_SURROUNDINGS else 'OFF'})")


def stop() -> None:
    _stop_event.set()


def set_enabled(enabled: bool) -> None:
    voice_engine.DESCRIBE_SURROUNDINGS = enabled
    print(f"🗣 Ambient narration {'ON' if enabled else 'OFF'}")
