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

def event_info(newpage2):
    def ok():
        event_name=name.get()
        event_date=date.get()
        evt_hr=hr.get()
        evt_tm=tm.get()
        evt_mn=mn1.get()
        event_time=evt_hr+':'+str(evt_mn)+' '+evt_tm
        #event_time=time.get()

        dt=event_date.split('/')

        mn=dt[0]
        if len(mn)==1:
            mn=str(0)+dt[0]

        dy=dt[1]
        if len(dy)==1:
            dy=str(0)+dt[1]

        event_date=mn+'/'+dy+'/'+dt[2]

        with open("event_data.csv", "a") as dataFile:
            csvWriter = csv.writer(dataFile)
            csvWriter.writerow([event_name,event_date, event_time])
            dataFile.close()
        msg.showinfo('', 'Event Added Successfully')
        newpage2.destroy()

    popupwindow2 = Toplevel(newpage2)
    popupwindow2.title('Add Evnet')
    popupwindow2.geometry("350x200")


    Label(popupwindow2,text='Add Event',bg='yellow',fg='red',font=('Arial',20,'bold')).grid(row=0,column=3,columnspan=6)


    Label(popupwindow2, text='Event Name', font=('Arial', 10, 'bold')).grid(row=1,column=1)
    Label(popupwindow2, text='Event Date', font=('Arial', 10, 'bold')).grid(row=2,column=1)
    Label(popupwindow2, text='Event Time', font=('Arial', 10, 'bold')).grid(row=3,column=1)

    name = StringVar()
    date = StringVar()
    hr = StringVar()
    mn1 = IntVar()
    tm = StringVar()

    Entry(popupwindow2, textvariable=name, width=20).grid(row=1, column=3,columnspan=3)
    DateEntry(popupwindow2,selectmode='day',width=18,textvariable=date).grid(row=2,column=3,columnspan=3)
    #Entry(popupwindow2, textvariable=time, width=20).grid(row=3, column=3,columnspan=3)
    Spinbox(popupwindow2,from_=1,to=12,width=3,textvariable=hr).grid(row=3,column=3)
    Spinbox(popupwindow2, from_=0, to=59,width=3,textvariable=mn1).grid(row=3,column=4)
    Spinbox(popupwindow2,values=('AM','PM'),width=3,textvariable=tm).grid(row=3, column=5)

    fr = Frame(popupwindow2, bg='grey',width=2)
    bu = Button(fr, text="OK", font="Arial 15 bold", fg='green',command=ok,width=2)
    bu.grid()
    fr.grid(row=4,column=6)

    popupwindow2.mainloop()
