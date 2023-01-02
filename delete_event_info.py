from tkinter import *
from tkinter import ttk
import cv2
import tkinter.messagebox as msg
from tkcalendar import DateEntry
import os
import tkinter.filedialog
from PIL import Image
import csv
import time
import datetime
from gtts import gTTS
from playsound import playsound

def event_infodelete(newpage2):
    def ok():
        event_name=name.get()
        event_date=date.get()
        event_time=time.get()

        tempList = []
        with open("event_data.csv", 'r') as rd:
            reader = csv.reader(rd)
            for row in reader:
                if (row[0] != event_name and row[1] != event_date and row[2] != event_time):
                    tempList.append(row)
            rd.close()
        with open("event_data.csv", 'w') as wr:
            writer = csv.writer(wr)
            writer.writerows(tempList)
            wr.close()


        msg.showinfo('', 'Successfully Deleted Of Your Event')
        newpage2.destroy()

    file_event_name = []
    file_event_date=[]
    file_event_time=[]

    with open("event_data.csv", 'r') as rd:
        reader = csv.reader(rd)
        for row in reader:
            file_event_name.append(row[0])
            file_event_date.append(row[1])
            file_event_time.append(row[2])
        rd.close()

    popupwindow2 = Toplevel(newpage2)
    popupwindow2.title('Add Evnet')
    popupwindow2.geometry("350x200")


    Label(popupwindow2, text='Add Event', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0,column=2,columnspan=4)


    Label(popupwindow2, text='Event Name', font=('Arial', 10, 'bold')).grid(row=1,column=1)
    Label(popupwindow2, text='Event Date', font=('Arial', 10, 'bold')).grid(row=2,column=1)
    Label(popupwindow2, text='Event Time', font=('Arial', 10, 'bold')).grid(row=3,column=1)

    name = StringVar()
    date = StringVar()
    time = StringVar()

    b1 = ttk.Combobox(popupwindow2, values=file_event_name, width=23, textvariable=name).grid(row=1, column=2,columnspan=3)
    b2 = ttk.Combobox(popupwindow2, values=file_event_date, width=23, textvariable=date).grid(row=2, column=2,columnspan=3)
    b1 = ttk.Combobox(popupwindow2, values=file_event_time, width=23, textvariable=name).grid(row=3, column=2,columnspan=3)
    #Entry(popupwindow2, text=name, width=20).grid(row=1, column=2,columnspan=3)
    #DateEntry(popupwindow2,selectmode='day',width=18,textvariable=date).grid(row=2,column=2,columnspan=3)
    #Entry(popupwindow2, text=time, width=20).grid(row=3, column=2,columnspan=3)

    fr = Frame(popupwindow2, bg='grey')
    bu = Button(fr, text="OK", font="Arial 15 bold", fg='green',command=ok)
    bu.grid()
    fr.grid(row=4,column=6)

    popupwindow2.mainloop()
