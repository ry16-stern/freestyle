from tkinter import *
from tkinter import messagebox
import qrcode
from PIL import Image
  

class new(Toplevel):

 def __init__(self, master = None):
          
        super().__init__(master = master)
        self.title("New Window")
        self.geometry("500x500")
        Label(self, text ="This is a new Window").pack()
      
        #img = qrcode.make("test") #w.username.get()
        img = PhotoImage(file="qrcode_test.png")  
        Label(self,image = img,bg="white").pack()



class mfa():
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.resizable(False,False)
        self.title("MFA app")

    def Canvas(self):
        self.canvas = Canvas(self,bg = "white" , width="580", height="480")
        self.canvas.place(x=10, y=10)

        self.title = Label(self, text="MFA authentication demo", bg="white" , font="bold, 20")
        self.title.place(x=160,y=50)

        self.explainer = Label(self, text="This demo will ", bg="white" , font="14")
        self.explainer.place(x=50,y=100)

    def login_page(self):


        self.un_text=Label(self,text = "email", bg="white" , font="14")
        self.un_text.place(x=90, y=210)
        self.username = Entry(self, font="50", bd=3, relief=GROOVE)
        self.username.place(x = 170, y = 200,  width=300,  height=60)


        self.pw_text=Label(self,text = "password", bg="white" , font="14")
        self.pw_text.place(x=60, y=310)
        self.passw=Text(self, font="50", bd=3, relief=GROOVE)
        self.passw.place(x = 170, y = 300,  width=300,  height=60)

        self.login_btn = Button(self , text = "LOGIN" , bg="blue" , fg="white", command= self.login_fn, font="bold, 20")
        self.login_btn.place(width=200, height=60 , x=220 , y=400)
    
    def login_fn(self):

        img = qrcode.make(w.username.get())
        img.save('qrcode_test.png')
        new()


    def quit(self):
        self.destroy()



#def run_main():
#    w.Canvas()
#
#def run_sec():
#    w.login_page()
#
if __name__=="__main__":
    #w = mfa(Tk)
    master = Tk()
    new(master)

    #run_main()


    #run_sec()
    
    

    
    
        
    master.mainloop()
    
    


