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
from datetime import datetime, timedelta
import socket
import base64
import smtplib as smtp
import ssl
import imghdr
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes
import random
import string

getUsername = ""
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
    
def has_letters(inputString):
    return any(char.isalpha() for char in inputString)

def forgotPassword():
    ForgotPasswordWindow = Toplevel()
    ForgotPasswordWindow.title("Recover Password")
    ForgotPasswordWindow.iconbitmap('JtTechLogoIcon.ico')
    ForgotPasswordWindow.geometry("300x180")
    ForgotPasswordWindow.resizable(False,False)
    recoverFrame = Frame(ForgotPasswordWindow)
    confirmationLabel = Label(recoverFrame, text="", font=("Arial", 15), fg="black") 
    confirmationLabel.place(x=10, y=30)
    recoverFrame.place(relwidth=1, relheight=1, x=0,y=0)
    codeFrame = Frame(ForgotPasswordWindow)
    codeFrame.place_forget()
    resetPasswordFrame = Frame(ForgotPasswordWindow)
    resetPasswordFrame.place_forget()
    Label(recoverFrame, text="Email:", font=("Arial", 15), fg="black") .place(x=10, y=5)
    emailEntry = Entry(recoverFrame, width=15, font=("Arial", 15), bg="white")
    emailEntry.place(x=80, y=5)
    emailEntry.focus()
    send("SMTPSSL")
    send("SMTPPORT")
    send("SMTPEMAIL")
    send("SMTPPASSWORD")
    def sendRecoverEmail():
        port = int(databaseData[6])
        sender = databaseData[7]
        senderPassword = databaseData[8]

        receiver = emailEntry.get()
        cursor = JtTechDb.cursor(buffered=True)
        try:
            cursor.execute('SELECT * from Users WHERE email=%s', [receiver])
            for getData in cursor.fetchall():
                global getUsername
                getUsername = getData[1]

        except:
            Label(recoverFrame, text="Email does not match with our database.", font=("Arial", 15), fg="black") .place(x=10, y=30)

        if getUsername != "":        
            now = datetime.now()
            d4 = now.strftime("%b %d, %Y, %H:%M %I %Z")
            message = EmailMessage()
            message['Subject'] = "Recover password"
            message['From'] = sender
            message['To'] = receiver
            #message['Date'] = d4
            letters = string.ascii_letters
            code = ''.join(random.choice(letters) for i in range(15))
            message.set_content(f'''A lost account process has been initiated on your JTelloTech account
            
            Here is the Username registered to this email in case your forgot it: <b>{getUsername}</b>
            Your reset password code is <b>{code}</b>.
             Your code will expire in 24 hours.
             Thank you for choosing Jtellotech! We appreciate your business.
            ''')
            image_cid = make_msgid(domain='jtellotech.com')
            codeExpDate = int(time.time()) + (24 * 60 * 60)
            cursor.execute('''UPDATE Users SET recoveryCode=%s, codeExpDate=%s WHERE email=%s''', 
                                (code, codeExpDate, receiver)) 
            JtTechDb.commit()
            message.add_alternative('''\
            <!DOCTYPE html>
            <html>
                <body>
                    <h2>A lost account process has been initiated on your JTelloTech account</h2>
                    <h2></h2>
                    <h3>Here is the Username registered to this email in case your forgot it: <b>{getUsername}</b></h3>
                    <h2></h2>
                    <h3>Your reset password code is <b>{code}</b>.</h3>
                    <h3> Your code will expire in 24 hours.</h3>
                    
                    <h3></h3>
                    <h3> Thank you for choosing Jtellotech! We appreciate your business.</h3>
                    
                </body>
            </html>
            '''.format(getUsername=getUsername, code=code), subtype='html')
            #<img src="cid:{image_cid}", alt="">
            # image_cid=image_cid[1:-1], 
            # image_cid looks like <long.random.number@xyz.com>
            # to use it as the img src, we don't need `<` or `>`
            # so we use [1:-1] to strip them off


            # now open the image and attach it to the email
            with open('JtTechLogo.png', 'rb') as img:

                # know the Content-Type of the image
                maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

                # attach it
                message.get_payload()[1].add_related(img.read(), 
                                                    maintype=maintype, 
                                                    subtype=subtype, 
                                                    cid=image_cid)

            context = ssl.create_default_context()
            # image attachment
        #with open("JtTechLogo.png", 'rb') as attach:
        #    attachmentData = attach.read()
        #    attachmentType = imghdr.what(attach.name)
        #    attachmentName = attach.name
        #
        #message.add_attachment(attachmentData, maintype='image', subtype=attachmentType, filename=attachmentName)
        
            # pdf attachment
            #with open("documents/JUAN FELLIPE BRAGANCA TELLO - ITIN.pdf", 'rb') as attach:
            #   attachmentData = attach.read()
            #   filename = attach.name
            #   splittedName = filename.split("/")
            #   attachmentName = splittedName[1]
        #
            #message.add_attachment(attachmentData, maintype='application', subtype='octet-stream', filename=attachmentName)


            with smtp.SMTP(databaseData[5], port) as server:
                server.login(sender, senderPassword)
                server.send_message(message)

            confirmationLabel.config(text="Email sent.")
            getUsername = ""
            recoverFrame.place_forget()
            codeFrame.place(relwidth=1, relheight=1, x=0,y=0)
            Label(codeFrame, text=f"A confirmation code has been sent to\n{receiver}.", font=("Arial", 12), fg="black") .place(x=10, y=5)
            Label(codeFrame, text="Code:", font=("Arial", 15), fg="black") .place(x=10, y=50)
            codeEntry = Entry(codeFrame, width=15, font=("Arial", 15), bg="white")
            codeEntry.place(x=80, y=50)
            codeEntry.focus()
            codeMsg = Label(codeFrame, text="", font=("Arial", 12), fg="black")
            codeMsg.place(x=30, y=120)
            def passwordNext():
                cursor.execute('SELECT recoveryCode from Users WHERE email=%s', [receiver])
                recCode = cursor.fetchone()
                cursor.execute('SELECT codeExpDate from Users WHERE email=%s', [receiver])
                codeExpiration = cursor.fetchone()
                if recCode[0] == codeEntry.get() and codeExpiration[0] > int(time.time()):
                    codeFrame.place_forget()
                    resetPasswordFrame.place(relwidth=1, relheight=1, x=0,y=0)
                    Label(resetPasswordFrame, text="New Password:", font=("Arial", 15), fg="black") .place(x=2, y=10)
                    newPassword = Entry(resetPasswordFrame, width=12, font=("Arial", 15), bg="white", show="*")
                    newPassword.place(x=150, y=10)
                    newPassword.focus()
                    Label(resetPasswordFrame, text="Confirm:", font=("Arial", 15), fg="black") .place(x=2, y=50)
                    passwordConfirm = Entry(resetPasswordFrame, width=12, font=("Arial", 15), bg="white", show="*")
                    passwordConfirm.place(x=120, y=50)
                    def resetsPassword():
                        if len(newPassword.get()) >= 8:
                            if has_numbers(newPassword.get()) and has_letters(newPassword.get()):
                                if newPassword.get() == passwordConfirm.get():
                                    newPass = base64.b64encode(f"{newPassword.get()}".encode('utf-8'))
                                    cursor.execute('SELECT Password from Users WHERE email=%s', [receiver])
                                    oldPassword = cursor.fetchone()
                                    if newPass == oldPassword[0]:
                                        cursor.execute('''UPDATE Users SET Password=%s WHERE email=%s''', (newPass, receiver))
                                        JtTechDb.commit()
                                        ForgotPasswordWindow.destroy()
                                        messagebox.showinfo("Success", "Password changed!")
                                    else:
                                        confiLabel.config(text="Password can't be the same\n as a previous password.")
                                else:
                                    confiLabel.config(text="Passwords do not match.")
                            else:
                                confiLabel.config(text="You password must contain letters\n and numbers.")
                        else:
                            confiLabel.config(text="Your password must contain at least\n 8 letters or numbers.")

                    resetPass = tk.Button(resetPasswordFrame, text="Reset Password", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=resetsPassword)
                    resetPass.place(x=80, y=80)
                    confiLabel = Label(resetPasswordFrame, text="", font=("Arial", 12), fg="black")
                    confiLabel.place(x=2, y=120)
                    
                else:
                    codeMsg.config(text="Wrong code or code expired.")

            nextWindow = tk.Button(codeFrame, text="Next", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=passwordNext)
            nextWindow.place(x=100, y=80)  
        else:
            confirmationLabel.config(text="Email does not match database.")

    sendEmail = tk.Button(recoverFrame, text="Recover", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=sendRecoverEmail)
    sendEmail.place(x=100, y=80)

AuthenticationWindow = Tk()
AuthenticationWindow.title("JTelloTech - Authentication")
AuthenticationWindow.iconbitmap('JtTechLogoIcon.ico')
AuthenticationWindow.geometry("500x270")
AuthenticationWindow.resizable(False,False)


HEADER = 64
PORT = 9316
SERVER = "test.bestserverglobal.com"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

databaseData = []

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' * (HEADER - len(sendLength))
    client.send(sendLength)
    client.send(message)
    from_server = client.recv(HEADER).decode(FORMAT)
    if from_server and from_server != "KEEP ALIVE":
        databaseData.append(from_server)

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    send("getDatabaseHost")
    send("getDatabaseUser")
    send("getDatabasePassword")
    send("getDatabaseMainTable")
    send("getDatabasePort")
except:
    messagebox.showerror("Error", "Unable to connect to server.")
    AuthenticationWindow.destroy()


try:
    JtTechDb = mysql.connect(
        host = databaseData[0],
        user = databaseData[1],
        passwd = databaseData[2],
        database = databaseData[3],
        port = databaseData[4],
    )
except:
    messagebox.showerror("Error", "Unable to connect to database.")
    AuthenticationWindow.destroy()

def on_close():
    try:
        JtTechDb.close()
    except:
        pass
    try:
        send(DISCONNECT_MESSAGE)
    except:
        pass
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
    cursor = JtTechDb.cursor(buffered=True)
    #cursor.execute('''CREATE TABLE IF NOT EXISTS Users(
    #            id integer PRIMARY KEY AUTO_INCREMENT,
    #            Username TEXT,
    #            Password TEXT,
    #            Plan integer NOT NULL DEFAULT 0,
    #            days integer NOT NULL DEFAULT 0,
    #            lastday integer NOT NULL DEFAULT 0,
    #            userDatabase TEXT,
    #            FirstName TEXT,
    #            MiddleName TEXT,
    #            LastName TEXT,
    #            email TEXT,
    #            phone TEXT,
    #            address TEXT,
    #            apt TEXT,
    #            city TEXT,
    #            state TEXT,
    #            zip TEXT,
    #            recoveryCode TEXT,
    #            codeExpDate integer NOT NULL DEFAULT 0)''')
    cursor.execute('SELECT * from Users')
    Users = cursor.fetchall()
    
    def AdminPanel():
        AdminPanelWindow = Toplevel()
        AdminPanelWindow.title("JTelloTech Admin Panel")
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
        
        def CreateUserWind():
            createUserWindow = Toplevel()
            createUserWindow.title("JTelloTech Create User")
            createUserWindow.iconbitmap('JtTechLogoIcon.ico')
            createUserWindow.geometry("550x500")
            createUserWindow.resizable(False,False)

            Label(createUserWindow, text="Username:", font=("Arial", 15), fg="black") .place(x=10, y=10)
            NewUserUsername = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserUsername.place(x=110, y=10)
            NewUserUsername.focus()
            
            Label(createUserWindow, text="Password:", font=("Arial", 15), fg="black") .place(x=10, y=50)
            NewUserPassword = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserPassword.place(x=110, y=50)
            
            Label(createUserWindow, text="Plan:", font=("Arial", 15), fg="black") .place(x=10, y=90)
            NewUserPlan = Entry(createUserWindow, width=5, font=("Arial", 15), bg="white")
            NewUserPlan.place(x=70, y=90)
            
            Label(createUserWindow, text="Database:", font=("Arial", 15), fg="black") .place(x=10, y=130)
            NewUserDatabase = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserDatabase.place(x=110, y=130)
            
            Label(createUserWindow, text="First Name:", font=("Arial", 15), fg="black") .place(x=10, y=170)
            NewUserFirstName = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserFirstName.place(x=120, y=170)
            
            Label(createUserWindow, text="Middle Name:", font=("Arial", 15), fg="black") .place(x=10, y=210)
            NewUserMiddleName = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserMiddleName.place(x=130, y=210)
            
            Label(createUserWindow, text="Last Name:", font=("Arial", 15), fg="black") .place(x=10, y=250)
            NewUserLastName = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserLastName.place(x=120, y=250)
            
            Label(createUserWindow, text="Email:", font=("Arial", 15), fg="black") .place(x=10, y=290)
            NewUserEmail = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserEmail.place(x=80, y=290)
            
            Label(createUserWindow, text="Phone:", font=("Arial", 15), fg="black") .place(x=10, y=330)
            NewUserPhone = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserPhone.place(x=90, y=330)
            
            Label(createUserWindow, text="Address:", font=("Arial", 15), fg="black") .place(x=10, y=370)
            NewUserAddress = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserAddress.place(x=100, y=370)
            
            Label(createUserWindow, text="Apt:", font=("Arial", 15), fg="black") .place(x=280, y=370)
            NewUserApt = Entry(createUserWindow, width=5, font=("Arial", 15), bg="white")
            NewUserApt.place(x=320, y=370)
            
            Label(createUserWindow, text="City:", font=("Arial", 15), fg="black") .place(x=10, y=410)
            NewUserCity = Entry(createUserWindow, width=15, font=("Arial", 15), bg="white")
            NewUserCity.place(x=60, y=410)
            
            Label(createUserWindow, text="State:", font=("Arial", 15), fg="black") .place(x=240, y=410)
            NewUserState = Entry(createUserWindow, width=5, font=("Arial", 15), bg="white")
            NewUserState.place(x=300, y=410)
            
            Label(createUserWindow, text="Zip:", font=("Arial", 15), fg="black") .place(x=360, y=410)
            NewUserZip = Entry(createUserWindow, width=10, font=("Arial", 15), bg="white")
            NewUserZip.place(x=400, y=410)

            def createUser():
                encryotedPassword = base64.b64encode(f"{NewUserPassword.get()}".encode('utf-8'))
                recCodeTemp = "HBUgra524wgIUSI34RB"
                cursor.execute('''INSERT INTO Users (Username, Password, Plan, userDatabase,
                            FirstName, MiddleName, LastName, email, phone, address, apt, city, state, zip, recoveryCode) 
                            VALUES (%s, %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
                            [NewUserUsername.get(), encryotedPassword, NewUserPlan.get(), NewUserDatabase.get(),
                            NewUserFirstName.get(), NewUserMiddleName.get(), NewUserLastName.get(),
                            NewUserEmail.get(), NewUserPhone.get(), NewUserAddress.get(),
                            NewUserApt.get(), NewUserCity.get(), NewUserState.get(),
                                NewUserZip.get(), recCodeTemp])
                JtTechDb.commit()
                cursor.execute('SELECT * from Users')
                UsersDB = cursor.fetchall()

                for user in UsersDB:
                    data = []
                    for user in UsersDB:
                        data.append(user[1])
                    users = sorted(data)
                    UpdateUser(sorted(users))
                
                createUserWindow.destroy()
                messagebox.showinfo("Success", "New User Created!")
                
            CreateUserButton = tk.Button(createUserWindow, text="Create", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=createUser)
            CreateUserButton.place(x=230, y=450)            
        
        def ManageUserWind():
            ManageUserWindow = Toplevel()
            ManageUserWindow.title("JTelloTech Manage User")
            ManageUserWindow.iconbitmap('JtTechLogoIcon.ico')
            ManageUserWindow.geometry("550x500")
            ManageUserWindow.resizable(False,False)
            
            UserId = Label(ManageUserWindow, text="a", font=("Arial", 15), fg="black") 
            UserId.place(x=330, y=10)

            Label(ManageUserWindow, text="Username:", font=("Arial", 15), fg="black") .place(x=10, y=10)
            ManageUserUsername = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserUsername.place(x=110, y=10)
            ManageUserUsername.focus()
            
            Label(ManageUserWindow, text="Password:", font=("Arial", 15), fg="black") .place(x=10, y=50)
            ManageUserPassword = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserPassword.place(x=110, y=50)
            
            Label(ManageUserWindow, text="Plan:", font=("Arial", 15), fg="black") .place(x=10, y=90)
            ManageUserPlan = Entry(ManageUserWindow, width=5, font=("Arial", 15), bg="white")
            ManageUserPlan.place(x=70, y=90)
            
            Label(ManageUserWindow, text="Database:", font=("Arial", 15), fg="black") .place(x=10, y=130)
            ManageUserDatabase = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserDatabase.place(x=110, y=130)
            
            Label(ManageUserWindow, text="First Name:", font=("Arial", 15), fg="black") .place(x=10, y=170)
            ManageUserFirstName = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserFirstName.place(x=120, y=170)
            
            Label(ManageUserWindow, text="Middle Name:", font=("Arial", 15), fg="black") .place(x=10, y=210)
            ManageUserMiddleName = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserMiddleName.place(x=130, y=210)
            
            Label(ManageUserWindow, text="Last Name:", font=("Arial", 15), fg="black") .place(x=10, y=250)
            ManageUserLastName = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserLastName.place(x=120, y=250)
            
            Label(ManageUserWindow, text="Email:", font=("Arial", 15), fg="black") .place(x=10, y=290)
            ManageUserEmail = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserEmail.place(x=80, y=290)
            
            Label(ManageUserWindow, text="Phone:", font=("Arial", 15), fg="black") .place(x=10, y=330)
            ManageUserPhone = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserPhone.place(x=90, y=330)
            
            Label(ManageUserWindow, text="Address:", font=("Arial", 15), fg="black") .place(x=10, y=370)
            ManageUserAddress = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserAddress.place(x=100, y=370)
            
            Label(ManageUserWindow, text="Apt:", font=("Arial", 15), fg="black") .place(x=280, y=370)
            ManageUserApt = Entry(ManageUserWindow, width=5, font=("Arial", 15), bg="white")
            ManageUserApt.place(x=320, y=370)
            
            Label(ManageUserWindow, text="City:", font=("Arial", 15), fg="black") .place(x=10, y=410)
            ManageUserCity = Entry(ManageUserWindow, width=15, font=("Arial", 15), bg="white")
            ManageUserCity.place(x=60, y=410)
            
            Label(ManageUserWindow, text="State:", font=("Arial", 15), fg="black") .place(x=240, y=410)
            ManageUserState = Entry(ManageUserWindow, width=5, font=("Arial", 15), bg="white")
            ManageUserState.place(x=300, y=410)
            
            Label(ManageUserWindow, text="Zip:", font=("Arial", 15), fg="black") .place(x=360, y=410)
            ManageUserZip = Entry(ManageUserWindow, width=10, font=("Arial", 15), bg="white")
            ManageUserZip.place(x=400, y=410)

            userListFrame2 = Frame(ManageUserWindow)
            userListFrame2.place(relwidth=0.28, relheight=0.37, x=360,y=10)
            userListScrollBar2 = Scrollbar(userListFrame2, orient=VERTICAL)

            userList2 = Listbox(ManageUserWindow, yscrollcommand=userListScrollBar2.set)
            userList2.place(relwidth=0.3, relheight=0.37, x=360,y=10)
            userListScrollBar2.config(command=userList2.yview)
            userListScrollBar2.pack(side=RIGHT, fill=Y)

            userSearchEntry2 = Entry(ManageUserWindow, font=("Helvetica", 15), width=14, bg="white", fg="grey")
            userSearchEntry2.place(x=360, y=200)
            userSearchEntry2.insert(0, "Search Users...")

            def UpdateUser2(data):  
                userList2.delete(0, END)

                for user in data:
                    userList2.insert(END, user)

            cursor.execute('SELECT * from Users')
            UsersDB = cursor.fetchall()
            for user in UsersDB:
                    data = []
                    for user in UsersDB:
                        data.append(user[1])
                    users = sorted(data)
                    UpdateUser2(sorted(users))
            
            def SearchUser2(search):
                searched = userSearchEntry2.get()

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

                UpdateUser2(sorted(data))

            def SaveUser():
                getUserId = UserId.cget("text")
                encryptedPassword = base64.b64encode(f"{ManageUserPassword.get()}".encode('utf-8'))
                cursor.execute('''UPDATE Users SET Username=%s, Password=%s, Plan=%s, userDatabase=%s,
                                                    FirstName=%s, MiddleName=%s, LastName=%s, email=%s,
                                                    phone=%s, address=%s, apt=%s, city=%s,
                                                    state=%s, zip=%s WHERE id=%s''', 
                            (ManageUserUsername.get(), encryptedPassword, ManageUserPlan.get(), ManageUserDatabase.get(),
                            ManageUserFirstName.get(), ManageUserMiddleName.get(), ManageUserLastName.get(), ManageUserEmail.get(),
                            ManageUserPhone.get(), ManageUserAddress.get(), ManageUserApt.get(), ManageUserCity.get(),
                            ManageUserState.get(), ManageUserZip.get(), getUserId))
                JtTechDb.commit()
                cursor.execute('SELECT * from Users')
                UsersDB = cursor.fetchall()

                for user in UsersDB:
                    data = []
                    for user in UsersDB:
                        data.append(user[1])
                    users = sorted(data)
                    UpdateUser2(sorted(users))
                
                messagebox.showinfo("Success", "User Updated!")

            def LoadUser2(self):
                cursor.execute('SELECT * from Users')
                users = cursor.fetchall()
                try:
                    loadedUser2 = userList2.get(userList2.curselection())
                except:
                    messagebox.showerror("Error", "You must select a client from the list.")
                    return
                
                for userx in users:
                    if userx[1] == loadedUser2:
                        UserId.config(text=userx[0])
                        ManageUserUsername.delete(0, END)
                        ManageUserUsername.insert(0, userx[1])

                        ManageUserPassword.delete(0, END)
                        dencryptedPassword = base64.b64decode(userx[2]).decode('utf-8')
                        ManageUserPassword.insert(0, dencryptedPassword)

                        ManageUserPlan.delete(0, END)
                        ManageUserPlan.insert(0, userx[3])
                        
                        ManageUserDatabase.delete(0, END)
                        ManageUserDatabase.insert(0, userx[6])
                        
                        ManageUserFirstName.delete(0, END)
                        ManageUserFirstName.insert(0, userx[7])
                        
                        ManageUserMiddleName.delete(0, END)
                        ManageUserMiddleName.insert(0, userx[8])
                        
                        ManageUserLastName.delete(0, END)
                        ManageUserLastName.insert(0, userx[9])
                        
                        ManageUserEmail.delete(0, END)
                        ManageUserEmail.insert(0, userx[10])
                        
                        ManageUserPhone.delete(0, END)
                        ManageUserPhone.insert(0, userx[11])
                        
                        ManageUserAddress.delete(0, END)
                        ManageUserAddress.insert(0, userx[12])
                        
                        ManageUserApt.delete(0, END)
                        ManageUserApt.insert(0, userx[13])
                        
                        ManageUserCity.delete(0, END)
                        ManageUserCity.insert(0, userx[14])
                        
                        ManageUserState.delete(0, END)
                        ManageUserState.insert(0, userx[15])
                        
                        ManageUserZip.delete(0, END)
                        ManageUserZip.insert(0, userx[16])
                        break
                

            def onSearchUserClick2(event):
                if userSearchEntry2.get() == "Search Users...":
                    userSearchEntry2.delete(0, END)
                    userSearchEntry2.insert(0, "")
                    userSearchEntry2.config(fg="black")

            def onSearchUserFocusOut2(event):
                if userSearchEntry2.get() == "":
                    userSearchEntry2.insert(0, "Search Users...")
                    userSearchEntry2.config(fg="grey")

            userList2.bind("<Double-Button-1>", LoadUser2)
            userSearchEntry2.bind("<KeyRelease>", SearchUser2)
            userSearchEntry2.bind("<FocusIn>", onSearchUserClick2)
            userSearchEntry2.bind("<FocusOut>", onSearchUserFocusOut2)

            UpdateUserButton = tk.Button(ManageUserWindow, text="Update", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=SaveUser)
            UpdateUserButton.place(x=230, y=450)   

        AddDaysButton = tk.Button(AdminPanelWindow, text="Add", font=("Arial", 13), padx=10, pady=1, fg="white", bg="#263D42", command=addMembershipDays)
        AddDaysButton.place(x=10, y=200)            

        RemoveDaysButton = tk.Button(AdminPanelWindow, text="Remove", font=("Arial", 13), padx=10, pady=1, fg="white", bg="#263D42", command=removeMembershipDays)
        RemoveDaysButton.place(x=80, y=200)     

        ManageUsersButton = tk.Button(AdminPanelWindow, text="Manage", font=("Arial", 13), padx=10, pady=1, fg="white", bg="#263D42", command=ManageUserWind)
        ManageUsersButton.place(x=180, y=200)  
                
        OpenAppButton = tk.Button(AdminPanelWindow, text="Open App", font=("Arial", 13), padx=10, pady=1, fg="white", bg="#263D42", command=OpenApp)
        OpenAppButton.place(x=290, y=200)  
        
        CreateUserButton = tk.Button(AdminPanelWindow, text="Create User", font=("Arial", 13), padx=10, pady=1, fg="white", bg="#263D42", command=CreateUserWind)
        CreateUserButton.place(x=270, y=8)  

    for user in Users:
        UserUsername = user[1]
        UserPassword = base64.b64decode(user[2]).decode('utf-8')
        UserPlan = user[3]
        EndingDateInSecondos = user[5]
        userDatabase = user[6]
        
        if UserUsername == Username.get() and UserPassword == Password.get():
            if RememberMe.get() == 1:
                stringDoRemember = str(RememberMe.get())
                stringDoKeepLogin = str(KeepMeLoggedIn.get())
                with open('doNotDelete.txt', 'wb') as f:
                    f.truncate(0)
                    fileContent = base64.b64encode(f"{Username.get()},{Password.get()},{stringDoRemember},{stringDoKeepLogin}".encode('utf-8'))
                    f.write(fileContent)
            else:
                with open('doNotDelete.txt', 'wb') as f:
                    f.truncate(0)
            if UserPlan == 999:
                AdminPanel()
                break
            if EndingDateInSecondos >= currentDateInSeconds:
                send(userDatabase)
                send(DISCONNECT_MESSAGE)
                subprocess.Popen('python msQuoterWithSub.py')
                AuthenticationWindow.destroy()
                return
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

#canvas = Canvas(AuthenticationWindow, highlightthickness=0, width=250, height=100)
#canvas.place(x=170, y=140)

def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs):
        
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return canvas.create_polygon(points, **kwargs, smooth=True)

#my_rectangle = round_rectangle(7, 8, 240, 37, radius=20, fill="white")
#my_rectangle = round_rectangle(7, 44, 240, 74, radius=20, fill="white")

Label(AuthenticationWindow, text="Username", font=("Arial", 15), fg="black") .place(x=10, y=149)
Username = Entry(AuthenticationWindow, width=20, font=("Arial", 15), bg="white", borderwidth=1)
Username.place(x=180, y=150)
Username.focus()
Username.bind("<Return>", bindedTechLogin)

Label(AuthenticationWindow, text="Password", font=("Arial", 15), fg="black") .place(x=10, y=184)
Password = Entry(AuthenticationWindow, width=20, font=("Arial", 15), bg="white", show="*", borderwidth=1)
Password.place(x=180, y=185)
Password.bind("<Return>", bindedTechLogin)

RememberMe = IntVar()
Label(AuthenticationWindow, text="Remember me", font=("Arial", 13), fg="black") .place(x=35, y=215)
RememberMeChecked = Checkbutton(AuthenticationWindow, variable=RememberMe)
RememberMeChecked.place(x=10, y=216)

KeepMeLoggedIn = IntVar()
Label(AuthenticationWindow, text="Keep me logged in", font=("Arial", 13), fg="black") .place(x=35, y=238)
KeepMeLoggedInChecked = Checkbutton(AuthenticationWindow, variable=KeepMeLoggedIn)
KeepMeLoggedInChecked.place(x=10, y=238)

try:
    with open('doNotDelete.txt', 'rb') as f:
        fileContent = f.read()
        decodeFile = base64.b64decode(fileContent).decode('utf-8')
        contextSplit = decodeFile.split(",")
        Username.insert(0, contextSplit[0])
        Password.insert(0, contextSplit[1])
        if int(contextSplit[2]) == 1:
            RememberMeChecked.select()
        if int(contextSplit[3]) == 1:
            KeepMeLoggedInChecked.select()
except:
    pass

forgotpassword = Label(AuthenticationWindow, text="Forgot your password?", font=("Arial", 13), fg="blue", cursor="hand2")
forgotpassword.place(x=179, y=215)
f = tkFont.Font(forgotpassword, forgotpassword.cget("font"))
f.configure(underline = True)
forgotpassword.configure(font=f)
forgotpassword.bind("<Button-1>", lambda e: forgotPassword())

arrowSize = (20,30)
LoginArrow = Image.open("rightarrowEnter.png")
showLoginArrow = ImageTk.PhotoImage(LoginArrow.resize(arrowSize, Image.ANTIALIAS))
#showLoginArrow = ImageTk.PhotoImage(LoginArrow)
LoginArrowLabel = Label(AuthenticationWindow, image=showLoginArrow, cursor="hand2") 
LoginArrowLabel.place(x=430, y=163)
LoginArrowLabel.bind("<Button-1>", lambda e: JtTechLogin())

def stayConnectedToMySQL():
    cursor = JtTechDb.cursor(buffered=True)
    cursor.execute('SELECT id from Users LIMIT 1')
    send("KEEP ALIVE")
    print("foi")
    LoginArrowLabel.after(300000, stayConnectedToMySQL)


if RememberMe.get() == 1 and KeepMeLoggedIn.get() == 1:
    print("vish")
    #JtTechLogin()
else:
    stayConnectedToMySQL()
AuthenticationWindow.mainloop()
