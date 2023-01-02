from tkinter import *
import cv2 as cv
import tkinter.messagebox as msg
import numpy as np
import os
import face_recognition as fc
import pickle5 as pickle
from PIL import ImageTk,Image

root=Tk()
image_o=Image.open('face.jpg')
size=(600,400)      #450,400
image_o=image_o.resize(size)
back_end=ImageTk.PhotoImage(image_o)
root.geometry("600x400")
lbl=Label(root,image=back_end)
lbl.place(x=168,y=47)

def ok():
    msg.showinfo('', 'Your Information is Recorded')

def camera():
    path = 'Images'
    image = []
    dict = {}
    id = 1
    Name = []
    mylist = os.listdir(path)
    print(mylist)
    for cls in mylist:
        curImg = cv.imread(f'{path}/{cls}')
        image.append(curImg)
        name = os.path.splitext(cls)[0]
        Name.append(name)
        dict[name] = id
        id += 1

    def findEncoding(image):
        encodlist = []
        for img in image:
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            encode = fc.face_encodings(img)[0]
            encodlist.append(encode)
        return encodlist

    encodlistknown = findEncoding(image)

    with open('Record file.txt', 'w') as f:
        for x in range(0, 3):
            f.write(f"Name = {Name[x]} , ID = {dict[Name[x]]} , Image encoding = {encodlistknown[x]}\n\n")
    print("done txt")

    cap = cv.VideoCapture(0)
    while True:
        ret, img = cap.read()
        imgS = cv.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv.cvtColor(imgS, cv.COLOR_BGR2RGB)

        faceLokCurrentFrame = fc.face_locations(imgS)
        encodingCurrentFrame = fc.face_encodings(imgS, faceLokCurrentFrame)

        for encodeFace, faceLok in zip(encodingCurrentFrame, faceLokCurrentFrame):
            match = fc.compare_faces(encodlistknown, encodeFace)
            faceDis = fc.face_distance(encodlistknown, encodeFace)

            minDis = min(faceDis)
            if faceDis[0] > 0.55:
                y1, x2, y2, x1 = faceLok
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv.putText(img, "Unknown", (x1 + 6, y2 + 25), cv.FONT_HERSHEY_COMPLEX, 1, (0, 100, 255), 1)
            else:
                matchIndex = np.argmin(faceDis)
                if match[matchIndex]:
                    name = Name[matchIndex]
                    print(name)
                    y1, x2, y2, x1 = faceLok
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv.putText(img, name, (x1 + 6, y1 - 6), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    cv.putText(img, "ID=" + str(dict[name]), (x1 + 6, y2 + 70), cv.FONT_HERSHEY_COMPLEX, 1,
                               (100, 200, 255), 2)

        cv.imshow('Window', img)
        key = cv.waitKey(1)
        if key == 27:
            break


def popup():

    def capture():
        cap = cv.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            cv.imshow('Capturing Image', frame)
            key = cv.waitKey(1)
            if key == 13:
                n=name.get()
                imgName='{}.jpg'.format(n)
                cv.imwrite(imgName,frame)
                break
        cap.release()
        cv.destroyAllWindows()
        print(imgName)

        img=fc.load_image_file(imgName)
        encodeimg=fc.face_encodings(img)
        print(encodeimg)

        with open('BinaryFile.dat',mode='wb') as f:
            pickle.dump(encodeimg,f)

    popupwindow=Toplevel(root)
    popupwindow.title('Add New or Edit')
    popupwindow.geometry("400x200")


    Label(popupwindow,text='Add New / Edit',bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0,column=3)

    Label(popupwindow, text='Name',font=('Arial',10,'bold')).grid()
    Label(popupwindow, text='Department',font=('Arial',10,'bold')).grid()
    Label(popupwindow, text='ID',font=('Arial',10,'bold')).grid()

    name = StringVar()
    Department = StringVar()
    ID = StringVar()

    Entry(popupwindow,text=name).grid(row=1,column=3)
    Entry(popupwindow,text=Department).grid(row=2,column=3)
    Entry(popupwindow,text=ID).grid(row=3, column=3)

    fr = Frame(popupwindow, bg='grey')
    bu = Button(fr, text="Image", font="Arial 15 bold", fg='green',command=capture)
    bu.grid()
    fr.grid(row=5,column=3)

    fr1 = Frame(popupwindow, bg='grey')
    bu = Button(fr1, text="OK", font="Arial 15 bold", fg='black',command=ok)
    bu.grid()
    fr1.grid(row=6, column=5)

    popupwindow.mainloop()

def quitpage():
    root.destroy()

root.title("Identity Recognition System")

f1=Frame(root,bg="yellow",relief=SUNKEN,borderwidth=6)
f1.pack(side=LEFT,fill=Y)
f2=Frame(root,bg='grey',relief=SUNKEN,borderwidth=6)
f2.pack(side=TOP,fill=X)
a=Label(f1,text='Face Recognize',fg='red',font=('Arial',15,'bold'))
a.pack(pady=150)
b=Label(f2,text='Identity Recognition System',font=('Arial',20,'bold'),fg='green')
b.pack()


frame1=Frame(root,height=50,width=120,bg='green')
b1=Button(frame1,text="Add New",font="Arial 12 bold",fg='green',command=popup)
b1.pack()
frame1.pack(side=TOP,pady=5)

frame2=Frame(root,height=50,width=120,bg='black')
b1=Button(frame2,text="Delete",font="Arial 12 bold",fg='black')
b1.pack()
frame2.pack(side=TOP,pady=5)

frame3=Frame(root,height=50,width=120,bg='green')
b1=Button(frame3,text="Edit",font="Arial 12 bold",fg='green')
b1.pack()
frame3.pack(side=TOP,pady=5)

frame4=Frame(root,height=50,width=120,bg='black')
b1=Button(frame4,text="Camera",font="Arial 12 bold",fg='black',command=camera)
b1.pack()
frame4.pack(side=TOP,pady=5)

frame5=Frame(root,height=50,width=120,bg='green')
b1=Button(frame5,text="Quit",font="Arial 12 bold",fg='green',command=quitpage)
b1.pack()
frame5.pack(side=TOP,pady=5)

root.mainloop()