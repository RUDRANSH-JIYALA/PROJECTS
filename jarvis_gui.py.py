import speech_recognition as sr
import pyttsx3
import datetime
import requests
import os
import webbrowser
import time
import pygame
import wikipedia
import cv2
import pywhatkit  
import json
import psutil 
import pyjokes
import pyautogui
import random 
from googletrans import Translator
import platform
import ctypes

# Text-to-Speech

def speak(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speech Error:", e)

# Microphone setup

r = sr.Recognizer()

def listen(timeout=None, phrase_time_limit=8):
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait")
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError:
            speak("Network error for speech recognition.")
            return None
    except sr.WaitTimeoutError:
        print("Listening timed out, no speech detected")
        return None

# Features

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {now}")

def tell_date():
    today = datetime.date.today().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {today}")

def get_news():
    api_key = "35ef6a23786e4605a86685cb2e9e74e0" 
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    try:
        response = requests.get(url).json()
        articles = response.get("articles", [])[:5]
        if articles:
            speak("Here are the top 5 news headlines:")
            for i, art in enumerate(articles, start=1):
                title = art.get("title") or "No title available"
                print(f"\nNews {i}: {title}")
                speak(f"News {i}. {title}")
                time.sleep(1)
        else:
            speak("I couldn't fetch the news.")
    except Exception as e:
        print("Error fetching news:", e)
        speak("Error fetching news.")

def get_weather(city="Greater Noida"):
    api_key = "625b550325045040773a0f3fe18f0c8d"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url).json()
        if response.get("main"):
            temp = response["main"]["temp"]
            desc = response["weather"][0]["description"]
            speak(f"The weather in {city} is {desc} with temperature {temp} degree Celsius.")
        else:
            speak("I couldn't fetch weather data.")
    except Exception:
        speak("Error fetching weather.")

def wikipedia_search(query):
    try:
        topic = query.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        result = wikipedia.summary(topic, sentences=2)
        print(result)
        speak(result)
    except Exception as e:
        print("Wikipedia error:", e)
        speak("Sorry, I couldn't find anything on Wikipedia.")

def play_on_youtube(command):
    song = command.replace("play", "").strip()
    if song:
        speak(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)
    else:
        speak("Please tell me what to play on YouTube.")

# Conversational Memory

MEMORY_FILE = "memory.json"

def remember_fact(key, value):
    data = {}
    if os.path.isfile(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    data[key] = value
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f)

def recall_fact(key):
    if os.path.isfile(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
            return data.get(key)
    return None

# System Control

def system_info():
    cpu = psutil.cpu_percent()
    battery = psutil.sensors_battery()
    speak(f"CPU is at {cpu} percent.")
    if battery:
        speak(f"Battery is at {battery.percent} percent.")

# NEW RELIABLE VOLUME CONTROL

VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF

def _press_vk(vk):
    ctypes.windll.user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.keybd_event(vk, 0, 2, 0)

def control_volume(command):
    os_name = platform.system()
    cmd = command.lower()

    try:
        if os_name == "Windows":
            if "volume up" in cmd:
                _press_vk(VK_VOLUME_UP)
                speak("Volume increased")
            elif "volume down" in cmd:
                _press_vk(VK_VOLUME_DOWN)
                speak("Volume decreased")
            elif "mute volume" in cmd or "unmute volume" in cmd:
                _press_vk(VK_VOLUME_MUTE)
                speak("Volume muted or unmuted")
            else:
                speak("Specify volume up , volume down or mute volume for volume control.")
            return

        else:
            pyautogui.press("volumeup")
            speak("Fallback volume control used.")
    except Exception as e:
        print("Volume control error:", e)
        speak("Volume control failed.")


# Opening Any Apps

def open_app_or_website(command):
    apps_sites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://www.github.com",
        "notepad": "notepad.exe",
        "calculator": "calc.exe"
    }
    for key, val in apps_sites.items():
        if key in command:
            speak(f"Opening {key}")
            if val.startswith("http"):
                webbrowser.open(val)
            else:
                os.startfile(val)
            return
    speak("Sorry, I don't recognize that app or site.")


# Entertainment

def tell_joke():
    joke = pyjokes.get_joke()
    print(f"\n Joke: {joke}\n")
    speak(joke)
    time.sleep(2)  


def tell_quote():
    quotes = [
        "The best way to predict the future is to create it.",
        "Believe you can and you're halfway there.",
        "Success is not in what you have, but who you are.",
        "Happiness is not something ready made. It comes from your own actions.",
        "The only limit to our realization of tomorrow is our doubts of today."
    ]
    quote = random.choice(quotes)
    print(f"\n Quote: {quote}\n")
    speak(quote)
    time.sleep(2)  

# Music Player

pygame.mixer.init()
playlist = []
current_index = -1

def play_music(file_path):
    global playlist, current_index
    if os.path.isfile(file_path):
        if file_path not in playlist:
            playlist.append(file_path)
        current_index = playlist.index(file_path)
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
    else:
        speak("File not found. Please check the path.")

def stop_music():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        speak("Music stopped.")
    else:
        speak("No music is playing.")

def play_next():
    global current_index
    if playlist and current_index < len(playlist) - 1:
        current_index += 1
        play_music(playlist[current_index])
    else:
        speak("No next song in playlist.")

def play_previous():
    global current_index
    if playlist and current_index > 0:
        current_index -= 1
        play_music(playlist[current_index])
    else:
        speak("No previous song in playlist.")

# Alarm

def set_alarm(alarm_time, alarm_file):
    speak(f"Alarm set for {alarm_time}")
    while True:
        current_time = datetime.datetime.now().strftime("%H:%M")
        if current_time == alarm_time:
            if os.path.isfile(alarm_file):
                pygame.mixer.music.load(alarm_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(1)
            else:
                speak("Alarm file not found.")
            break
        time.sleep(10)

# Face Detection 

def detect_face():
    speak("Opening camera for face detection.")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    detected_once = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            if not detected_once:
                speak("I see a person in front of me.")
                detected_once = True

        cv2.imshow("Camera", frame)
        if time.time() - start_time > 25:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    speak("Camera closed.")

# Speech Translation

translator = Translator()

def translate_speech(text, dest_lang="fr"):
    try:
        result = translator.translate(text, dest=dest_lang)
        print(f"Translated ({dest_lang}):", result.text)
        speak(result.text)
    except Exception as e:
        print("Translation Error:", e)
        speak("Sorry, translation failed.")

#  Main 
def main():
    speak("Hello, I am Jarvis. How can I help you?")

    while True:
        txt = listen(timeout=5, phrase_time_limit=8)
        if txt is None:
            continue

        if "time" in txt:
            tell_time()
        elif "date" in txt:
            tell_date()
        elif "news" in txt:
            get_news()
        elif "weather" in txt:
            speak("Which city?")
            city = listen(timeout=5, phrase_time_limit=5)
            if city:
                get_weather(city)
            else:
                speak("I didn't catch the city name.")
        elif "play music" in txt:
            file_path = "C:/Users/Rudransh/Downloads/jarvis sounds/back_in_black.mp3"
            play_music(file_path)
        elif "stop music" in txt or "stop" in txt:
            stop_music()
        elif "next" in txt:
            play_next()
        elif "previous" in txt:
            play_previous()
        elif "open" in txt:
            open_app_or_website(txt)
        elif "cpu" in txt or "battery" in txt:
            system_info()
        elif "volume" in txt:
            control_volume(txt)
        elif "set alarm" in txt:
            alarm = input("Enter time (HH:MM): ").strip()
            alarm_file = "C:/Users/Rudransh/Downloads/j_a_r_v_i_s_alarm.mp3"
            set_alarm(alarm, alarm_file)
        elif "who is in front of me" in txt or "face detection" in txt:
            detect_face()
        elif "joke" in txt or "tell me a joke" in txt:
            tell_joke()
        elif "quote" in txt or "motivate me" in txt:
            tell_quote()
        elif "remember" in txt:
            speak("What should I remember?")
            fact = listen()
            if fact:
                speak("Give me a key to save this under.")
                key = listen()
                if key:
                    remember_fact(key, fact)
                    speak(f"I have remembered {fact} under key {key}.")
        elif "recall" in txt:
            speak("Which key should I recall?")
            key = listen()
            if key:
                fact = recall_fact(key)
                if fact:
                    speak(f"I remember {fact} under {key}.")
                else:
                    speak(f"No memory found for {key}.")
        elif "who is" in txt or "what is" in txt or "tell me about" in txt:
            wikipedia_search(txt)
        elif "open" in txt:
            open_app_or_website(txt)
        elif "play" in txt:
            play_on_youtube(txt)
        elif "translate" in txt:
            speak("What should I translate?")
            phrase = listen()
            if phrase:
                speak("Which language? For example, 'fr' for French.")
                lang = listen()
                if lang:
                    translate_speech(phrase, dest_lang=lang)
        elif "exit" in txt or "quit" in txt or "shut down" in txt:
            speak("Goodbye!")
            break
        else:
            speak("Sorry, I didn't understand that.")

if __name__ == "__main__":
    main()

