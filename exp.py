from tkinter import *
from tkinter import messagebox
import os
import pyqrcode
import pyrebase  

firebaseConfig = {
    "apiKey": "AIzaSyAWgbsRL6RVGFNrAy5pOaCc_e8bM8fkrgo",
    "authDomain": "mfademo-fa400.firebaseapp.com",
    "projectId": "mfademo-fa400",
    "storageBucket": "mfademo-fa400.appspot.com",
    "messagingSenderId": "968589107332",
    "appId": "1:968589107332:web:42f38c670392f2859922d1",
    "measurementId": "G-XW8RL344BF",
    "databaseURL" : ""
  }


firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

window = Tk()
window.geometry("600x500")
window.resizable(False,False)
window.title("MFA app")
window.canvas = Canvas(window,bg = "white" , width="580", height="480").pack()

class Pages():
    def login_show():
            global email,password ,l1,l2,l3,l4,l5,l6
            email = StringVar()
            password = StringVar()
            l1=Label(window, text="MFA authentication demo", bg="white" , font="bold, 20")
            l1.place(x=160,y=50)
            l2=Label(window,text = "email", bg="white" , font="14")
            l2.place(x=90, y=210)
            l3=Entry(window, textvariable = email,font="50", bd=3, relief=GROOVE)
            l3.place(x = 170, y = 200,  width=300,  height=60)
            l4=Label(window,text = "password", bg="white" , font="14")
            l4.place(x=60, y=310)
            l5=Entry(window,textvariable = password, font="50", bd=3, relief=GROOVE)
            l5.place(x = 170, y = 300,  width=300,  height=60)
            l6=Button(window , text = "LOGIN" , bg="blue" , fg="white", command= generate, font="bold, 20")
            l6.place(width=200, height=60 , x=220 , y=400)
    def login_hide():
        l1.place_forget()
        l2.place_forget()
        l3.place_forget()
        l4.place_forget()
        l5.place_forget()
        l6.place_forget()
    def radio():
         global r1,r2
         r1=Radiobutton(window, text = "Register",  value = "value1", indicator = 0, background = "light blue", font="Bold, 16")
         r1.place(width=100,height=40,x=196,y=130)
         r2=Radiobutton(window, text = "Login",  value = "value2", indicator = 0, background = "light blue", font="Bold, 16")
         r2.place(width=100,height=40,x=304,y=130)

def generate():
    emailval=email.get()
    passval=password.get()
    auth.create_user_with_email_and_password(emailval, passval)
    #if len(email.get())!=0 :
    #    global qr,photo
    #    qr = pyqrcode.create(email.get())
    #    photo = BitmapImage(data = qr.xbm(scale=8))
    #else:
    #    messagebox.showinfo("Please Enter some Subject")
    #try:
    #    
    #    imageLabel.config(image = photo)
    #    subLabel.config(text="QR of " + email.get())
    #except:
    #    pass


Pages.login_show()
Pages.radio()
imageLabel = Label(window)
imageLabel.place(x=0, y=0)

subLabel = Label(window,text="")
subLabel.place(x=0, y=0)

window.mainloop()