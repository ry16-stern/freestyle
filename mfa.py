from tkinter import *
from tkinter import messagebox
import pyqrcode
import io

def login_fn():
    print("test")


class mfa(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.resizable(False,False)

    def Canvas(self):
        self.canvas = Canvas(self,bg = "white" , width="580", height="480")
        self.canvas.place(x=10, y=10)

        self.title = Label(self, text="MFA authentication demo", bg="white" , font="bold, 20")
        self.title.place(x=160,y=50)

        self.explainer = Label(self, text="This demo will ", bg="white" , font="14")
        self.explainer.place(x=50,y=100)
    def qr(self):
        self.QRCode = Label(self,image = qr_code_image,bg="white")
        self.QRCode.place(x=200,y=150)

    def login(self):

        login = StringVar()
        self.un_text=Label(self,text = "email", bg="white" , font="14")
        self.un_text.place(x=90, y=210)
        self.username = Entry(self, font="50", bd=3, justify = CENTER, textvariable=login, relief=GROOVE)
        self.username.place(x = 170, y = 200,  width=300,  height=60)

        password = StringVar()
        self.pw_text=Label(self,text = "password", bg="white" , font="14")
        self.pw_text.place(x=60, y=310)
        self.passw=Entry(self, font="50", bd=3, justify = CENTER, textvariable=password, relief=GROOVE)
        self.passw.place(x = 170, y = 300,  width=300,  height=60)

        self.login_btn = Button(self , text = "LOGIN" , bg="blue" , fg="white", command= login_fn, font="bold, 20")
        self.login_btn.place(width=200, height=60 , x=220 , y=400)
    def quit(self):
        self.destroy()


if __name__=="__main__":
    w = mfa()
    w.Canvas()
    global qr, qr_code_image
    qr = pyqrcode.create('http://uca.edu')
    qr_code_image = BitmapImage(data = qr.xbm(scale=8))
    #window.qr()
    w.login()
    w.mainloop()


