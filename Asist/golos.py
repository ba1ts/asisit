import speech_recognition as sr
import pyttsx3
import time
from fuzzywuzzy import fuzz
import datetime
from tkinter import * 
import golos2
import subprocess
import os
from translate import Translator
import webbrowser
import re
import pyglet
import random
import web

spek=pyttsx3.init()
def speak(text):
    print(text)
    spek.say(text)
    spek.runAndWait()

opts = {
    "TimeTimes": ('минута','минуты','минуту','минут'),
    "TimeSeconds":('секунд','секунду','секунды','секунда'),
    "alias": ('candy','кеша','геннадий','гена'),
    "cmds": {
        "ctime": ('время','час','время','время','времени'),
        "kalkulater": ('+','-','/','х'),
        "perevod": ('переведи','перевод'),
        "Poisk":('google', 'поиск', 'найти'),
        "Timer":('засеки таймер','таймер'),
        "game": ('змейка игра игру'),
        "dol": ('курс', 'доллара', 'долара', 'доллар', 'долар', '$'),
        "monetka": ('подкинь' 'монетку' 'подкинуть','кинь')
    }
}

def rec():
    global kal
    r=sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        audio = r.listen(source)
    try:
        voice = r.recognize_google(audio, language = "ru-RU").lower()
        print("[log] "+ voice)

        cmd = voice
        for x in opts['alias']:
            cmd=kal= cmd.replace(x, "").strip()

        cmd = recognize_cmd(cmd)
        funck(cmd['cmd'])

    except sr.UnknownValueError:
        rec
    except sr.RequestError as e:
        speak("[log] Неизвестная ошибка, проверьте интернет или код!")
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC
def funck(cmd):
    if cmd == "Poisk":
        speak("что вы хотите узнать?")
        r=sr.Recognizer()
        with sr.Microphone(device_index = 1) as source:
            audio = r.listen(source)
        lok = r.recognize_google(audio, language = "ru-RU").lower()
        webbrowser.open('https://yandex.ru/search/?text=' + lok)
    elif cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'kalkulater':
        print(kal)
        kaling = kal.replace('и','') 
        kaling1 = kaling.replace('х','*')
        summa = eval(kaling1)
        speak(summa)
    elif cmd == "perevod":
        r=sr.Recognizer()
        speak("что перевести?")
        with sr.Microphone(device_index = 1) as source:
            audio = r.listen(source)
        perevodim = r.recognize_google(audio, language = "ru-RU").lower()
        print (perevodim)
        translator= Translator(from_lang="russian",to_lang="English")
        translation = translator.translate(perevodim) 
        speak(translation)
    elif cmd == "Timer":
        speak("на какое время поставить таймер")
        r=sr.Recognizer()
        with sr.Microphone(device_index = 1) as source:
            audio = r.listen(source)
        times = r.recognize_google(audio, language = "ru-RU").lower()
        print("[log]"+ times)
        for x in opts['TimeTimes']:
            min = times.split(x)[0]
        for y in opts['TimeTimes']:
            sec = times.split(y)[-1]
            for z in opts['TimeSeconds']:
                sec = sec.split(z)[0]
                sec = re.sub('\D', '', sec)
        min= int(min) * 60
        timerING = int(min) + int(sec)
        speak("вы поставили таймер на: "+ str(timerING) + " секунды")
        time.sleep(int(timerING))
        speak("Тймер завершён")
    elif cmd == "monetka":
        mon = random.randint(1, 2)
        if mon == 1:
            speak("Орёл")
        else:
            speak("Решка")
    elif cmd == "dol":
        subprocess.Popen('python Dolar.py')
    elif cmd == "game":
        subprocess.Popen('python game.py')
    else:
        print("что вы хотите")
        rec
    subprocess.Popen('python golos2.py')
   

    




