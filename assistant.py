import pyttsx3
import datetime
import requests
import json
import speech_recognition as sr
import os
from dotenv import load_dotenv

load_dotenv()

apiKey = os.getenv("apikey")
ct = datetime.datetime.now()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_BASE_URL = 'https://newsapi.org/v2/top-headlines'
params = {
    'country': 'in',
    'category': 'general',
    'apiKey': NEWS_API_KEY
}

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
            # speak("Recognising...")
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
                file.write(item.upper() + "\n")
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


def remove_items():
    try:
        with open('todo.txt', 'r') as file:
            content = file.read()
            while (True):
                speak("What do you want to remove?")
                item = listen()
                if item.upper() in content:
                    modified_content = content.replace(item.upper(), '')
                    with open('todo.txt', 'w') as file:
                        file.write(modified_content)
                        speak(f"Removed {item} from the list")
                        file.close()
                    break
                else:
                    speak("Item is not in the list.")
                speak("Do you want to remove anything else?")
                choice = listen()
                if "YES" in choice.upper():
                    continue
                else:
                    speak("Ok")
                    break
        file.close()
    except FileNotFoundError:
        speak("File not found.")


def greet():
    if 4 <= ct.hour <= 12:
        return "Good morning sir"
    elif 12 < ct.hour <= 17:
        return "Good afternoon sir"
    elif 17 < ct.hour <= 11:
        return "Good evening sir"
    else:
        return "Hello sir"


def get_news():
    response = requests.get(NEWS_BASE_URL, params=params)
    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles']
        count = 0
        for article in articles:
            title = article['title']
            description = article['description']
            source = article['source']['name']
            print(
                f"From {source}. Title: {title}. Description: {description}.")
            speak(
                f"From {source}. Title: {title}. Description: {description}.")
            count += 1
            if count == 3:
                break
    else:
        print("Error fetching news:", response.status_code)


speak(f"{greet()}, how may I help you?")

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
        speak("Do you want to read the todo list or add a new item or remove an item?")
        choice = listen()
        if "read" in choice:
            read_todo_list()
        elif "add" in choice:
            add_items()
        elif "remove" in choice:
            remove_items()
        else:
            speak("Function not found.")
            pass
    elif "NEWS" in comm.upper():
        get_news()
    elif ("EXIT" or "QUIT" or "TERMINATE") in comm.upper():
        speak("Have a nice day sir.")
        break
    elif ("stop" or "stop listening" or "pause") in comm:
        speak("Ok, press any key to enable listening.")
        n = input("Press any key to enable listening.")
        continue
    else:
        speak("Sorry, I don't know about this.")
        failure_counter += 1
        if failure_counter == 3:
            speak("Exiting program because of too many failed attempts.")
            break
