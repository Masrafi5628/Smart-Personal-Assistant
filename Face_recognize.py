import face_recognition as fc
import cv2 as cv
import numpy as np
import os
from gtts import gTTS
import playsound
import speech_recognition

path='Images'
image=[]
dict={}
id=1
Name=[]
mylist=os.listdir(path)
print(mylist)
for cls in mylist:
    curImg=cv.imread(f'{path}/{cls}')
    image.append(curImg)
    name=os.path.splitext(cls)[0]
    Name.append(name)
    dict[name]=id
    id+=1

print(Name)

def findEncoding(image):
    encodlist=[]
    for img in image:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = fc.face_encodings(img)[0]
        encodlist.append(encode)
    return encodlist

encodlistknown=findEncoding(image)
print('Encoding Complete....')


with open('Record file.txt','w') as f:
    for x in range(0,5):
        f.write(f"Name = {Name[x]} , ID = {dict[Name[x]]} , Image encoding = {encodlistknown[x]}\n\n")
print("done txt")

cap=cv.VideoCapture(0)
while True:
    ret,img=cap.read()
    imgS=cv.resize(img,(0,0),None,0.25,0.25)
    imgS=cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

    faceLokCurrentFrame=fc.face_locations(imgS)
    encodingCurrentFrame=fc.face_encodings(imgS,faceLokCurrentFrame)

    for encodeFace,faceLok in zip(encodingCurrentFrame,faceLokCurrentFrame):
        match=fc.compare_faces(encodlistknown,encodeFace)
        faceDis=fc.face_distance(encodlistknown,encodeFace)
        minDis=min(faceDis)
        if faceDis[0]>0.55:
            y1,x2,y2,x1=faceLok
            y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
            cv.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv.putText(img,"Unknown",(x1+6,y2+25),cv.FONT_HERSHEY_COMPLEX,1,(0,100,255),1)
            myText = 'Unknown'
            language = 'en'
            tts = gTTS(text=myText, lang=language)
            filename = 'voice.mp3'
            tts.save(filename)
            playsound.playsound(filename)
        else:
            matchIndex=np.argmin(faceDis)
            if match[matchIndex]:
                name= Name[matchIndex]
                print(name)
                y1,x2,y2,x1=faceLok
                y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
                cv.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv.putText(img,name,(x1+6,y1-6),cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
                cv.putText(img,"ID="+str(dict[name]),(x1+6,y2+70),cv.FONT_HERSHEY_COMPLEX,1,(100,200,255),2)
                myText=dict[name]
                language='en'
                tts=gTTS(text=myText,lang=language)
                filename='voice.mp3'
                tts.save(filename)
                playsound.playsound(filename)

    cv.imshow('Window',img)
    key=cv.waitKey(1)
    if key==27:
        break
