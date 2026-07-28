#!/usr/bin/env python3
"""Standalone mic/STT diagnostic tool.

Loops recording short snippets and runs them through the exact same
Hailo-8L Whisper pipeline kida_chat_wakeword.py uses, printing (and logging
to wakeword_debug.log) the raw mic level, the post-gain level, whether VAD
found speech, the transcript Whisper actually produced, and whether it
would have matched a wake word. Talk normally while this runs so you can
see what's really reaching Whisper instead of guessing.

Run:  python3 scripts/debug_wakeword.py
Stop: Ctrl+C
Watch the log from another terminal: tail -f scripts/wakeword_debug.log
"""

import os
import sys
import time
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path
from datetime import datetime

import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(BASE_DIR))

from hailo_whisper_pipeline import HailoWhisperPipeline
from common.audio_utils import load_audio
from common.preprocessing import preprocess, improve_input_audio
from common.postprocessing import clean_transcription
from common.record_utils import record_audio

WHISPER_VARIANT = "base"
SCAN_DURATION   = 3.0   # seconds per snippet — matches kida_chat_wakeword's WAKE_DURATION
AUDIO_PATH = str(BASE_DIR / "audio" / "snippets" / "debug_wake_snippet.wav")
LOG_PATH   = str(BASE_DIR / "logs" / "wakeword_debug.log")

ENCODER_HEF = str(BASE_DIR / "resources/hefs/h8l/base/base-whisper-encoder-5s_h8l.hef")
DECODER_HEF = str(BASE_DIR / "resources/hefs/h8l/base/base-whisper-decoder-fixed-sequence-matmul-split_h8l.hef")

WAKE_WORDS = {
    "kida", "hi kida", "hey kida", "okay kida", "ok kida",
    "kira", "hi kira", "hey kira", "okay kira", "ok kira",
    "robot", "hi robot", "hey robot", "okay robot", "ok robot",
}


def _contains_wake_word(text: str) -> bool:
    t = text.lower().strip()
    return any(ww in t for ww in WAKE_WORDS)


def log(line: str, fh) -> None:
    print(line)
    fh.write(line + "\n")
    fh.flush()


def main():
    for p in (ENCODER_HEF, DECODER_HEF):
        if not os.path.exists(p):
            print(f"HEF not found: {p}")
            sys.exit(1)

    print(f"Loading Hailo-8L Whisper ({WHISPER_VARIANT})...")
    pipeline = HailoWhisperPipeline(
        encoder_model_path=ENCODER_HEF,
        decoder_model_path=DECODER_HEF,
        variant=WHISPER_VARIANT,
        multi_process_service=True,
    )
    print(f"Ready. Recording {SCAN_DURATION}s snippets in a loop — talk whenever. Ctrl+C to stop.")
    print(f"Logging to {LOG_PATH}")

    with open(LOG_PATH, "a") as fh:
        log(f"\n=== session start {datetime.now().isoformat(timespec='seconds')} ===", fh)
        try:
            while True:
                raw = record_audio(SCAN_DURATION, audio_path=AUDIO_PATH)
                raw_peak = float(np.max(np.abs(raw))) if len(raw) else 0.0

                audio = load_audio(AUDIO_PATH)
                audio, start_time = improve_input_audio(audio, vad=True)
                boosted_peak = float(np.max(np.abs(audio))) if len(audio) else 0.0
                chunk_offset = max(0.0, (start_time or 0.0) - 0.2)

                mel_spectrograms = preprocess(
                    audio, is_nhwc=True, chunk_length=5, chunk_offset=chunk_offset
                )

                texts = []
                for mel in mel_spectrograms:
                    pipeline.send_data(mel)
                    time.sleep(0.1)
                    raw_text = pipeline.get_transcription()
                    cleaned = clean_transcription(raw_text)
                    if cleaned:
                        texts.append(cleaned)
                transcript = " ".join(texts).strip()

                ts = datetime.now().strftime("%H:%M:%S")
                matched = _contains_wake_word(transcript) if transcript else False
                speech = f"{start_time:.2f}s" if start_time is not None else "none"

                log(
                    f"[{ts}] raw_peak={raw_peak:.3f} boosted_peak={boosted_peak:.3f} "
                    f"speech_detected={speech} transcript={transcript!r} "
                    f"wake_word_match={matched}",
                    fh,
                )
        except KeyboardInterrupt:
            log(f"=== session end {datetime.now().isoformat(timespec='seconds')} ===", fh)
            pipeline.stop()
            print("\nStopped.")


if __name__ == "__main__":
    main()
