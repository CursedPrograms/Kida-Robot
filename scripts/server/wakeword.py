import whisper
import sounddevice as sd
import numpy as np
import time
import os

DURATION = 3  # seconds
SAMPLE_RATE = 16000
THRESHOLD_PHRASE = "hey kida"

# Load Whisper model (use "tiny" for speed on Pi)
model = whisper.load_model("tiny")

def record_audio(duration=DURATION, fs=SAMPLE_RATE):
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    audio = np.squeeze(audio)
    return (audio * 32767).astype(np.int16)

def save_wav(audio, filename, fs=SAMPLE_RATE):
    from scipy.io.wavfile import write
    write(filename, fs, audio)

def listen_for_wakeword():
    while True:
        audio = record_audio()
        save_wav(audio, "chunk.wav")

        try:
            result = model.transcribe("chunk.wav", fp16=False)
            text = result["text"].lower().strip()
            print(f"🧠 Heard: {text}")

            if THRESHOLD_PHRASE in text:
                print("🚨 Wake word detected! Running main script...")
                os.system("python3 main.py")  # Replace with actual action
                break
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(0.5)

if __name__ == "__main__":
    listen_for_wakeword()
