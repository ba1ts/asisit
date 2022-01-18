import speech_recognition as sr
from golos import rec
import time
import pyttsx3
spek=pyttsx3.init()
opts = {
    "alias": ('candy','кеша','геннадий','гена')}
global gov

def speak(text):
    print(text)
    spek.say(text)
    spek.runAndWait()

def slyx():
    print("по факту")
    r=sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        audio = r.listen(source)
    print("вызови меня")

    try:
        gov = r.recognize_google(audio, language = "ru-RU").lower()
    except:
        print(".")
        slyx()


    if gov.startswith(opts["alias"]): 
        speak("говорите")
        rec()
        return gov
        print(gov)
    else:
        slyx()

slyx()
