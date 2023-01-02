from tkinter import *
from tkinter import ttk
import cv2
import tkinter.messagebox as msg
import os
import tkinter.filedialog
from PIL import Image
import csv
import time

def student_information(newpage2):
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
                cv2.putText(frame, 'Press ENTER to Capture Image', (30, 30), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 255), 2)
                cv2.imshow('Capturing Image', frame)
                key = cv2.waitKey(1)
                if key == 13:
                    inputName = name.get()
                    imgName = '{}.jpg'.format(inputName)
                    path = '/home/ashik/PycharmProjects/pythonProject/Images'
                    cv2.imwrite(os.path.join(path, imgName), frame)
                    time.sleep(3)
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
        dept = Department.get().upper()

        if len(inputName) > 2 and len(dept) > 1 and '@.gmail.com' in phone.get():
            with open("Data.csv", "a") as dataFile:
                csvWriter = csv.writer(dataFile)
                csvWriter.writerow(
                    [inputName, Department.get().upper(), ID.get(), Password.get(), phone.get(), year.get()])
                dataFile.close()
            print("done csv")
            msg.showinfo('', 'Your Information is recorded')
            popupwindow2.destroy()
            newpage2.destroy()
        else:
            msg.showinfo('', 'Please, Give correct information')

    def show_password():
        if c_v1.get() == 1:
            b.config(show='')
        else:
            b.config(show='*')

    popupwindow2 = Toplevel(newpage2)
    popupwindow2.title('Add New')
    popupwindow2.geometry("500x280")

    depart = ['CSE', 'EEE', 'IPE', 'ChE']
    yr=[1,2,3,4]

    Label(popupwindow2, text='Add Your Information', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0,
                                                                                                            column=1)

    Label(popupwindow2, text='Name(Full Name)', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow2, text='Department', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow2, text='Student ID', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow2, text='year', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow2, text='Phone Number or Email', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow2, text='Password', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow2, text='', font=('Arial', 10, 'bold')).grid()

    name = StringVar()
    Department = StringVar()
    ID = StringVar()
    year = StringVar()
    phone = StringVar()
    Password = StringVar()
    c_v1 = IntVar(value=0)

    Entry(popupwindow2, text=name,width=29).grid(row=1, column=1)
    b1=ttk.Combobox(popupwindow2,value=depart,width=27,text=Department).grid(row=2, column=1)
    Entry(popupwindow2, text=ID,width=29).grid(row=3, column=1)
    #Entry(popupwindow2, text=year).grid(row=4, column=1)
    b2 = ttk.Combobox(popupwindow2, value=yr, width=27, text=year).grid(row=4, column=1)
    Entry(popupwindow2, text=phone,width=29).grid(row=5, column=1)
    b = Entry(popupwindow2, show='*', textvariable=Password,width=29)
    b.grid(row=6, column=1)
    Checkbutton(popupwindow2, variable=c_v1, onvalue=1, offvalue=0, command=show_password).place(x=420, y=150)

    fr = Frame(popupwindow2, bg='grey')
    bu = Button(fr, text="Image", font="Arial 15 bold", fg='green', command=lambda: new_window())
    bu.grid()
    fr.grid(row=7, column=1)

    fr1 = Frame(popupwindow2, bg='grey')
    bu = Button(fr1, text="OK", font="Arial 15 bold", fg='black', command=ok1)
    bu.grid()
    fr1.grid(row=8, column=4)

    popupwindow2.mainloop()