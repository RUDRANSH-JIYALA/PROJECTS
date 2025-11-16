JARVIS – A Python Voice Assistant

A fully functional, offline-capable and internet-powered AI assistant built with Python.

Overview

JARVIS is an advanced Python-based voice assistant that performs tasks using speech recognition and text-to-speech. It supports system control, automation, online queries, file and music operations, system monitoring, face detection, translation, alarms, YouTube playback, Wikipedia search, and more.
This project combines multiple Python libraries to create an interactive desktop AI assistant similar to Iron Man’s Jarvis.

Features
Voice Interaction

Converts speech to text using the SpeechRecognition library

Produces realistic speech responses using pyttsx3

Date and Time

Announces the current system time

Provides today’s date

Weather Information

Retrieves current weather and temperature using the OpenWeatherMap API

News Headlines

Fetches the top five latest news headlines using NewsAPI

Wikipedia Search

Provides short summaries for questions such as “who is”, “what is”, and “tell me about”

YouTube Playback

Plays songs or videos directly on YouTube using pywhatkit

System Monitoring

Reports CPU usage

Announces battery percentage using psutil

Hardware Volume Control (Windows)

Volume up

Volume down

Mute and unmute

Implemented using ctypes and virtual key codes

Application and Website Launcher

Supports commands such as:

open google

open calculator

open notepad

open youtube

Offline Music Player

Plays local MP3 files

Supports next, previous, and stop

Maintains a playback playlist

Alarm System

Allows setting custom alarm times

Triggers alarm sound automatically

Entertainment

Tells random jokes using pyjokes

Provides motivational quotes

Local Memory System

Stores user-defined facts in memory.json

Recalls stored information on request

Face Detection

Detects faces using OpenCV and Haarcascade classifiers

Highlights faces with bounding boxes

Speech Translation

Translates spoken sentences into other languages using googletrans

Project Structure
JARVIS/
│── jarvis.py
│── memory.json
│── requirements.txt
│── README.md
│── assets/
│     └── alarm.mp3

Requirements

Install all dependencies using:

pip install -r requirements.txt

Libraries Used

speech_recognition

pyttsx3

requests

wikipedia

pygame

opencv-python

psutil

googletrans

pyjokes

pyautogui

pywhatkit

json

ctypes

platform

random

datetime

Setup Instructions
Step 1: Clone the Repository
git clone https://github.com/RUDRANSH-JIYALA/PROJECTS.git
cd RUDRANSH-JIYALA

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Add API Keys

Replace the placeholder keys inside the script:

news_api_key ="35ef6a23786e4605a86685cb2e9e74e0"
weather_api_key ="625b550325045040773a0f3fe18f0c8d"

Step 4: Run the Assistant
python jarvis.py

How to Use
General Commands

what time is it

tell me today’s date

tell me a joke

Online Commands

give me the latest news

what is the weather in Bangalore

who is Albert Einstein

Action Commands

play believer on youtube

open google

open notepad

Music Player Commands

play music

stop music

next song

previous song

System Status

cpu usage

battery status

Face Detection

who is in front of me

start face detection

Translation

translate this

Key Code Components
Speech-to-Text
r = sr.Recognizer()
audio = r.listen(source)
command = r.recognize_google(audio)

Text-to-Speech
engine = pyttsx3.init()
engine.say("Hello")
engine.runAndWait()

Weather API
url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"

News API
url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={key}"

Music Playback
pygame.mixer.music.load(file)
pygame.mixer.music.play()

Persistent Memory
data[key] = value
json.dump(data, f)

Face Detection
face_cascade.detectMultiScale(gray, 1.3, 5)

Future Improvements

Graphical user interface using Tkinter or PyQt

Integration with ChatGPT API for more intelligent responses

Email automation

Gesture-based controls

Hotword detection (always-on “Hey Jarvis”)

WhatsApp messaging automation
