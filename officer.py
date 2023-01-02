from tkinter import *
from tkinter import ttk
import cv2
import tkinter.messagebox as msg
import os
import tkinter.filedialog
from PIL import Image
import csv
import time

def office(newpage2):
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
            a=0
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if a == 0:
                    cv2.putText(frame,'Press ENTER to Capture Image or Press Esc to exit.',(30,30),cv2.FONT_HERSHEY_COMPLEX,0.5,(0, 255, 255),2)
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
        dept = office_name.get().upper()
        des=ID.get().upper()
        a = -1
        if des == 'VICE CHANCELLOR':
            a = 0
        elif des == 'PS TO VICE CHANCELLOR':
            a=1
        elif des == 'REGISTER':
            a=2
        elif des == 'PROCTOR':
            a=3
        elif des == 'DEPUTY REGISTER':
            a=4
        elif des == 'SECTION OFFICER':
            a=5
        elif des == 'TREASURER':
            a=6
        elif des == 'ASSISTANT REGISTER':
            a=7
        elif des == 'DIRECTOR':
            a=8
        elif des == 'ASSISTANT PROCTOR':
            a=9

        if len(inputName) != ' ' and len(dept) != ' ' and Password.get() == Confirm_Password.get() and '@.gmail.com' in phone.get():
            with open("Data.csv", "a") as dataFile:
                csvWriter = csv.writer(dataFile)
                csvWriter.writerow([inputName, office_name.get().upper(), des, Password.get(), phone.get(), a])
                dataFile.close()
            print("done csv")
            msg.showinfo('', 'Your Information is recorded')
            popupwindow.destroy()
            newpage2.destroy()
        else:
            msg.showinfo('', 'Please, Enter correct information')

    def show_password():
        if c_v1.get() == 1:
            b.config(show='')
        else:
            b.config(show='*')

    popupwindow = Toplevel(newpage2)
    popupwindow.title('Add New')
    popupwindow.geometry("500x280")

    depart=['Office of Registar','Office of Vice Chancellor','Office of the Treasure','Office of the proctor','Office of the Director of Accounts','Office of Librarian']
    options=['Vice Chancellor','PS to Vice Chancellor','Section Officer','Treasurer','Register','Deputy Register','Assistant Registar','Security Officer','Librarian','Deputy Librarian','Proctor','Assistant Proctor','Director']

    Label(popupwindow, text='Add Your Information', bg='yellow', fg='red', font=('Arial', 20, 'bold')).grid(row=0,
                                                                                                            column=1)

    Label(popupwindow, text='Name(Full Name)', font=('Arial', 10, 'bold'),).grid()
    Label(popupwindow, text='Office Name', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow, text='Designation', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow, text='Phone Number or Email', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow, text='Password', font=('Arial', 10, 'bold')).grid()
    Label(popupwindow, text='Confirm Password', font=('Arial', 10, 'bold')).grid()

    name = StringVar()
    office_name = StringVar()
    ID = StringVar()
    phone = StringVar()
    Password = StringVar()
    Confirm_Password = StringVar()
    c_v1 = IntVar(value=0)

    Entry(popupwindow, text=name,width=29).grid(row=1, column=1)
    b1=ttk.Combobox(popupwindow,value=depart,width=27,text=office_name).grid(row=2, column=1)
    b2=ttk.Combobox(popupwindow,value=options,width=27,text=ID).grid(row=3, column=1)
    Entry(popupwindow, text=phone,width=29).grid(row=4, column=1)
    b = Entry(popupwindow, show='*', textvariable=Password,width=29)
    b.grid(row=5, column=1)
    Checkbutton(popupwindow, variable=c_v1, onvalue=1, offvalue=0, command=show_password).place(x=420, y=127)
    Entry(popupwindow, show='*', textvariable=Confirm_Password,width=29).grid(row=6, column=1)

    fr = Frame(popupwindow, bg='grey')
    bu = Button(fr, text="Image", font="Arial 15 bold", fg='green', command=lambda: new_window())
    bu.grid()
    fr.grid(row=7, column=1)

    fr1 = Frame(popupwindow, bg='grey')
    bu = Button(fr1, text="OK", font="Arial 15 bold", fg='black', command=ok1)
    bu.grid()
    fr1.grid(row=8, column=4)

    popupwindow.mainloop()