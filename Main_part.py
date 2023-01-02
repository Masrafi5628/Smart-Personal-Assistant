from tkinter import *
import cv2
import tkinter.messagebox as msg
import os
import tkinter.filedialog
from PIL import Image,ImageTk
import csv
import tkinter
import delete_event_info
import edit_evt_management
from delete_event_info import *
import alarm_control
from alarm_control import *
import Capture
import event_management
import Staff
import officer
from officer import *
import student
import event_management
import delete_file
from delete_file import *
import teacher
from teacher import *
from student import *
from Capture import *
from Staff import *
from event_management import *
from edit_evt_management import *

root = Tk()
image_o = Image.open('face.jpg')
size = (600, 400)  # 450,400
image_o = image_o.resize(size)
back_end = ImageTk.PhotoImage(image_o)
root.geometry("600x400")
root.resizable(width=False,height=False)
lbl = Label(root, image=back_end)
lbl.place(x=168, y=47)

def camera():
    Capture.capta()

def delete():
    delete_file.delt(root)

def evt():
    def add_event():
        event_management.event_info(newpage2)
    def delete_event():
        delete_event_info.event_infodelete(newpage2)
    def edit_event():
        edit_evt_management.event_info_edit(newpage2)

    newpage2 = Toplevel(root)
    newpage2.title('Event')
    newpage2.geometry("300x200")

    fr = Frame(newpage2, bg='grey')
    bu = Button(fr, text="Add Event", font="Arial 15 bold", fg='orange',command=add_event)
    bu.grid()
    fr.pack(side=TOP)

    fr2 = Frame(newpage2, bg='grey')
    bu = Button(fr2, text="Edit Event", font="Arial 15 bold", fg='green',command=edit_event)
    bu.grid()
    fr2.pack(side=TOP)

    fr1 = Frame(newpage2, bg='grey')
    bu = Button(fr1, text="Delete Event", font="Arial 15 bold", fg='orange',command=delete_event)
    bu.grid()
    fr1.pack(side=TOP)

    newpage2.mainloop()


def check():
    def popup2():
        student.student_information(newpage2)
    def teacher2():
        teacher.teach(newpage2)
    def officers():
        officer.office(newpage2)
    def stf():
        Staff.staff_info(newpage2)

    newpage2 = Toplevel(root)
    newpage2.title('Catagory')
    newpage2.geometry("300x200")

    fr = Frame(newpage2, bg='grey')
    bu = Button(fr, text="STUDENT", font="Arial 15 bold", fg='orange', command=popup2)
    bu.grid()
    fr.pack(side=TOP)

    fr1 = Frame(newpage2, bg='grey')
    bu = Button(fr1, text="TEACHER", font="Arial 15 bold", fg='green', command=teacher2)
    bu.grid()
    fr1.pack(side=TOP)

    fr2 = Frame(newpage2, bg='grey')
    bu = Button(fr2, text="OFFICER", font="Arial 15 bold", fg='orange', command=officers)
    bu.grid()
    fr2.pack(side=TOP)

    fr3 = Frame(newpage2, bg='grey')
    bu = Button(fr3, text="STAFF", font="Arial 15 bold", fg='green', command=stf)
    bu.grid()
    fr3.pack(side=TOP)

    newpage2.mainloop()

def quitpage():
    root.destroy()

root.title("Identity Recognition System")

f1 = Frame(root, bg="yellow", relief=SUNKEN, borderwidth=6)
f1.pack(side=LEFT, fill=Y)
f2 = Frame(root, bg='grey', relief=SUNKEN, borderwidth=6)
f2.pack(side=TOP, fill=X)
a = Label(f1, text='Face Recognize', fg='red', font=('Arial', 15, 'bold'))
a.pack(pady=150)
b = Label(f2, text='Identity Recognition System', font=('Arial', 20, 'bold'), fg='green')
b.pack()

frame1 = Frame(root, height=50, width=120, bg='green')
b1 = Button(frame1, text="Add New", font="Arial 12 bold", fg='green', command=check)
b1.pack()
frame1.pack(side=TOP, pady=5)

frame2 = Frame(root, height=50, width=120, bg='black')
b1 = Button(frame2, text="Delete", font="Arial 12 bold", fg='black', command=delete)        #
b1.pack()
frame2.pack(side=TOP, pady=5)

frame4 = Frame(root, height=50, width=120, bg='green')
b1 = Button(frame4, text="Camera", font="Arial 12 bold", fg='green', command=camera)        #
b1.pack()
frame4.pack(side=TOP, pady=5)

frame6 = Frame(root, height=50, width=120, bg='green')
b1 = Button(frame6, text="Event", font="Arial 12 bold", fg='black', command=evt)        #
b1.pack()
frame6.pack(side=TOP, pady=5)

frame5 = Frame(root, height=50, width=120, bg='black')
b1 = Button(frame5, text="Quit", font="Arial 12 bold", fg='green', command=quitpage)
b1.pack()
frame5.pack(side=TOP, pady=5)

root.mainloop()