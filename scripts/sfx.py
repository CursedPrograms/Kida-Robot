# sfx.py — short one-shot sound effects (camera shutter, video reel, ...)
#
# Plays on its own pygame Channel, separate from music (pygame.mixer.music)
# and from voice_engine's speech channel, so none of the three interrupt
# each other.

import os
import pygame

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR    = os.path.dirname(_SCRIPT_DIR)
SFX_DIR     = os.path.join(BASE_DIR, "audio")

_channel = None


def _get_channel():
    global _channel
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    if _channel is None:
        _channel = pygame.mixer.Channel(6)  # reserved, separate from voice (7) and music
    return _channel


def play(name: str, block: bool = False) -> None:
    """Play audio/<name> (e.g. 'camera_shutter.mp3'). Missing file = silent no-op."""
    path = os.path.join(SFX_DIR, name)
    if not os.path.isfile(path):
        print(f"⚠️ sfx: {path} not found — skipping")
        return
    try:
        sound = pygame.mixer.Sound(path)
        ch = _get_channel()
        ch.play(sound)
        if block:
            while ch.get_busy():
                pygame.time.wait(20)
    except Exception as e:
        print(f"⚠️ sfx playback error: {e}")
