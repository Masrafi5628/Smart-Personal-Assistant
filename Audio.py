'''
tts=gTTS(text='Sabbir Ahmed from department of cse',lang='en')
filename='hello.mp3'
tts.save(filename)
playsound('hello.mp3')
'''
'''
import pyttsx3
friend=pyttsx3.init()
friend.setProperty('rate',130)
friend.setProperty('voices',0.8)
friend.say('Ashik from department of cse')
friend.runAndWait()
'''
import datetime
import time
for i in range(4):
    cur_time=datetime.datetime.now()
    time_set = cur_time.strftime("%H:%M")
    date_set = cur_time.strftime("%m/%d/%y")
    print(date_set,time_set)