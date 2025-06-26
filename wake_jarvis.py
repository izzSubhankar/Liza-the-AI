import sounddevice as sd
import queue
import json
import os
from vosk import Model, KaldiRecognizer
from Jarvis import execute_command, speak, take_command  # Import all from your assistant

# Path to your Vosk model folder
model_path = "vosk-model-small-en-in-0.4"

# Wake words you want to support
wake_words = ["hey jarvis", "ok jarvis", "hello jarvis"]

# Queue for live audio data
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(f"[ERROR] Audio input issue: {status}")
    q.put(bytes(indata))

def listen_for_wake_word():
    if not os.path.exists(model_path):
        print("❌ Model not found. Download from https://alphacephei.com/vosk/models and place it correctly.")
        exit(1)

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    print("🔉 JARVIS is now passively listening. Say 'Hey Jarvis' to activate.")

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=audio_callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()
                if text.strip() != "":
                    print(f"🗣️ Heard: {text}")

                # Wake word detected
                if any(wake_word in text for wake_word in wake_words):
                    speak("Yes, I'm listening.")
                    command = take_command()
                    if command and command != "None":
                        if "stop" in command or "exit" in command:
                            speak("Shutting down. Goodbye.")
                            break
                        execute_command(command)
                    print("🛑 Returning to passive listening...")

if __name__ == "__main__":
    try:
        listen_for_wake_word()
    except KeyboardInterrupt:
        print("\n🔌 Program stopped manually.")
    except Exception as e:
        print(f"❗ Unexpected error: {e}")
