import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import select
import sys
import queue
import time


CHANNELS = 1


def _detect_mic():
    """
    Pick a real capture device and a sample rate it will actually open at.

    This box's /etc/asound.conf defines `pcm.!default` as a null sink, so
    PortAudio's "default"/"pulse" pseudo-devices silently capture near-
    silence instead of raising an error — the wake word was never heard
    because we were transcribing dead air. The USB dongle mic itself also
    only accepts 44.1k/48k natively, not Whisper's preferred 16k, so probe
    for a rate it supports; common/audio_utils.load_audio() resamples to
    16k via ffmpeg when the WAV is loaded for transcription anyway.
    """
    try:
        devices = sd.query_devices()
    except Exception:
        return None, 16000

    real = [(i, d) for i, d in enumerate(devices)
            if d["max_input_channels"] > 0 and d["name"] not in ("pulse", "default")]
    usb = [pair for pair in real if "usb" in pair[1]["name"].lower()]
    device_index = (usb or real or [(None, None)])[0][0]

    for rate in (16000, 44100, 48000, 22050, 32000, 8000):
        try:
            sd.check_input_settings(device=device_index, samplerate=rate, channels=CHANNELS)
            return device_index, rate
        except Exception:
            continue
    return device_index, 16000


DEVICE_INDEX, SAMPLE_RATE = _detect_mic()
print(f"🎙️  Mic input: device {DEVICE_INDEX} @ {SAMPLE_RATE}Hz "
      f"({sd.query_devices(DEVICE_INDEX)['name'] if DEVICE_INDEX is not None else 'none found'})")


def enter_pressed():
    # select() on a non-tty stdin (e.g. /dev/null under a systemd service
    # with no controlling terminal) reports "ready" immediately and forever,
    # which used to make this fire on the very first check every time —
    # recording 0 frames in a tight infinite loop that hammered the shared
    # audio device and starved every other audio path (TTS, music). Only
    # honor the early-stop keypress when stdin is an actual terminal.
    if not sys.stdin.isatty():
        return False
    return select.select([sys.stdin], [], [], 0.0)[0]

def record_audio(duration, audio_path):
    """
    Record audio from the microphone and save it as a WAV file. The user has the possibility to stop the recording earlier by pressing Enter on the keyboard.

    Args:
        duration (int): Duration of the recording in seconds.

    Returns:
        np.ndarray: Recorded audio data.
    """
    q = queue.Queue()
    recorded_frames = []
    interactive = sys.stdin.isatty()

    def audio_callback(indata, frames, time_info, status):
        if status:
            print("Status:", status)
        q.put(indata.copy())

    print(f"Recording for up to {duration} seconds. Press Enter to stop early...")

    start_time = time.time()
    with sd.InputStream(samplerate=SAMPLE_RATE,
                        channels=CHANNELS,
                        dtype="float32",
                        device=DEVICE_INDEX,
                        callback=audio_callback):
        if interactive:
            # Set stdin to non-blocking line-buffered mode
            sys.stdin = open('/dev/stdin')
        while True:
            if time.time() - start_time >= duration:
                print("Max duration reached.")
                break
            if enter_pressed():
                sys.stdin.read(1)  # consume the newline
                print("Early stop requested.")
                break
            try:
                frame = q.get(timeout=0.1)
                recorded_frames.append(frame)
            except queue.Empty:
                continue

    print("Recording finished. Processing...")

    if not recorded_frames:
        audio_data = np.zeros(0, dtype="float32")
    else:
        audio_data = np.concatenate(recorded_frames, axis=0)
        if audio_data.ndim > 1:
            audio_data = np.mean(audio_data, axis=1)

    wav.write(audio_path, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))
    return audio_data
