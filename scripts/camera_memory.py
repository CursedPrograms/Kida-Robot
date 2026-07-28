# camera_memory.py — remembers the last photo KIDA took
#
# Single source of truth so camera_actions.take_photo() (voice or button)
# and both HUDs (pygame + web) agree on what the "last photo" is.

import threading
import time

_lock = threading.Lock()
_last_photo_path: str | None = None
_last_photo_time: float | None = None


def record_photo(path: str) -> None:
    global _last_photo_path, _last_photo_time
    with _lock:
        _last_photo_path = path
        _last_photo_time = time.time()


def get_last_photo() -> tuple[str | None, float | None]:
    with _lock:
        return _last_photo_path, _last_photo_time
