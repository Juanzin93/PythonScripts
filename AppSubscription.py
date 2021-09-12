from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import time
import webbrowser
import tkinter.font as tkFont

AuthenticationWindow = Tk()
AuthenticationWindow.title("JuanBot 1.0.0 - Authentication")
AuthenticationWindow.iconbitmap('JtTechLogoIcon.ico')
#AuthenticationWindow.configure(background="black")
AuthenticationWindow.geometry("500x250")
AuthenticationWindow.resizable(False,False)

def callback(url):
    webbrowser.open_new(url)

imageSize = (500,400)
SignInLogo = Image.open("JtTechLogo.png")
showSignInLogo = ImageTk.PhotoImage(SignInLogo.resize(imageSize, Image.ANTIALIAS))
#showSignInLogo = ImageTk.PhotoImage(SignInLogo)
LogoLabel = Label(AuthenticationWindow, image=showSignInLogo) 
LogoLabel.place(x=-20, y=-120)


Label(AuthenticationWindow, text="Username", font=("Arial", 15), fg="black") .place(x=10, y=149)
Username = Entry(AuthenticationWindow, width=20, font=("Arial", 15), bg="white")
Username.place(x=180, y=150)
Username.focus()

Label(AuthenticationWindow, text="Password", font=("Arial", 15), fg="black") .place(x=10, y=184)
Password = Entry(AuthenticationWindow, width=20, font=("Arial", 15), bg="white", show="*")
Password.place(x=180, y=185)


RememberMe = IntVar()
Label(AuthenticationWindow, text="Remember me", font=("Arial", 13), fg="black") .place(x=35, y=215)
RememberMeChecked = Checkbutton(AuthenticationWindow, variable=RememberMe)
RememberMeChecked.place(x=10, y=216)

forgotpassword = Label(AuthenticationWindow, text="Forgot your password?", font=("Arial", 13), fg="blue", cursor="hand2")
forgotpassword.place(x=179, y=215)
f = tkFont.Font(forgotpassword, forgotpassword.cget("font"))
f.configure(underline = True)
forgotpassword.configure(font=f)
forgotpassword.bind("<Button-1>", lambda e: callback("http://www.google.com"))

arrowSize = (20,30)
LoginArrow = Image.open("rightarrowEnter.png")
showLoginArrow = ImageTk.PhotoImage(LoginArrow.resize(arrowSize, Image.ANTIALIAS))
#showLoginArrow = ImageTk.PhotoImage(LoginArrow)
LoginArrowLabel = Label(AuthenticationWindow, image=showLoginArrow, cursor="hand2") 
LoginArrowLabel.place(x=430, y=163)
LoginArrowLabel.bind("<Button-1>", lambda e: callback("http://www.google.com"))

AuthenticationWindow.mainloop()