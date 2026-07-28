# voice_commands.py — map spoken phrases to robot control actions
#
# Called from kida_chat_wakeword._task_worker before falling through to LLM.
# If a phrase matches a command, the action is executed and the LLM is skipped.

import re

# ── Pattern → action key ────────────────────────────────────────────────────
# Narration and video-recording "stop ..." phrases must come before the
# generic "stop" pattern below — otherwise "stop narrating"/"stop recording"
# would match \bstop\b first and trigger a full motor stop instead.
_COMMANDS = [
    (r"\b(stop narrating|stop describing|quiet down|stay quiet)\b",       "narrate_off"),
    (r"\b(start narrating|describe your surroundings|describe what you see|keep me posted)\b", "narrate_on"),
    (r"\b(what do you see|where are you|look around)\b",                 "narrate_once"),
    (r"\b(stop recording|stop the video|end recording|stop filming)\b",   "video_stop"),
    (r"\b(take a picture|take a photo|snap a photo|snap a picture)\b",    "photo"),
    (r"\b(record a? ?video|start recording|film this|start filming)\b",  "video_start"),
    (r"\b(switch camera|change camera|other camera|next camera|swap camera)\b", "camera_switch"),
    (r"\b(stop|halt|emergency stop|full stop|freeze)\b",        "stop"),
    (r"\b(play music|play song|play track|start music)\b",      "music_play"),
    (r"\b(next track|skip track|skip song|next song|skip)\b",   "music_skip"),
    (r"\b(stop music|mute music|no music|quiet|silence)\b",     "music_stop"),
    (r"\b(keyboard mode|manual mode|take control|drive)\b",     "mode_keyboard"),
    (r"\b(autonomous mode|auto mode|self.?driv)\b",             "mode_autonomous"),
    (r"\b(line follow|line follower|follow the line|follow line)\b", "mode_line_follow"),
    (r"\b(idle|sleep mode|standby|do nothing)\b",               "mode_idle"),
    (r"\b(watchdog|watch mode|guard mode|sentry|alarm mode)\b", "mode_watchdog"),
    (r"\b(lane detect|lane detection|follow lane|detect lane)\b","mode_lane"),
]

_REPLIES = {
    "stop":             "All motors stopped.",
    "narrate_off":      "Going quiet. Wake me if you need me.",
    "narrate_on":       "You got it — I'll keep you posted.",
    "photo":            "Got it, say cheese!",
    "video_start":      "Recording now.",
    "video_stop":       "Stopped recording.",
    "music_play":       "Playing music.",
    "music_skip":       "Next track.",
    "music_stop":       "Music off.",
    "mode_keyboard":    "Switching to keyboard mode.",
    "mode_autonomous":  "Going autonomous. Try to keep up.",
    "mode_line_follow": "Activating line follower.",
    "mode_idle":        "Entering idle mode.",
    "mode_watchdog":    "Watchdog mode active. I'm watching.",
    "mode_lane":        "Lane detection active.",
}


def _norm(text: str) -> str:
    return re.sub(r"[^\w\s]", "", text.lower()).strip()


def dispatch(text: str) -> str | None:
    """Return an action key if text matches a control command, else None."""
    n = _norm(text)
    for pattern, key in _COMMANDS:
        if re.search(pattern, n):
            return key
    return None


def execute(action: str, speak_fn=None) -> bool:
    """
    Run a robot control action.
    speak_fn: optional callable(text) to give audio feedback.
    Returns True if the action was handled.
    """
    try:
        from mode_control import switch_mode
        import web_bridge
    except ImportError as e:
        print(f"⚠️ voice_commands import error: {e}")
        return False

    if   action == "stop":             switch_mode(4)
    elif action == "music_play":       web_bridge.action("music_play")
    elif action == "music_skip":       web_bridge.action("music_skip")
    elif action == "music_stop":       web_bridge.action("music_stop")
    elif action == "mode_keyboard":    switch_mode(1)
    elif action == "mode_autonomous":  switch_mode(3)
    elif action == "mode_line_follow": switch_mode(5)
    elif action == "mode_idle":        switch_mode(4)
    elif action == "mode_watchdog":    switch_mode(6)
    elif action == "mode_lane":        switch_mode(7)
    elif action == "narrate_on":
        import ambient_narration
        ambient_narration.set_enabled(True)
    elif action == "narrate_off":
        import ambient_narration
        ambient_narration.set_enabled(False)
    elif action == "narrate_once":
        import ambient_narration
        ambient_narration.describe_now(block=True)
        print("🎤 Voice command executed: narrate_once")
        return True
    elif action == "photo":
        import camera_actions
        camera_actions.take_photo()
    elif action == "video_start":
        import camera_actions
        camera_actions.start_video()
    elif action == "video_stop":
        import camera_actions
        camera_actions.stop_video()
    elif action == "camera_switch":
        import camera_actions
        cam_id   = camera_actions.cycle_camera()
        cam_name = "the main camera" if cam_id == 0 else "the A I camera"
        if speak_fn:
            speak_fn(f"Switching to {cam_name}.")
        print(f"🎤 Voice command executed: {action}")
        return True
    else:
        return False

    if speak_fn:
        speak_fn(_REPLIES.get(action, "Done."))

    # Sound effects play AFTER she's done talking — speak_fn (kida_chat's
    # piper speak()) blocks until playback finishes, so by this point the
    # reply has already been heard.
    if action == "photo":
        import sfx
        sfx.play("camera_shutter.mp3")
    elif action == "video_start":
        import sfx
        sfx.play("video_reel.mp3")

    print(f"🎤 Voice command executed: {action}")
    return True
