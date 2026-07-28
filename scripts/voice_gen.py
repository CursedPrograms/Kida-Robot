#!/usr/bin/env python3
# voice_gen.py — type text, hear it in KIDA's Piper voice, save an .mp3
#
# Usage:
#   python3 scripts/voice_gen.py                        interactive REPL
#   python3 scripts/voice_gen.py "text to speak"         one-shot, auto filename
#   python3 scripts/voice_gen.py "text" --name mode_watchdog
#       Saves/overwrites audio/voiceovers/mode_watchdog.mp3 — use this to
#       hand-author or re-record one of the cached lines voice_engine.py
#       plays automatically (mode_<name>.mp3, vibration_alert.mp3, ...).

import argparse
import os
import sys

import voice_engine


def generate(text: str, name: str | None = None, play: bool = True) -> str:
    """Synthesize text to audio/voiceovers/<name or slug>.mp3, return the path."""
    key = name or voice_engine.slugify(text)
    path = os.path.join(voice_engine.VOICE_DIR, f"{key}.mp3")
    if not voice_engine.synthesize(text, path):
        raise RuntimeError("Piper synthesis failed — check the piper binary/model path")
    print(f"💾 Saved: {path}")
    if play:
        voice_engine.play_file(path, block=True)
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Type text, hear it in KIDA's voice, save as .mp3 in audio/voiceovers/"
    )
    parser.add_argument("text", nargs="?", help="Text to speak (omit for interactive mode)")
    parser.add_argument("--name", help="Save as this filename instead of an auto slug "
                                        "(e.g. --name mode_watchdog)")
    parser.add_argument("--no-play", action="store_true", help="Don't play it back after saving")
    args = parser.parse_args()

    if args.text:
        generate(args.text, name=args.name, play=not args.no_play)
        return

    print("=" * 50)
    print("  🔊 KIDA voice generator")
    print(f"  Voice     : {os.path.basename(voice_engine.PIPER_MODEL)}")
    print(f"  Saving to : {voice_engine.VOICE_DIR}")
    print("  Ctrl+C to quit")
    print("=" * 50 + "\n")

    while True:
        try:
            text = input("Say: ").strip()
            if not text:
                continue
            name = input("  Save as (blank = auto name): ").strip() or None
            generate(text, name=name, play=True)
            print()
        except KeyboardInterrupt:
            print("\n\nBye!")
            sys.exit(0)


if __name__ == "__main__":
    main()
