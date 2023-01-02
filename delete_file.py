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

def delt(root):

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
