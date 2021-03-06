from tkinter import *
from tkinter import messagebox
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import pyqrcode
import pyrebase  
import pyotp
load_dotenv()

#load necessary config data from .env
apiKey = os.getenv("apiKey")
authDomain = os.getenv("authDomain")
projectId = os.getenv("projectId")
storageBucket = os.getenv("storageBucket")
messagingSenderId = os.getenv("messagingSenderId")
appId = os.getenv("appId")
measurementId = os.getenv("measurementId")
databaseURL = os.getenv("databaseURL")
#assign config data
firebaseConfig = {
    "apiKey": apiKey,
    "authDomain": authDomain,
    "projectId": projectId,
    "storageBucket":storageBucket,
    "messagingSenderId": messagingSenderId,
    "appId": appId,
    "measurementId": measurementId,
    "databaseURL" : databaseURL
  }


firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
#declare Tkinter object
window = Tk()
window.geometry("600x500")
window.resizable(False,False)
window.title("MFA app")
window.canvas = Canvas(window,bg = "white" , width="580", height="480").pack()

#Custom Tkinter control class
class Pages():
    def radio():
         global r0,r1,r2,contrvar
         r0=Label(window, text="MFA authentication demo", bg="white" , font="bold, 15")
         r0.place(x=160,y=50)
         contrvar=StringVar()
         r1=Radiobutton(window, text = "Register",  variable = contrvar, value = "1", command=lambda : Pages.reg_show("Register new user page","REGISTER"),indicator = 0, background = "light blue", font="Bold, 14")
         r1.place(width=100,height=40,x=196,y=130)
         r2=Radiobutton(window, text = "Login",     variable = contrvar, value = "2", command=lambda :  Pages.reg_show("Login page","LOGIN"),indicator = 0, background = "light blue", font="Bold, 14")
         r2.place(width=100,height=40,x=304,y=130)
    def reg_show(l1_txt,l6_txt):
            global email,password ,l1,l2,l3,l4,l5,l6
            l1_text=StringVar()
            l6_text=StringVar()
            l1_text=l1_txt
            l6_text=l6_txt
            email = StringVar()
            password = StringVar()
            r0.config(text=l1_text)
            l2=Label(window,text = "email", bg="white" , font="14")
            l2.place(x=90, y=210)
            l3=Entry(window, textvariable = email,font="50", bd=3, relief=GROOVE, justify="center")
            l3.place(x = 170, y = 200,  width=300,  height=60)
            l4=Label(window,text = "password", bg="white" , font="14")
            l4.place(x=60, y=310)
            l5=Entry(window,textvariable = password, font="50", bd=3, relief=GROOVE, justify="center")
            l5.place(x = 170, y = 300,  width=300,  height=60)
            l6=Button(window , text = l6_text , bg="blue" , fg="white", command= generate, font="bold, 16")
            l6.place(width=200, height=60 , x=220 , y=400)
    def barcode_show():
        global b0,b1
    def reg_hide():
        r0.place_forget()
        l2.place_forget()
        l3.place_forget()
        l4.place_forget()
        l5.place_forget()
        l6.place_forget()
        r1.place_forget()
        r2.place_forget()
    def reset_form():
        contrvar.set(None)
        Pages.reg_hide()
        Pages.radio()
    def qr_confirmed():
        imageLabel.place_forget()
        subLabel.place_forget()
        c1.place_forget()
        Pages.radio()
    def qr_view():
        global c1
        Pages.reg_hide()
        r0.place_forget()
        r1.place_forget()
        r2.place_forget()
        c1=Button(window , text = "CONFIRM" , bg="light blue" , fg="white", command= lambda :Pages.qr_confirmed(), font="bold, 16")
        c1.place(width=200, height=60 , x=175 , y=380)
    def show_mfa():
        global l7
        l4.place_forget()
        l5.place_forget()
        r1.place_forget()
        r2.place_forget()
        l7=Label(window,text = "Enter verification code", bg="white" , font="14")
        l7.place(x=200, y=150)
        l2.config(text="Code")
        l3.delete(0, 'end')
        l6.config(text="CANCEL")
    def show_success():
        #show success message
        r0.config(text="Successfully authenticated")
        l2.place_forget()
        l3.place_forget()
        l4.place_forget()
        l5.place_forget()
        l6.place_forget()
        r1.place_forget()
        r2.place_forget()
        l7.place_forget()

    def countdown(key,z):
        #MFA code verification
        if z>30:
            curr_time = datetime.now()
            sec = int(curr_time.strftime('%S'))
            #depending on the current second calculate how many seconds left before the next 30 sec cycle
            if sec>30:
                t=60-sec
            elif sec==30:
                t=30
            elif sec<30:
                t=30-sec
        else:
            t=z
        totp = pyotp.TOTP(key)
        text=StringVar()
        text_first="You have "
        text_last=" seconds to enter the code"
        text=text_first+str(t)+text_last
        #display the countdown timer
        r0.config(text=text)
        correct_value=str(totp.now())
        entered_value=email.get()
        #compare codes every second
        if correct_value==entered_value:
            #Authenticate user
            messagebox.showinfo("SUCCESS","MFA Authentication was succesful!")
            Pages.show_success()
        else:
            #if the times has expired reset it to 30 sec
            t -= 1
            if t<1:
                t=30
            window.after(1000,lambda: Pages.countdown(key,t))


def qrcodegen(link):
    #generate qr code
    if len(email.get())!=0 :
        global qr,photo
        qr = pyqrcode.create(link)
        photo = BitmapImage(data = qr.xbm(scale=5))
    else:
        messagebox.showinfo("Please Enter some Subject")
    try:

        showcode()
    except:
        pass

def showcode():
    #display qr code
    imageLabel.config(image = photo)
    subLabel.config(text="Scan this code with Google Authenticator")

def generate():
    emailval=email.get()
    passval=password.get()
    db = firebase.database()
    if contrvar.get()=="1":
        #Registration form is active      
        try:
            token = auth.create_user_with_email_and_password(emailval, passval)
            #Create base32 secret and store in data var
            secret=pyotp.random_base32()
            data = {  "key": secret }
            # Pass the user's idToken to the set method of pyrebase
            try:
                results = db.child(token["localId"]).set(data)
                if results:
                    messagebox.showinfo("Success!!","Account created succesfully")
                    #create OTP link for google authentication
                    link=pyotp.totp.TOTP(secret).provisioning_uri(name=emailval, issuer_name='MFA Demo')
                    qrcodegen(link)
                    Pages.qr_view()

            except:
                messagebox.showinfo("Error","Unknown error creating account")
                Pages.reset_form()

        except Exception as e:
            #error handler
            error_json = e.args[1]
            print(error_json)
            error=json.loads(error_json)['error']['message']
            
            if error=="EMAIL_EXISTS":
                 messagebox.showerror("Error","Email already registered")
                 
            elif error=="WEAK_PASSWORD : Password should be at least 6 characters":
                messagebox.showwarning("Error","WEAK_PASSWORD : Password should be at least 6 characters")
                
            if error=="INVALID_EMAIL":
                 messagebox.showwarning("Error","You entered an invalid email, please etner a valid email")
            Pages.reset_form()

    elif contrvar.get()=="2":
        #Login form is active
        try:
            token = auth.sign_in_with_email_and_password(emailval, passval)
            result = db.child(token["localId"]).get().val()
            key=result["key"]
            #check potp value
            Pages.show_mfa()
            Pages.countdown(key,40)
        except Exception as e:
            #error handler
            error_json = e.args[1]
            print(error_json)
            error=json.loads(error_json)['error']['message']
            if error=="INVALID_PASSWORD" or error=="EMAIL_NOT_FOUND":
                 messagebox.showerror("Error","Username or password are incorrect")
                 
#initiates Pages class
Pages.radio()
#Declaring the placeholder for QR code
imageLabel = Label(window,bg="white")
imageLabel.place(x=130, y=60)
subLabel = Label(window,text="",font="Bold, 14",bg="white")
subLabel.place(x=110, y=40)

window.mainloop()