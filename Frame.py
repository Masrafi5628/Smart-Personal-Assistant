import tkinter.filedialog
from tkinter import *
import cv2
import tkinter.messagebox as msg
import face_recognition as fc
import csv
import os
import numpy as np
import time
from PIL import Image,ImageTk
import pyttsx3

root=Tk()
#root.configure(bg='#856ff8')
#root.maxsize(800,500)

image_o=Image.open('face.jpg')
size=(600,400)      #450,400
image_o=image_o.resize(size)
back_end=ImageTk.PhotoImage(image_o)
root.geometry("600x400")
lbl=Label(root,image=back_end)
lbl.place(x=168,y=47)

speaker=pyttsx3.init()
speaker.setProperty('rate',150)
speaker.setProperty('voices',0.9)

def camera():
    dictData = {}
    with open("Data.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # if(dictData[row[0]]): // if name already exists
            dictData[row[0]] = (row[1], row[2])
        file.close()

    path = '/home/ashik/PycharmProjects/pythonProject/Images'
    images = []
    classNames = []
    myList = os.listdir(path)  # file names in directory
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
            encode = fc.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    encodeListKnown = findEncodings(images)
    print(encodeListKnown)
    print('Encoding Complete')

    cap=cv2.VideoCapture(0)
    while True:
        success, img = cap.read()
        cv2.putText(img,'Press ENTER to listen',(30,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
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
                cv2.putText(img, "Unknown", (x1 + 6, y2 + 25),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 100, 255), 1)
            else:
                matchIndex = np.argmin(faceDis)
                if matches[matchIndex]:
                    name = classNames[matchIndex]
                    y1,x2,y2,x1=faceLoc
                    y1,x2,y2,x1=y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),1)
                    cv2.putText(img,name,(x1+6,y2+25),cv2.FONT_HERSHEY_COMPLEX,1,(100,100,0),2)
                    cv2.putText(img,"Departmet : "+str(dictData[name][0]),(x1+6,y2+70),cv2.FONT_HERSHEY_COMPLEX,0.8,(100,200,255),2)
                    if (dictData[name][1][0] <= '9' and dictData[name][1][0] >= '0'):
                        cv2.putText(img,"ID : "+str(dictData[name][1]),(x1+6,y2+115),cv2.FONT_HERSHEY_COMPLEX,0.8,(100,200,255),2)
                        '''
                        key=cv2.waitKey(0)
                        if key==13:
                            myText = f'{name} from department of {dictData[name][0]} with id {dictData[name][1]}'
                            speaker.say(myText)
                            speaker.runAndWait()
                        '''
                    else:
                        cv2.putText(img,"Designation : "+str(dictData[name][1]),(x1+6,y2+115),cv2.FONT_HERSHEY_COMPLEX,0.8,(100,200,255),2)
                        '''
                        key = cv2.waitKey(1)
                        if key == 13:
                            myText=f'{name} {dictData[name][1]} department of {dictData[name][0]}'
                            speaker.say(myText)
                            speaker.runAndWait()
                        '''
        cv2.imshow('Webcam', img)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def delete():

    def deleteInfo():
        getName=name.get()
        getPassword=Password.get()
        getphone=phone.get()

        with open('Data.csv','r') as f:
            reader=csv.reader(f)
            for line in reader:
                if line[4]==getphone:
                    myPassword=line[3]
                    myName=line[0]
                    myPhone=line[4]
                    break
            f.close()
        print(myPassword)

        if myPassword==getPassword and getName==myName and getphone==myPhone:
            newMyName=myName+'.jpg'
            path=f'/home/ashik/PycharmProjects/pythonProject/Images/{newMyName}'
            print(newMyName)
            if os.path.exists(path):
                os.remove(path)
            print('done')

            tempList = []
            with open("Data.csv", 'r') as rd:
                reader = csv.reader(rd)
                for row in reader:
                    if (row[4] != myPhone):
                        tempList.append(row)
                rd.close()
            with open("Data.csv", 'w') as wr:
                writer = csv.writer(wr)
                writer.writerows(tempList)
                wr.close()
            msg.showinfo('','Deleted Your Information')
            newpage2.destroy()

        else:
            msg.showinfo('','Give Correct Information')

    newpage2 = Toplevel(root)
    newpage2.title('Delete')
    newpage2.geometry("550x150")

    Label(newpage2, text='Delete Your Information', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0,column=1)

    Label(newpage2,text='Name',font=('Arial',10,'bold')).grid()
    Label(newpage2, text='Phone Number or Email', font=('Arial', 10, 'bold')).grid()
    Label(newpage2, text='Password', font=('Arial', 10, 'bold')).grid()

    name = StringVar()
    phone = StringVar()
    Password=StringVar()

    Entry(newpage2, text=name).grid(row=1, column=1)
    Entry(newpage2, text=phone).grid(row=2, column=1)
    b = Entry(newpage2, show='*', textvariable=Password)
    b.grid(row=3, column=1)

    fr1 = Frame(newpage2, bg='grey')
    bu = Button(fr1, text="OK", font="Arial 15 bold", fg='black',command=deleteInfo)
    bu.grid()
    fr1.grid(row=4, column=2)

    newpage2.mainloop()

def check():

    def teacher():

        def new_window():

            def ok():
                msg.showinfo('', 'Your Picture is Selected')
                newpage.destroy()

            def upload_files():
                f_type = [('Jpg files', '*.jpg'), ('PNG files', '*.png')]
                filename = tkinter.filedialog.askopenfilenames(filetypes=f_type)
                print(filename[0])

                inputName = name.get()
                PATH = filename[0]
                copyPathFile = f'/home/ashik/PycharmProjects/pythonProject/Images/{inputName}'
                copyPath = copyPathFile
                img = Image.open(os.path.join(PATH))
                img.save(copyPath + '.jpg')
                print("save")

            def capture():
                cap = cv2.VideoCapture(0)
                while True:
                    ret, frame = cap.read()
                    cv2.imshow('Capturing Image', frame)
                    key = cv2.waitKey(1)
                    if key == 13:
                        inputName = name.get()
                        imgName = '{}.jpg'.format(inputName)
                        path = '/home/ashik/PycharmProjects/pythonProject/Images'
                        cv2.imwrite(os.path.join(path, imgName), frame)
                        time.sleep(5)
                    if key == 27:
                        break

                cap.release()
                cv2.destroyAllWindows()

            newpage = Toplevel(newpage2)
            newpage.title('Select Image')
            newpage.geometry("300x200")

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
            inputName = name.get()
            dept = Department.get()
            with open("Data.csv", "a") as dataFile:
                csvWriter = csv.writer(dataFile)
                csvWriter.writerow([inputName, Department.get(), ID.get(),Password.get(),phone.get()])
                dataFile.close()
            print("done csv")
            if len(inputName) > 2 and len(dept) > 1:
                msg.showinfo('', 'Your Information is recorded')
                popupwindow.destroy()
                newpage2.destroy()
            else:
                msg.showinfo('', 'Please, Give correct information')

        def show_password():
            if c_v1.get() == 1:
                b.config(show='')
            else:
                b.config(show='*')

        popupwindow = Toplevel(newpage2)
        popupwindow.title('Add New')
        popupwindow.geometry("500x280")

        Label(popupwindow, text='Add Your Information', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0, column=1)

        Label(popupwindow, text='Name(Full Name)', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Department', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Designation', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Phone Number or Email', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Password', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Confirm Password', font=('Arial', 10, 'bold')).grid()

        name = StringVar()
        Department = StringVar()
        ID = StringVar()
        phone = StringVar()
        Password = StringVar()
        Confirm_Password = StringVar()
        c_v1 = IntVar(value=0)

        Entry(popupwindow, text=name).grid(row=1, column=1)
        Entry(popupwindow, text=Department).grid(row=2, column=1)
        Entry(popupwindow, text=ID).grid(row=3, column=1)
        Entry(popupwindow, text=phone).grid(row=4, column=1)
        b = Entry(popupwindow, show='*', textvariable=Password)
        b.grid(row=5, column=1)
        Checkbutton(popupwindow, variable=c_v1, onvalue=1, offvalue=0, command=show_password).place(x=375, y=127)
        Entry(popupwindow, show='*', textvariable=Confirm_Password).grid(row=6, column=1)


        fr = Frame(popupwindow, bg='grey')
        bu = Button(fr, text="Image", font="Arial 15 bold", fg='green', command=lambda: new_window())
        bu.grid()
        fr.grid(row=7, column=1)

        fr1 = Frame(popupwindow, bg='grey')
        bu = Button(fr1, text="OK", font="Arial 15 bold", fg='black', command=ok1)
        bu.grid()
        fr1.grid(row=8, column=4)

        popupwindow.mainloop()

    def popup():

        def new_window():

            def ok():
                msg.showinfo('', 'Your Picture is Selected')
                newpage.destroy()

            def upload_files():
                f_type = [('Jpg files', '*.jpg'), ('PNG files', '*.png')]
                filename = tkinter.filedialog.askopenfilenames(filetypes=f_type)
                print(filename[0])

                inputName = name.get()
                PATH = filename[0]
                copyPathFile = f'/home/ashik/PycharmProjects/pythonProject/Images/{inputName}'
                copyPath = copyPathFile
                img = Image.open(os.path.join(PATH))
                img.save(copyPath + '.jpg')
                print("save")

            def capture():
                cap = cv2.VideoCapture(0)
                while True:
                    ret, frame = cap.read()
                    cv2.imshow('Capturing Image', frame)
                    key = cv2.waitKey(1)
                    if key == 13:
                        inputName = name.get()
                        imgName = '{}.jpg'.format(inputName)
                        path = '/home/ashik/PycharmProjects/pythonProject/Images'
                        cv2.imwrite(os.path.join(path, imgName), frame)
                        time.sleep(5)
                    if key == 27:
                        break

                cap.release()
                cv2.destroyAllWindows()

            newpage = Toplevel(newpage2)
            newpage.title('Select Image')
            newpage.geometry("300x200")

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
            inputName = name.get()
            dept = Department.get()
            with open("Data.csv", "a") as dataFile:
                csvWriter = csv.writer(dataFile)
                csvWriter.writerow([inputName, Department.get(), ID.get(),Password.get(),phone.get()])
                dataFile.close()
            print("done csv")
            if len(inputName) > 2 and len(dept) > 1:
                msg.showinfo('', 'Your Information is recorded')
                popupwindow.destroy()
                newpage2.destroy()
            else:
                msg.showinfo('', 'Please, Give correct information')

        def show_password():
            if c_v1.get() == 1:
                b.config(show='')
            else:
                b.config(show='*')

        popupwindow = Toplevel(newpage2)
        popupwindow.title('Add New')
        popupwindow.geometry("500x280")

        Label(popupwindow, text='Add Your Information', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0,column=1)

        Label(popupwindow, text='Name(Full Name)', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Department', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Student ID', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Phone Number or Email', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Password', font=('Arial', 10, 'bold')).grid()
        Label(popupwindow, text='Confirm Password', font=('Arial', 10, 'bold')).grid()

        name = StringVar()
        Department = StringVar()
        ID = StringVar()
        phone=StringVar()
        Password = StringVar()
        Confirm_Password = StringVar()
        c_v1 = IntVar(value=0)

        Entry(popupwindow, text=name).grid(row=1, column=1)
        Entry(popupwindow, text=Department).grid(row=2, column=1)
        Entry(popupwindow, text=ID).grid(row=3, column=1)
        Entry(popupwindow, text=phone).grid(row=4, column=1)
        b = Entry(popupwindow, show='*', textvariable=Password)
        b.grid(row=5, column=1)
        Checkbutton(popupwindow, variable=c_v1, onvalue=1, offvalue=0, command=show_password).place(x=375, y=127)
        Entry(popupwindow, show='*', textvariable=Confirm_Password).grid(row=6, column=1)

        fr = Frame(popupwindow, bg='grey')
        bu = Button(fr, text="Image", font="Arial 15 bold", fg='green', command=lambda: new_window())
        bu.grid()
        fr.grid(row=7, column=1)

        fr1 = Frame(popupwindow, bg='grey')
        bu = Button(fr1, text="OK", font="Arial 15 bold", fg='black', command=ok1)
        bu.grid()
        fr1.grid(row=8, column=4)

        popupwindow.mainloop()

    newpage2 = Toplevel(root)
    newpage2.title('Catagory')
    newpage2.geometry("300x200")

    fr = Frame(newpage2, bg='grey')
    bu = Button(fr, text="STUDENT", font="Arial 15 bold", fg='orange', command=popup)
    bu.grid()
    fr.pack(side=TOP)

    fr1 = Frame(newpage2, bg='grey')
    bu = Button(fr1, text="TEACHER", font="Arial 15 bold", fg='green', command=teacher)
    bu.grid()
    fr1.pack(side=TOP)

    newpage2.mainloop()


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
b1=Button(frame1,text="Add New",font="Arial 12 bold",fg='green',command=check)
b1.pack()
frame1.pack(side=TOP,pady=5)

frame2=Frame(root,height=50,width=120,bg='black')
b1=Button(frame2,text="Delete",font="Arial 12 bold",fg='black',command=delete)
b1.pack()
frame2.pack(side=TOP,pady=5)

frame4=Frame(root,height=50,width=120,bg='green')
b1=Button(frame4,text="Camera",font="Arial 12 bold",fg='green',command=camera)
b1.pack()
frame4.pack(side=TOP,pady=5)

frame5=Frame(root,height=50,width=120,bg='black')
b1=Button(frame5,text="Quit",font="Arial 12 bold",fg='black',command=quitpage)
b1.pack()
frame5.pack(side=TOP,pady=5)

root.mainloop()