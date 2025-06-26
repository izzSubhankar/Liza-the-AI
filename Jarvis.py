import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import wikipedia
import pyjokes
import pyautogui
import requests
import time
import psutil
import random
from scipy.io.wavfile import read, write
import numpy as np
import sounddevice as sd  

# ========== VOICE LOCK ==========
import sounddevice as sd
from scipy.io.wavfile import write, read
import numpy as np

def verify_voice():
    fs = 44100
    seconds = 3

    print("🔒 Voice verification activated.")
    speak("I need to verify your voice.")

    print("🎙️ Listening for your password now...")
    speak("Please speak your voice password.")
    time.sleep(1)
    print("Now !")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()

    write("temp_input.wav", fs, recording)

    try:
        _, ref = read("voiceprint.wav")
        _, sample = read("temp_input.wav")

        ref = ref.astype(np.float32).flatten()
        sample = sample.astype(np.float32).flatten()

        if len(ref) != len(sample):
            min_len = min(len(ref), len(sample))
            ref = ref[:min_len]
            sample = sample[:min_len]

        similarity = np.dot(ref, sample) / (np.linalg.norm(ref) * np.linalg.norm(sample))
        print(f"🔍 Similarity score: {similarity:.2f}")
        return similarity > 0.01  # Set your desired threshold here
    except Exception as e:
        print(f"❌ Voice lock error: {e}")
        return False


# ========== TTS ==========
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 175)

def speak(text):
    print(f"LIZA: {text}")
    engine.say(text)
    engine.runAndWait()

# ========== ASSISTANT ==========
def wish_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am LIZA, your Girlfriend Assistant. How can I help you today?")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        command = r.recognize_google(audio, language='en-in')
        print(f"You said: {command}")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
        return "None"
    except sr.RequestError:
        speak("Could not connect to the recognition service.")
        return "None"
    return command.lower()

def get_weather(city):
    speak(f"Fetching weather for {city}.")
    try:
        res = requests.get(f"https://wttr.in/{city}?format=3")
        speak(res.text)
    except:
        speak("Unable to fetch weather details.")

def write_note():
    speak("What should I write in your note?")
    note = take_command()
    with open("note.txt", "a") as f:
        f.write(f"{datetime.datetime.now()}: {note}\n")
    speak("I've written your note.")

def clear_notes():
    open("note.txt", "w").close()
    speak("All notes have been cleared.")

def calculate(expression):
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

def battery_status():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        speak(f"Battery is at {percent} percent")
        if battery.power_plugged:
            speak("Your system is charging.")
        else:
            speak("You are running on battery.")
    else:
        speak("Cannot retrieve battery status.")

def tell_fact():
    facts = [
        "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs.",
        "Octopuses have three hearts.",
        "Bananas are berries, but strawberries are not.",
        "A group of flamingos is called a flamboyance.",
        "There's enough DNA in the human body to stretch from the sun to Pluto and back — 17 times."
    ]
    speak(random.choice(facts))

def execute_command(command):
    if 'time' in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {time_now}")

    elif 'date' in command:
        date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today is {date}")

    elif 'wikipedia' in command:
        speak("Searching Wikipedia...")
        query = command.replace("wikipedia", "")
        try:
            result = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            speak(result)
        except:
            speak("No results found on Wikipedia.")

    elif 'joke' in command:
        speak(pyjokes.get_joke())

    elif 'open youtube' in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif 'open google' in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    elif 'open downloads' in command:
        os.startfile(os.path.join(os.path.expanduser("~"), "Downloads"))
        speak("Opening Downloads folder.")

    elif 'open documents' in command:
        os.startfile(os.path.join(os.path.expanduser("~"), "Documents"))
        speak("Opening Documents folder.")

    elif 'open vs code' in command:
        path = r"C:\Users\YourUserName\AppData\Local\Programs\Microsoft VS Code\Code.exe"  # Change this
        os.startfile(path)
        speak("Opening Visual Studio Code.")

    elif 'weather in' in command:
        city = command.split("in")[-1].strip()
        get_weather(city)

    elif 'write a note' in command:
        write_note()

    elif 'clear notes' in command:
        clear_notes()

    elif 'calculate' in command:
        expression = command.replace("calculate", "").strip()
        calculate(expression)

    elif 'search' in command:
        query = command.replace("search", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif 'ip address' in command:
        ip = requests.get('https://api.ipify.org').text
        speak(f"Your IP address is {ip}")

    elif 'screenshot' in command:
        filename = f"screenshot_{int(time.time())}.png"
        pyautogui.screenshot(filename)
        speak(f"Screenshot saved as {filename}")

    elif 'battery' in command:
        battery_status()

    elif 'fact' in command:
        tell_fact()

    elif 'shutdown' in command or 'exit' in command:
        speak("Goodbye! Shutting down.")
        exit()

    else:
        speak("I'm not trained for that yet.")

# ========== MAIN ==========
def main():
    # 🔁 Keep verifying until granted
    while True:
        if verify_voice():
            speak(" Access granted. Welcome back!")
            break
        else:
            speak(" Access denied. Please try again.")
            print(" Retrying...")

    # 💻 Assistant starts
    wish_user()
    while True:
        command = take_command()
        if command != "None":
            execute_command(command)

if __name__ == "__main__":
    main()
