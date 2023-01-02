import tkinter.filedialog
from tkinter import *
import cv2
import face_recognition
import numpy as np
import tkinter.messagebox as msg
import os
import csv

root=Tk()
root.geometry("1200x800")
#bg=PhotoImage(file="60.png")
root.configure(bg='#856ff8')
dataLocations=[]

def camera():
    dictData={}
    with open("Finale/Data.csv",'r') as file:
        reader=csv.reader(file)
        for row in reader:
            # if(dictData[row[0]]): // if name already exists
            dictData[row[0]]=(row[1],row[2])
        file.close()
    path = 'FR/Photos'
    images = []
    classNames = []
    myList = os.listdir(path) # file names in directory
    print(myList)

    for cl in myList:
        curImg = cv2.imread(f'{path}/{cl}') # reads image file cl from path
        images.append(curImg)
        name = os.path.splitext(cl)[0]
        classNames.append(name)

    print(classNames)

    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print(encodeListKnown)
    print('Encoding Complete')

    cap = cv2.VideoCapture(0) # get a video capture object
    print("cap")
    while True:
        success, img = cap.read()
        #img = captureScreen()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)
        for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(faceDis)
            minDis = min(faceDis)
            if(minDis > 0.5):
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                # cv2.rectangle(img, (x1, y2-35), (x2, y2), (255, 0, 0), cv2.FILLED)
                cv2.putText(img, "Unknown", (x1+6, y2+25),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (0, 100, 255), 1)
            else:
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = classNames[matchIndex]
                    # print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    cv2.putText(img, name, (x1+6, y2+25),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (100, 100, 0), 2)
                    cv2.putText(img,"Departmet : "+ str(dictData[name][0]), (x1+6, y2+70),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (100, 200, 255), 2)
                    if(dictData[name][1][0]<='9' and dictData[name][1][0]>='0'):
                        cv2.putText(img,"ID : "+ str(dictData[name][1]), (x1+6, y2+115),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (100, 200, 255), 2)
                    else:
                        cv2.putText(img,"Designation : "+ str(dictData[name][1]), (x1+6, y2+115),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (100, 200, 255), 2)

        cv2.imshow('Webcam', img)
        key=cv2.waitKey(1)
        if key==27:
            break
    cap.release()
    cv2.destroyAllWindows()

def popup():

    def new_window():

        def ok():
            msg.showinfo('', 'Your Picture is Selected')
            newpage.destroy()

        def upload_files():
            f_type = [('Jpg files', '*.jpg'), ('PNG files', '*.png')]
            filename = tkinter.filedialog.askopenfilenames(filetypes=f_type)
            print(filename[0])

            img = face_recognition.load_image_file(filename[0])
            encodeImg = face_recognition.face_encodings(img)
            print(encodeImg)


        def capture():
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Capturing Image', frame)
                key = cv2.waitKey(1)
                if key == 13:
                    inputName = name.get()
                    imgName = '{}.jpg'.format(inputName)
                    path = 'FR/Photos'
                    cv2.imwrite(os.path.join(path , imgName), frame)
                    # name,id,dept
                    with open("Data.csv","a") as dataFile:
                        csvWriter=csv.writer(dataFile)
                        csvWriter.writerow([inputName,Department.get(),ID.get()])
                        dataFile.close()
                    print("done csv")
                    cv2.waitKey(0)
                    break
            cap.release()
            cv2.destroyAllWindows()
            print(imgName)

        newpage = Toplevel(root)
        newpage.title('Select Image')
        newpage.geometry("600x500")

        fr = Frame(newpage, bg='grey')
        bu = Button(fr, text="Camera Frame", font="Arial 15 bold", fg='orange', command=capture)
        bu.grid()
        fr.pack(side=TOP)

        fr1 = Frame(newpage, bg='grey')
        bu = Button(fr1, text="Upload Image", font="Arial 15 bold", fg='green', command=lambda: upload_files())
        bu.grid()
        fr1.pack(side=TOP)

        fr2 = Frame(newpage, bg='grey')
        bu = Button(fr2, text="OK", font="Arial 15 bold", fg='blue', command=ok)
        bu.grid()
        fr2.pack(anchor='e')

        newpage.mainloop()

    def ok1():
        nam=name.get()
        roll=ID.get()
        dept=Department.get()
        if len(nam)>2 and len(roll)==6 and len(dept)>1:
            msg.showinfo('','Your Information is recorded')
            popupwindow.destroy()
        else:
            msg.showinfo('','Please, Give correct information')

    popupwindow=Toplevel(root)
    popupwindow.title('Add New')
    popupwindow.geometry("1200x400")

    Label(popupwindow,text='Please Add Your Information',bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0,column=1)

    Label(popupwindow, text='Name(Full Name)',font=('Arial',10,'bold')).grid()
    Label(popupwindow, text='Department',font=('Arial',10,'bold')).grid()
    Label(popupwindow, text='Student ID/Designation',font=('Arial',10,'bold')).grid()

    name = StringVar()
    Department = StringVar()
    ID = StringVar()

    Entry(popupwindow, text=name).grid(row=1,column=1)
    Entry(popupwindow, text=Department).grid(row=2,column=1)
    Entry(popupwindow, text=ID).grid(row=3, column=1)

    fr = Frame(popupwindow, bg='grey')
    bu = Button(fr, text="Image", font="Arial 15 bold", fg='green',command=lambda:new_window())
    bu.grid()
    fr.grid(row=5,column=1)

    fr1 = Frame(popupwindow, bg='grey')
    bu = Button(fr1, text="OK", font="Arial 15 bold", fg='black',command=ok1)
    bu.grid()
    fr1.grid(row=6, column=4)

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