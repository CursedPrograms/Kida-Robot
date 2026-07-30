# watchdog_mode.py — person-detection alarm mode
#
# When active: YOLO inference runs on cam-0.  If a "person" class is detected
# with its box center inside config.WATCHDOG_ZONE, the LEDs strobe and an
# alarm beep plays through pygame.  No motor commands are sent — the robot
# stays still and watches. WATCHDOG_ZONE defaults to the full frame (any
# person, anywhere); narrow it in config.py to watch e.g. just a doorway.

import threading
import time
import logging

import state
import leds
import config

logger = logging.getLogger(__name__)

POLL_INTERVAL  = 0.25   # seconds between detection checks
COOLDOWN       = 3.0    # seconds to keep alarm active after person leaves view

_stop_event    = threading.Event()
_thread: threading.Thread | None = None

# ── Alarm beep (generated at first use, cached) ──────────────────────────────
_alarm_sound = None


def _get_alarm_sound():
    global _alarm_sound
    if _alarm_sound is not None:
        return _alarm_sound
    try:
        import numpy as np
        import pygame
        sample_rate = 44100
        duration    = 0.18   # short sharp beep
        freq        = 1200   # Hz
        n = int(sample_rate * duration)
        t = np.linspace(0, duration, n, False)
        wave = (np.sign(np.sin(2 * np.pi * freq * t)) * 28000).astype(np.int16)
        stereo = np.column_stack([wave, wave])
        _alarm_sound = pygame.sndarray.make_sound(stereo)
        logger.info("Alarm beep generated")
    except Exception as e:
        logger.warning("Could not generate alarm beep: %s", e)
        _alarm_sound = None
    return _alarm_sound


def _person_in_zone() -> bool:
    zx1, zy1, zx2, zy2 = config.WATCHDOG_ZONE
    for det in state.detection_boxes:
        if det["label"].lower() != "person":
            continue
        x1, y1, x2, y2 = det["box"]
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        if zx1 <= cx <= zx2 and zy1 <= cy <= zy2:
            return True
    return False


def _run():
    logger.info("Watchdog thread started")
    state.systemStatus = "Watchdog: ARMED"
    alarm_active   = False
    last_seen_time = 0.0
    last_beep_time = 0.0

    sound = _get_alarm_sound()

    while not _stop_event.is_set():
        if _person_in_zone():
            now = time.time()
            last_seen_time = now
            if not alarm_active:
                alarm_active = True
                leds.start_alarm_strobe()
                logger.info("⚠ PERSON ENTERED WATCH ZONE — alarm triggered")
                print("🚨 Watchdog: PERSON ENTERED WATCH ZONE")
            state.systemStatus = "Watchdog: PERSON IN ZONE ⚠"
            if sound and now - last_beep_time >= 0.22:
                try:
                    sound.play()
                    last_beep_time = now
                except Exception:
                    pass
        else:
            elapsed = time.time() - last_seen_time
            if alarm_active and elapsed > COOLDOWN:
                alarm_active = False
                leds.stop_alarm_strobe()
                state.systemStatus = "Watchdog: ARMED"
                logger.info("Watchdog: alarm cleared")
                print("✅ Watchdog: zone clear — alarm cleared")

        time.sleep(POLL_INTERVAL)

    # Clean up on exit
    if alarm_active:
        leds.stop_alarm_strobe()
    state.systemStatus = "Watchdog: OFF"
    logger.info("Watchdog thread stopped")


def start() -> None:
    global _thread
    if _thread and _thread.is_alive():
        return
    _stop_event.clear()
    _thread = threading.Thread(target=_run, daemon=True, name="Watchdog")
    _thread.start()
    print("🚨 Watchdog mode started")


def stop() -> None:
    _stop_event.set()
    if _thread:
        _thread.join(timeout=2.0)
    print("🚨 Watchdog mode stopped")
