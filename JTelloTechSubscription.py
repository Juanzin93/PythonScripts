from tkinter import *
from tkinter import ttk, filedialog, messagebox
import tkinter as tk
from PIL import Image, ImageTk
import os
import time
import webbrowser
import tkinter.font as tkFont
import mysql.connector as mysql
import subprocess
from datetime import date, timedelta
import socket

AuthenticationWindow = Tk()
AuthenticationWindow.title("JTelloTech 1.0.0 - Authentication")
AuthenticationWindow.iconbitmap('JtTechLogoIcon.ico')
#AuthenticationWindow.configure(background="black")
AuthenticationWindow.geometry("500x250")
AuthenticationWindow.resizable(False,False)


HEADER = 64
PORT = 9316
SERVER = "test.bestserverglobal.com"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

databaseData = []
try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    def send(msg):
        message = msg.encode(FORMAT)
        msgLength = len(message)
        sendLength = str(msgLength).encode(FORMAT)
        sendLength += b' ' * (HEADER - len(sendLength))
        client.send(sendLength)
        client.send(message)
        from_server = client.recv(HEADER).decode(FORMAT)
        if from_server:
            databaseData.append(from_server)

    send("getDatabaseHost")
    send("getDatabaseUser")
    send("getDatabasePassword")
    send("getDatabaseTable")
    send("getDatabasePort")
    send(DISCONNECT_MESSAGE)

    JtTechDb = mysql.connect(
        host = databaseData[0],
        user = databaseData[1],
        passwd = databaseData[2],
        database = databaseData[3],
        port = databaseData[4],
    )
except:
    messagebox.showerror("Error", "Unable to connect to server.")
    AuthenticationWindow.destroy()

def on_close():
    JtTechDb.close()
    AuthenticationWindow.destroy()

AuthenticationWindow.protocol("WM_DELETE_WINDOW",  on_close)

def callback(url):
    webbrowser.open_new(url)

def bindedTechLogin(self):
    JtTechLogin()

currentDateInSeconds = int(time.time())
currentDateInSecondsLabel = Label(AuthenticationWindow, text="", font=("Arial", 15), fg="black") 
currentDateInSecondsLabel.place(x=1008, y=100)

def checkTime():
    global currentDateInSeconds
    currentDateInSeconds = int(time.time())
    currentDateInSecondsLabel.config(text="currentDateInSeconds")

    currentDateInSecondsLabel.after(1000, checkTime)
    #print(currentDateInSeconds)
    
checkTime()

def JtTechLogin():
    #print(JtTechDb)
    cursor = JtTechDb.cursor()
    #cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
    #            id integer PRIMARY KEY AUTO_INCREMENT,
    #            Username TEXT,
    #            Password TEXT,
    #            Plan integer NOT NULL DEFAULT 0,
    #            days integer NOT NULL DEFAULT 0,
    #            lastday integer NOT NULL DEFAULT 0,
    #            FirstName TEXT,
    #            MiddleName TEXT,
    #            LastName TEXT,
    #            email TEXT,
    #            phone TEXT,
    #            address TEXT,
    #            apt TEXT,
    #            city TEXT,
    #            state TEXT,
    #            zip TEXT)''')
    cursor.execute('SELECT * from Users')
    Users = cursor.fetchall()
    
    def AdminPanel():
        AdminPanelWindow = Toplevel()
        AdminPanelWindow.title("JTelloTech Admin Panel 1.0.0")
        AdminPanelWindow.iconbitmap('JtTechLogoIcon.ico')
        AdminPanelWindow.geometry("600x250")
        AdminPanelWindow.resizable(False,False)
        Label(AdminPanelWindow, text="Username:", font=("Arial", 15), fg="black") .place(x=18, y=5)
        usernameLabel = Label(AdminPanelWindow, text="", font=("Arial", 15), fg="black")
        usernameLabel.place(x=120, y=5)
        Label(AdminPanelWindow, text="Membership Days:", font=("Arial", 15), fg="black") .place(x=18, y=50)
        membershipLabel = Label(AdminPanelWindow, text="", font=("Arial", 15), fg="black") 
        membershipLabel.place(x=200, y=50)
        Label(AdminPanelWindow, text="Add days:", font=("Arial", 15), fg="black") .place(x=18, y=100)
        AddDaysEntry = Entry(AdminPanelWindow, width=5, font=("Arial", 15), bg="white")
        AddDaysEntry.place(x=120, y=100)
        AddDaysEntry.focus()
        Label(AdminPanelWindow, text="Remove days:", font=("Arial", 15), fg="black") .place(x=18, y=150)
        RemoveDaysEntry = Entry(AdminPanelWindow, width=5, font=("Arial", 15), bg="white")
        RemoveDaysEntry.place(x=150, y=150)
        memberID = Label(AdminPanelWindow, text="", font=("Arial", 15), fg="black") 
        memberID.place(x=250, y=250)

        userListFrame = Frame(AdminPanelWindow)
        userListFrame.place(relwidth=0.3, relheight=0.7, x=400,y=10)
        userListScrollBar = Scrollbar(userListFrame, orient=VERTICAL)

        userList = Listbox(AdminPanelWindow, yscrollcommand=userListScrollBar.set)
        userList.place(relwidth=0.27, relheight=0.7, x=400,y=10)
        userListScrollBar.config(command=userList.yview)
        userListScrollBar.pack(side=RIGHT, fill=Y)

        userSearchEntry = Entry(AdminPanelWindow, font=("Helvetica", 15), width=14, bg="white", fg="grey")
        userSearchEntry.place(x=400, y=200)
        userSearchEntry.insert(0, "Search Users...")
        
        def updateMembershipTime():
            UserIdGot = memberID.cget("text")
            cursor.execute('SELECT lastday from Users WHERE id=%s',[UserIdGot])
            getlastday = [x[0] for x in cursor.fetchall()]
            lastday = getlastday[0]
            if lastday == 0:
                membershipLabel.config(text=lastday)
                #membershipLabel.after(1000,updateMembershipTime)
                print("a")
            else:
                daysleft = timedelta(seconds=(lastday - currentDateInSeconds))
                membershipLabel.config(text=daysleft)
                membershipLabel.after(1000,updateMembershipTime)
        
        def UpdateUser(data):  
            userList.delete(0, END)

            for user in data:
                userList.insert(END, user)

        def SearchUser(search):
            searched = userSearchEntry.get()

            #cursor.execute('SELECT * from Users')
            #users = cursor.fetchall()
            if searched == '':
                data = []
                for user in Users:
                    data.append(user[1])
            else:
                data = []
                for user in Users:
                    userName = user[1]
                    if searched.lower() in userName.lower():
                        data.append(userName)

            UpdateUser(sorted(data))

        def LoadUser(self):
            global currentDateInSeconds
            cursor.execute('SELECT * from Users')
            users = cursor.fetchall()
            try:
                loadedUser = userList.get(userList.curselection())
            except:
                messagebox.showerror("Error", "You must select a client from the list.")
                return
            
            for userx in users:
                if userx[1] == loadedUser:
                    memberID.config(text=userx[0])
                    usernameLabel.config(text=userx[1])
                    if userx[5] == 0:
                        daysleft = 0
                    else:
                        daysleft = timedelta(seconds=(userx[5] - currentDateInSeconds))
                    
                    membershipLabel.config(text=daysleft)
                    break

                
            updateMembershipTime()
                
        def onSearchUserClick(event):
            if userSearchEntry.get() == "Search Users...":
                userSearchEntry.delete(0, END)
                userSearchEntry.insert(0, "")
                userSearchEntry.config(fg="black")

        def onSearchUserFocusOut(event):
            if userSearchEntry.get() == "":
                userSearchEntry.insert(0, "Search Users...")
                userSearchEntry.config(fg="grey")

        for user in Users:
            data = []
            for user in Users:
                data.append(user[1])
            users = sorted(data)
            UpdateUser(sorted(users))

        userList.bind("<Double-Button-1>", LoadUser)
        userSearchEntry.bind("<KeyRelease>", SearchUser)
        userSearchEntry.bind("<FocusIn>", onSearchUserClick)
        userSearchEntry.bind("<FocusOut>", onSearchUserFocusOut)

        def addMembershipDays():
            UserIdGot = memberID.cget("text")
            cursor.execute('SELECT lastday from Users WHERE id=%s', [UserIdGot])
            userLastDay = [ x[0] for x in cursor.fetchall()]
            EndingDateInSeconds = userLastDay[0]
            addDays = int(AddDaysEntry.get()) * 24 * 60 * 60

            if EndingDateInSeconds == 0:
                daysAdded = currentDateInSeconds + addDays
            else:
                leftOvers = EndingDateInSeconds - currentDateInSeconds
                print(leftOvers)
                print(addDays)
                daysAdded = currentDateInSeconds + addDays + leftOvers
                print(daysAdded)
            newDate = timedelta(seconds=daysAdded)
            oldDate = timedelta(seconds=currentDateInSeconds)
            newDay = int(newDate.days - oldDate.days)
            print(newDate.days)
            print(oldDate.days)
            print(newDay)
            MemberUserID = int(memberID.cget("text"))
            cursor.execute('UPDATE Users SET lastday=%s, days=%s WHERE id=%s', (daysAdded, newDay, MemberUserID))
            JtTechDb.commit()
            membershipLabel.config(text=newDay)
        
        def removeMembershipDays():
            UserIdGot = memberID.cget("text")
            cursor.execute('SELECT lastday from Users WHERE id=%s', [UserIdGot])
            userLastDay = [ x[0] for x in cursor.fetchall()]
            EndingDateInSeconds = userLastDay[0]
            removeDays = int(RemoveDaysEntry.get()) * 24 * 60 * 60

            leftOvers = EndingDateInSeconds - currentDateInSeconds

            daysRemoved = (currentDateInSeconds + leftOvers) - removeDays
            print(daysRemoved)
            newDate = timedelta(seconds=daysRemoved)
            oldDate = timedelta(seconds=currentDateInSeconds)
            newDay = int(newDate.days - oldDate.days)
            print(newDate.days)
            print(oldDate.days)
            print(newDay)
            MemberUserID = int(memberID.cget("text"))
            cursor.execute('UPDATE Users SET lastday=%s, days=%s WHERE id=%s', (daysRemoved, newDay, MemberUserID))
            JtTechDb.commit()
            membershipLabel.config(text=newDay)

        def OpenApp():
            subprocess.Popen('python msQuoterWithSub.py')
            AuthenticationWindow.destroy()

        AddDaysButton = tk.Button(AdminPanelWindow, text="Add", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=addMembershipDays)
        AddDaysButton.place(x=30, y=200)            

        RemoveDaysButton = tk.Button(AdminPanelWindow, text="Remove", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=removeMembershipDays)
        RemoveDaysButton.place(x=150, y=200)  
        
        OpenAppButton = tk.Button(AdminPanelWindow, text="Open App", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=OpenApp)
        OpenAppButton.place(x=270, y=200)  

    AdminUser = Users[0]
    for user in Users:
        UserUsername = user[1]
        UserPassword = user[2]
        UserPlan = user[3]
        EndingDateInSecondos = user[5]    
        
        if UserUsername == Username.get() and UserPassword == Password.get():
            if UserPlan == 999:
                AdminPanel()
                break
            if EndingDateInSecondos >= currentDateInSeconds:
                subprocess.Popen('python msQuoterWithSub.py')
                AuthenticationWindow.destroy()
            else:
                Label(AuthenticationWindow, text="Your membership has expired.", fg="red") .place(x=180, y=129)
            break
        else:
            Label(AuthenticationWindow, text="Wrong username or password.", fg="red") .place(x=180, y=129)

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
Password.bind("<Return>", bindedTechLogin)


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
LoginArrowLabel.bind("<Button-1>", lambda e: JtTechLogin())

AuthenticationWindow.mainloop()