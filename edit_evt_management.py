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

def event_info_edit(newpage2):
    def ok():

        def ok1():
            event_name = name.get()
            event_date = date.get()
            event_time = time.get()
            with open("event_data.csv", "a") as dataFile:
                csvWriter = csv.writer(dataFile)
                csvWriter.writerow([event_name, event_date, event_time])
                dataFile.close()
            msg.showinfo('', 'Event Edit Successfully')

            newpage2.destroy()


        event_details=details.get()
        edit_details=event_details.split(',')
        print(edit_details)
        tempList = []
        with open("event_data.csv", 'r') as rd:
            reader = csv.reader(rd)
            for row in reader:
                if row[0] != edit_details[0] and row[1] != edit_details[1] and row[2] != edit_details[2]:
                    print('Match')
                    print(row[0],row[1],row[2])
                    tempList.append(row)
                    print(tempList)
            rd.close()
        with open("event_data.csv", 'w') as wr:
            writer = csv.writer(wr)
            writer.writerows(tempList)
            wr.close()

        Label(popupwindow2, text='Enter Event', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=3, column=3,columnspan=6)

        Label(popupwindow2, text='Event Name', font=('Arial', 10, 'bold')).grid(row=4, column=1)
        Label(popupwindow2, text='Event Date', font=('Arial', 10, 'bold')).grid(row=5, column=1)
        Label(popupwindow2, text='Event Time', font=('Arial', 10, 'bold')).grid(row=6, column=1)

        name = StringVar()
        date = StringVar()
        time = StringVar()

        #file_event_name = (edit_details[0])
        file_event_date = []
        file_event_time = []
        file_event_name = []

        file_event_name.append(edit_details[0])
        file_event_time.append(edit_details[2])
        file_event_date.append(edit_details[1])

        print(file_event_name,file_event_date,file_event_time)

        b1 = ttk.Combobox(popupwindow2, value=file_event_name, width=23, textvariable=name)
        b1.grid(row=4, column=3,columnspan=3)
        b1.current(0)
        b2 = ttk.Combobox(popupwindow2, value=file_event_date, width=23, textvariable=date)
        b2.grid(row=5, column=3,columnspan=3)
        b2.current(0)
        b3 = ttk.Combobox(popupwindow2, value=file_event_time, width=23, textvariable=time)
        b3.grid(row=6, column=3,columnspan=3)
        b3.current(0)



        fr = Frame(popupwindow2, bg='grey', width=2)
        bu = Button(fr, text="OK", font="Arial 15 bold", fg='green', command=ok1, width=2)
        bu.grid()
        fr.grid(row=7, column=6)

    popupwindow2 = Toplevel(newpage2)
    popupwindow2.title('Edit Evnet')
    popupwindow2.geometry("400x230")

    evt=[]
    with open("event_data.csv", 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            choi=row[0]+','+row[1]+','+row[2]
            evt.append(choi)
        file.close()

    details=StringVar()

    Label(popupwindow2,text='Choose Event to Edit',bg='yellow',fg='red',font=('Arial',20,'bold')).grid(row=0,column=3, columnspan=6)
    Label(popupwindow2, text='Event Details', font=('Arial', 10, 'bold')).grid(row=1, column=1)
    b1 = ttk.Combobox(popupwindow2, values=evt, width=25, textvariable=details).grid(row=1, column=3,columnspan=3)
    fr1 = Frame(popupwindow2, bg='grey', width=2)
    bu = Button(fr1, text="OK", font="Arial 15 bold", fg='green', command=ok, width=2)
    bu.grid()
    fr1.grid(row=2, column=6)

    '''
    Label(popupwindow2, text='Enter Event', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=3,column=3,columnspan=6)

    Label(popupwindow2, text='Event Name', font=('Arial', 10, 'bold')).grid(row=4,column=1)
    Label(popupwindow2, text='Event Date', font=('Arial', 10, 'bold')).grid(row=5,column=1)
    Label(popupwindow2, text='Event Time', font=('Arial', 10, 'bold')).grid(row=6,column=1)

    name = StringVar()
    date = StringVar()
    time=StringVar()
    evevt_edit=ok()

    file_event_name=evevt_edit[0]
    file_event_date=evevt_edit[1]
    file_event_time=evevt_edit[2]

    b1 = ttk.Combobox(popupwindow2, values=file_event_name, width=23, textvariable=name).grid(row=4, column=3,columnspan=3)
    b2 = ttk.Combobox(popupwindow2, values=file_event_date, width=23, textvariable=date).grid(row=5, column=3,columnspan=3)
    b1 = ttk.Combobox(popupwindow2, values=file_event_time, width=23, textvariable=time).grid(row=6, column=3,columnspan=3)


    fr = Frame(popupwindow2, bg='grey',width=2)
    bu = Button(fr, text="OK", font="Arial 15 bold", fg='green',command=ok1,width=2)
    bu.grid()
    fr.grid(row=7,column=6)
    '''
    popupwindow2.mainloop()
