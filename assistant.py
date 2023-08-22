import pyttsx3
import datetime
import requests
import json
import speech_recognition as sr

apiKey = "a76b879d7578a0221a142c42b628f930"
ct = datetime.datetime.now()

engine = pyttsx3.init()


def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            speak("Recognising...")
            Query = r.recognize_google(audio, language='en-in')
        except Exception as e:
            print(e)
            return "None"

    return Query


def get_weather(city):
    url_city = f"http://api.openweathermap.org/geo/1.0/direct?q={city.upper()}&appid={apiKey}"
    city_response = requests.get(url_city)
    city_data = city_response.json()

    lat = city_data[0]["lat"]
    lon = city_data[0]["lon"]

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apiKey}"
    response = requests.get(url)
    data = response.json()
    return f"In {city.capitalize()}, the temperature is {round(data['main']['temp']) - 273} degrees which feels like {round(data['main']['feels_like']) - 273} degrees and humidity is {data['main']['humidity']}%"


def read_todo_list():
    try:
        with open('todo.txt', 'r') as file:
            content = file.read()
            if content == "":
                speak("There's nothing in the todo list")
                return
            speak("Here's the todo list.")
            speak(content)

        file.close()
    except FileNotFoundError:
        speak("File not found.")


def add_items():
    try:
        with open('todo.txt', 'a') as file:
            while (True):
                speak("What do you want to add?")
                item = listen()
                file.write(item + "\n")
                speak("Do you want to add anything else?")
                choice = listen()
                if "YES" in choice.upper():
                    continue
                else:
                    speak("Ok")
                    break
        file.close()
    except FileNotFoundError:
        speak("File not found.")


speak("Hello sir, how may I help you?")

failure_counter = 0

while (True):
    comm = listen()
    if "time" in comm:
        speak(f"The time is {ct.hour} {ct.minute}")

    elif "weather" in comm:
        speak("Which city's weather do you wanna know?")
        city = listen()
        weather = get_weather(city)
        speak(weather)

    elif "LIST" in comm.upper():
        speak("Do you want to read the todo list or add a new item?")
        choice = listen()
        if "read" in choice:
            read_todo_list()
        elif ("add" or "write") in choice:
            add_items()
        else:
            pass
    elif ("EXIT" or "QUIT" or "TERMINATE") in comm.upper():
        speak("Have a nice day sir.")
        break
    elif ("stop listening" or "pause") in comm:
        speak("Ok, press any key to enable listening.")
        n = input("Press any key to enable listening.")
        continue
    else:
        speak("Sorry, I don't know about this.")
        failure_counter += 1
        if failure_counter == 3:
            speak("Exiting program because of too many failed attempts.")
            break
