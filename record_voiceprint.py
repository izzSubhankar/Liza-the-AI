import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

print("🎙️ Recording your voice print in 3 seconds. Say: 'Access Granted'")
sd.sleep(3000)
print("Recording...")
my_recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()

write("voiceprint.wav", fs, my_recording)
print("✅ Voiceprint saved to voiceprint.wav")
