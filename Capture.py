import tkinter.filedialog
from tkinter import *
import cv2
import datetime
import time
import schedule
import tkinter.messagebox as msg
import face_recognition as fc
import csv
import os
from gtts import gTTS
from playsound import playsound
import numpy as np
import time
from PIL import Image,ImageTk
import How_many_image
import alarm_control
from alarm_control import *

def capta():

    s=[]
    t=[]
    all = []
    dictData = {}
    with open("Data.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # if(dictData[row[0]]): // if name already exists
            dictData[row[0]] = (row[1], row[2], row[5])
        file.close()
    print(dictData)
    path = '/home/ashik/PycharmProjects/smartParsonalAssistant/Images'
    images = []
    classNames = []
    myList = os.listdir(path)  # file names in directory
    print(myList)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}')  # reads image file cl from path
        images.append(curImg)
        name = os.path.splitext(cl)[0]
        classNames.append(name)
    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = fc.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print(encodeListKnown)
    print('Encoding Complete')

    #print(alarm_time,event_name_list,event_date_list,event_time_list)
    def job():
        alarming_system = alarm_control.control()
        print(alarming_system)

        alarm_time = alarming_system[0]
        event_name_list = alarming_system[1]
        event_date_list = alarming_system[2]
        event_time_list = alarming_system[3]

        cur_alarm_time=alarm_time[0]
        cur_event_name=event_name_list[0]
        cur_event_date=event_date_list[0]
        cur_event_time=event_time_list[0]

        cur_time=datetime.datetime.now()
        date_set = cur_time.strftime("%m/%d/%y")
        time_set = cur_time.strftime("%H:%M")
        print(date_set,cur_event_date)
        print(time_set,cur_alarm_time)

        if date_set == cur_event_date and time_set == cur_alarm_time:
            my_text = f"Your event {cur_event_name} is scheduled at {cur_event_time}"
            tts = gTTS(text=my_text, lang='en')
            filename = 'alarm.mp3'
            tts.save(filename)
            playsound('alarm.mp3')

        if date_set == cur_event_date and time_set == cur_event_time:
            tempList = []
            with open("event_data.csv", 'r') as rd:
                reader = csv.reader(rd)
                for row in reader:
                    if (row[0] != cur_event_name):
                        tempList.append(row)
                rd.close()
            with open("event_data.csv", 'w') as wr:
                writer = csv.writer(wr)
                writer.writerows(tempList)
                wr.close()


    schedule.every(30).seconds.do(job)

    cap = cv2.VideoCapture(0)
    while True:
        s=[]
        t=[]
        all=[]
        schedule.run_pending()
        success, img = cap.read()
        cv2.putText(img, 'Press ENTER to listen', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 2)
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = fc.face_locations(imgS)
        encodesCurFrame = fc.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = fc.compare_faces(encodeListKnown, encodeFace)
            faceDis = fc.face_distance(encodeListKnown, encodeFace)
            minDis = min(faceDis)
            if (minDis > 0.5):
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, "Unknown", (x1 + 6, y2 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 100, 255), 1)
            else:
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = classNames[matchIndex]
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    cv2.putText(img, name, (x1 + 6, y2 + 25), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 0), 2)
                    cv2.putText(img, "Departmet : " + str(dictData[name][0]), (x1 + 6, y2 + 70),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (100, 200, 255), 2)
                    if (dictData[name][1][0] <= '9' and dictData[name][1][0] >= '0'):
                        cv2.putText(img, "ID : " + str(dictData[name][1]), (x1 + 6, y2 + 115), cv2.FONT_HERSHEY_COMPLEX,
                                    0.8, (100, 200, 255), 2)
                        if (dictData[name][2], name) not in s:
                            s.append((dictData[name][2], name, dictData[name][0]))
                            s.sort(reverse=True)
                    else:
                        cv2.putText(img, "Designation : " + str(dictData[name][1]), (x1 + 6, y2 + 115),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.8, (100, 200, 255), 2)
                        if (dictData[name][2], name) not in t:
                            t.append((dictData[name][2], name, dictData[name][0]))
                            t.sort()
            print(s)
            print(t)
        cv2.imshow('Webcam', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 13:
            '''
            path = '/home/ashik/PycharmProjects/pythonProject'
            cv2.imwrite(os.path.join(path, 'detect.jpg'), img)
            #print('Capture Image')
            path1 = '/home/ashik/PycharmProjects/pythonProject/detect.jpg'
            num=How_many_image.count_image(path1)
            print(num)
            for i in range(num):
                if (dictData[name][1][0] <= '9' and dictData[name][1][0] >= '0'):
                    if (dictData[name][2], name) not in s:
                        s.append((dictData[name][2], name, dictData[name][0]))
                        s.sort(reverse=True)
                else:
                    if (dictData[name][2], name) not in t:
                        t.append((dictData[name][2], name, dictData[name][0]))
                        t.sort()
            '''
            all = t + s
            print(all[0])
            myText=f'{all[0][1]} from Department of {all[0][2]}'
            tts = gTTS(text=myText, lang='en')
            filename = 'hello.mp3'
            tts.save(filename)
            playsound('hello.mp3')


    cap.release()
    cv2.destroyAllWindows()