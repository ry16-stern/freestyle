from tkinter import *
from tkinter import messagebox
import json
from datetime import datetime
import time
import pyqrcode
import pyrebase  
import pyotp

firebaseConfig = {
    "apiKey": "AIzaSyAWgbsRL6RVGFNrAy5pOaCc_e8bM8fkrgo",
    "authDomain": "mfademo-fa400.firebaseapp.com",
    "projectId": "mfademo-fa400",
    "storageBucket": "mfademo-fa400.appspot.com",
    "messagingSenderId": "968589107332",
    "appId": "1:968589107332:web:42f38c670392f2859922d1",
    "measurementId": "G-XW8RL344BF",
    "databaseURL" : "https://mfademo-fa400-default-rtdb.firebaseio.com/"
  }


firebase=pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()

window = Tk()
window.geometry("600x500")
window.resizable(False,False)
window.title("MFA app")
window.canvas = Canvas(window,bg = "white" , width="580", height="480").pack()

class Pages():
    def radio():
         global r0,r1,r2,contrvar
         r0=Label(window, text="MFA authentication demo", bg="white" , font="bold, 20")
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
    def show_mfa(key,z):
        if z>30:
            curr_time = datetime.now()
            sec = int(curr_time.strftime('%S'))
            #depending on the current second calculate how many seconds left before the next cycle
            if sec>30:
                t=60-sec
            elif sec==30:
                t=30
            elif sec<30:
                t=30-sec
        else:
            t=z
        
        text=StringVar()
        text_first="You have "
        text_last=" to enter the code"
        text=text_first+str(t)+text_last
        r0.config(text=text)
        t -= 1
        if t>0:
            window.after(1000,lambda: Pages.show_mfa(key,t))





    
def qrcodegen(link):
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
    imageLabel.config(image = photo)
    subLabel.config(text="Scan this code with Google Authenticator")

def generate():
    emailval=email.get()
    passval=password.get()
    db = firebase.database()
    if contrvar.get()=="1":
        #Register radio button enabled      
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
        #Login radio button enabled
        try:
            token = auth.sign_in_with_email_and_password(emailval, passval)
            result = db.child(token["localId"]).get().val()
            key=result["key"]
            #check potp value
            Pages.show_mfa(key,40)
        except Exception as e:
            error_json = e.args[1]
            print(error_json)
            error=json.loads(error_json)['error']['message']
            if error=="INVALID_PASSWORD" or error=="EMAIL_NOT_FOUND":
                 messagebox.showerror("Error","Username or password are incorrect")
                 
        #
        #

    #
    




Pages.radio()

imageLabel = Label(window,bg="white")
imageLabel.place(x=130, y=60)

subLabel = Label(window,text="",font="Bold, 14",bg="white")
subLabel.place(x=110, y=40)

window.mainloop()