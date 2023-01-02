from tkinter import *
import tkinter.messagebox as msg
root=Tk()
root.geometry("500x200")

def travel():
    print('Your order is submitted')
    msg.showinfo('', 'Your order is submitted')
    print(f"Name = {name.get()},\nPhone number = {phone.get()},\nAddress = {address.get()},\nEmergency = {contact.get()},\nFood Order = {food.get()}")
    with open('Record file.txt','a') as f:
        f.write(f"\nName = {name.get()} \nPhone number = {phone.get()}\nAddress = {address.get()}\nEmergency = {contact.get()}\nFood Order = {food.get()}\n")

Label(root,text='Travel Agency',font=("Arial",20,"bold")).grid(row=0,column=4)

Label(root,text='Name').grid(row=2,column=3)
Label(root,text='Phone').grid(row=3,column=3)
Label(root,text='Address').grid(row=4,column=3)
Label(root,text='Contact Number').grid(row=5,column=3)

name=StringVar()
phone=StringVar()
address=StringVar()
contact=StringVar()
food=IntVar()

Entry(root,text=name).grid(row=2,column=4)
Entry(root,text=phone).grid(row=3,column=4)
Entry(root,text=address).grid(row=4,column=4)
Entry(root,text=contact).grid(row=5,column=4)
Checkbutton(root,text='Do you want prefood order',variable=food).grid(row=6,column=4)

Button(text='Submit',command=travel).grid(row=8,column=7)
root.mainloop()