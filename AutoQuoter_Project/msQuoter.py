from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sqlite3
import io
import os
import time
import pandas
import shutil
from datetime import date, timedelta
from tkcalendar import *
import datetime
import customtkinter

#main
MainWindow = Tk()
MainWindow.title("Morning Star")
MainWindow.configure(background="black")
MainWindow.iconbitmap('favicon-16x16.ico')
MainWindow.geometry("1500x950")
MainWindow.resizable(False,False)

topWindowsToCloseOnLogout = []

#Top Menu
TopMenuButtons = Frame(MainWindow, bg="#516CC2")
TopMenuButtons.place_forget()

#LOGIN
LoginScreen = Frame(MainWindow, bg="black")
LoginScreen.place(relwidth=0.4, relheight=0.8, x=450,y=50)

LoginFrame = Frame(LoginScreen, bg="#516CC2")
LoginFrame.place(relwidth=0.7, relheight=0.5, x=85,y=400)

imageSize = (400,300)
SignInLogo = Image.open("MSBIG.png")
showSignInLogo = ImageTk.PhotoImage(SignInLogo.resize(imageSize, Image.ANTIALIAS))
Label(LoginScreen, image=showSignInLogo, bg="black") .place(x=100, y=0)

Label(LoginScreen, text="Username", font=("Arial", 15), background="#516CC2", fg="white") .place(x=185, y=430)
Username = Entry(LoginScreen, width=20, font=("Arial", 15), bg="white")
Username.place(x=185, y=460)
Username.focus()

Label(LoginScreen, text="Password", font=("Arial", 15), background="#516CC2", fg="white") .place(x=185, y=530)
Password = Entry(LoginScreen, width=20, font=("Arial", 15), bg="white", show="*")
Password.place(x=185, y=560)

#Logged In
LoggedInWindow = Frame(MainWindow, bg="black")
LoggedInWindow.place_forget()

GetDaysAndHoursWorked = Frame(LoggedInWindow, bg="black")
GetDaysAndHoursWorked.place(relwidth=0.2, relheight=0.25, x=1200, y=40)

ClockWindow = Frame(LoggedInWindow, bg="black")
ClockWindow.place_forget()

connect = sqlite3.connect('MsClients.db')
cursor = connect.cursor()
#logo
Logo = PhotoImage(file="morning-star-logo.png")
Label(LoggedInWindow, image=Logo, bg="white") .place(x=340, y=50)

#clock
ClockLabel = Label(LoggedInWindow, text="", font=("Helvetica", 15), fg="white", bg="black")
ClockLabel.place(x=1270,y=0)

#days
Label(GetDaysAndHoursWorked, text="Monday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=0)
MondayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
MondayTimer.place(x=110, y=0)
Label(GetDaysAndHoursWorked, text="Tuesday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=30)
TuesdayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
TuesdayTimer.place(x=110, y=30)
Label(GetDaysAndHoursWorked, text="Wednesday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=60)
WednesdayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
WednesdayTimer.place(x=130, y=60)
Label(GetDaysAndHoursWorked, text="Thursday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=90)
ThursdayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
ThursdayTimer.place(x=110, y=90)
Label(GetDaysAndHoursWorked, text="Friday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=120)
FridayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
FridayTimer.place(x=110, y=120)

Label(GetDaysAndHoursWorked, text="Salary Earned:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=200)
salaryEarned = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
salaryEarned.place(x=140, y=200)

currentDate = time.strftime("%Y-%m-%d")

workedTimeInSeconds = 0

counting = False

timeDifferenceWhenLoggedIn = 0

#clients saved
clientListFrame = Frame(LoggedInWindow)
clientListFrame.place(relwidth=0.157, relheight=0.34, x=950,y=40)
clientListScrollBar = Scrollbar(clientListFrame, orient=VERTICAL)
Label(LoggedInWindow, text="Client List", font=("Helvetica", 15), fg="white", bg="black").place(x=1020, y=10)
clientList = Listbox(LoggedInWindow, yscrollcommand=clientListScrollBar.set)
clientList.place(relwidth=0.147, relheight=0.34, x=950,y=40)
clientListScrollBar.config(command=clientList.yview)
clientListScrollBar.pack(side=RIGHT, fill=Y)

documentListFrame = Frame(LoggedInWindow)
documentListFrame.place(relwidth=0.157, relheight=0.3, x=950,y=500)
documentListScrollBar = Scrollbar(documentListFrame, orient=VERTICAL)
Label(LoggedInWindow, text="Documents List", font=("Helvetica", 15), fg="white", bg="black").place(x=990, y=470)
documentList = Listbox(LoggedInWindow, yscrollcommand=documentListScrollBar.set)
documentList.place(relwidth=0.147, relheight=0.3, x=950,y=500)
documentListScrollBar.config(command=documentList.yview)
documentListScrollBar.pack(side=RIGHT, fill=Y)



cursor.execute('''CREATE TABLE IF NOT EXISTS Employees(
                    id integer PRIMARY KEY, Username TEXT, Password TEXT, FirstName TEXT, MiddleName TEXT, LastName TEXT, Access integer,
                    email TEXT, phone TEXT, address TEXT, apt TEXT, city TEXT, state TEXT, zip TEXT,
                    SSN TEXT, salary, photo BLOB NOT NULL,
                    clockedIn integer NOT NULL DEFAULT 0,
                    mondayDay TEXT,
                    mondayTimer	TEXT,
                    mondayTimeWorked integer NOT NULL DEFAULT 0,
                    tuesdayDay TEXT,
                    tuesdayTimer TEXT,
                    tuesdayTimeWorked integer NOT NULL DEFAULT 0,
                    wednesdayDay TEXT,
                    wednesdayTimer TEXT,
                    wednesdayTimeWorked	integer NOT NULL DEFAULT 0,
                    thursdayDay TEXT,
                    thursdayTimer TEXT,
                    thursdayTimeWorked integer NOT NULL DEFAULT 0,
                    fridayDay TEXT,
                    fridayTimer	TEXT,
                    fridayTimeWorked INTEGER DEFAULT 0,
                    timeOnClose	TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Clients(
                    id integer PRIMARY KEY, name TEXT, married integer,
                    email TEXT, phone TEXT, address TEXT, apt TEXT, city TEXT, state TEXT, zip TEXT,
                    homeOwned integer, sameAsMailing integer,
                    mailingAddress TEXT, mailingApt TEXT, mailingCity TEXT, mailingState TEXT, mailingZip TEXT, 
                    driver1 TEXT, driver1License TEXT, driver1State TEXT, driver1Dob TEXT, driver1Married integer,
                    driver2 TEXT, driver2License TEXT, driver2State TEXT, driver2Dob TEXT, driver2Married integer, 
                    driver3 TEXT, driver3License TEXT, driver3State TEXT, driver3Dob TEXT, driver3Married integer,
                    driver4 TEXT, driver4License TEXT, driver4State TEXT, driver4Dob TEXT, driver4Married integer,
                    driver5 TEXT, driver5License TEXT, driver5State TEXT, driver5Dob TEXT, driver5Married integer,
                    priorInsurance integer, priorInsuranceCarrier TEXT, priorInsurancePolicyNumber TEXT, priorInsuranceYearsWithPolicy TEXT, priorInsuranceExpDate TEXT,
                    BiLimit integer, PdLimit integer, PipDeductible integer, PdForYourVehicle integer, PdDeductibleForYourVehicle integer,
                    vehicle1 TEXT, vehicle1Make TEXT, vehicle1Model TEXT, vehicle1VIN TEXT, vehicle1Financed integer, vehicle1Leased integer,
                    vehicle2 TEXT, vehicle2Make TEXT, vehicle2Model TEXT, vehicle2VIN TEXT, vehicle2Financed integer, vehicle2Leased integer,
                    vehicle3 TEXT, vehicle3Make TEXT, vehicle3Model TEXT, vehicle3VIN TEXT, vehicle3Financed integer, vehicle3Leased integer,
                    vehicle4 TEXT, vehicle4Make TEXT, vehicle4Model TEXT, vehicle4VIN TEXT, vehicle4Financed integer, vehicle4Leased integer,
                    vehicle5 TEXT, vehicle5Make TEXT, vehicle5Model TEXT, vehicle5VIN TEXT, vehicle5Financed integer, vehicle5Leased integer,
                    accident1Date TEXT, accident1Type TEXT, accident1Driver TEXT, accident1PIP TEXT, accident1PointsOnLicense TEXT, 
                    accident2Date TEXT, accident2Type TEXT, accident2Driver TEXT, accident2PIP TEXT, accident2PointsOnLicense TEXT, 
                    accident3Date TEXT, accident3Type TEXT, accident3Driver TEXT, accident3PIP TEXT, accident3PointsOnLicense TEXT, 
                    licensePhoto BLOB NOT NULL)''')
    
cursor.execute('''CREATE TABLE IF NOT EXISTS EmployeeHours(
                    id integer PRIMARY KEY,
                    EmployeeID integer,
                    Date TEXT,
                    TimeWorked INTEGER DEFAULT 0,
                    ClockedIn1 TEXT,
                    ClockedOut1 TEXT,
                    ClockedIn2 TEXT,
                    ClockedOut2 TEXT,
                    ClockedIn3 TEXT,
                    ClockedOut3 TEXT,
                    ClockedIn4 TEXT,
                    ClockedOut4 TEXT,
                    ClockedIn5 TEXT,
                    ClockedOut5 TEXT,
                    ClockedIn6 TEXT,
                    ClockedOut6,
                    ClockedIn7 TEXT,
                    ClockedOut7	TEXT,
                    ClockedIn8 TEXT,
                    ClockedOut8 TEXT,
                    ClockedIn9 TEXT,
                    ClockedOut9 TEXT,
                    ClockedIn10 TEXT,
                    ClockedOut10 TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Documents(
                    id integer PRIMARY KEY,
                    ClientID integer,
                    DocumentName TEXT,
                    document BLOB NOT NULL,
                    documentDir TEXT)''')


cursor.execute('SELECT * from Clients')
clients = cursor.fetchall()

imageSize = (100,100)
licenseImage = Image.open("imageicon.png")
showLicense = ImageTk.PhotoImage(licenseImage.resize(imageSize, Image.ANTIALIAS))
licenseLabel = Label(LoggedInWindow, image=showLicense)
licenseLabel.place(x=40, y=50)
photoLabel = Label(LoggedInWindow, text='', bg=("black"), fg="white")
photoLabel.place(x=40, y=29)

currentTab = Label(text='Login', bg=("black"), fg="white")
currentTab.place(x=0,y=200)

UserIDfound = Label(text='', bg=("black"), fg="white")
UserIDfound.place(x=200,y=200)

clientIDfound = Label(text='', bg=("black"), fg="white")
clientIDfound.place(x=300,y=200)

#functions
def AutoQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    AutoQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Auto Quote")

def HomeQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    HomeQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Home Quote")

def LifeQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    LifeQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Life Quote")
    
def HealthQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    HealthQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Health Quote")

def GeneralLiabilityQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    GeneralLiabilityQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="General Liability Quote")
    
def WorkersCompQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    WorkersCompQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Workers Comp Quote")

def MotorcycleQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    MotorcycleQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Motorcycle Quote")

def BoatQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    BoatQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Boat Quote")

def FloodQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    FloodQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Flood Quote")

def UmbrellaQuoteTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    UmbrellaQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Umbrella Quote")

def AdminPanelTab():
    getTab = currentTab.cget("text")
    if getTab == "Auto Quote":
        AutoQuote.place_forget()
    elif getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    AdminPanel.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Admin Panel")

def get_photo():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=((".png","*.png"), ("all files", "*.*")))
    photoLabel.config(text=filename, fg='white')
    return filename

def convertToBinary(filename):
    with open(filename, 'rb') as file:
        photo = file.read()
    return photo

def uploadDocument():
    clientID = clientIDfound.cget("text")
    file = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=((".png","*.png"),(".jpg","*.jpg"),(".pdf","*.pdf"), ("all files", "*.*")))
    filename = os.path.basename(file)
    fileBinary = convertToBinary(file)
    splitFile = os.path.splitext(filename)
    getFileName = splitFile[0]
    fileExtension = splitFile[1]
    if fileExtension == ".pdf":
        shutil.copy(file, "documents/")
    docDir = f"documents/{filename}"
    cursor.execute('''INSERT INTO Documents (ClientID, DocumentName, document, documentDir) VALUES (?, ?, ?, ?)''', [clientID, getFileName, fileBinary, docDir])
    connect.commit()
    cursor.execute('SELECT DocumentName from Documents WHERE clientID=?', [clientID])
    documentsFetched = [ x[0] for x in cursor.fetchall()]
    documentsData = []
    for document in documentsFetched:
        documentsData.append(document)
    DocumentsSorted = sorted(documentsData)
    UpdateDocuments(DocumentsSorted)

def deleteDocument():
    clientID = clientIDfound.cget("text")
    loadedDocument = documentList.get(documentList.curselection())
    cursor.execute('SELECT documentDir from Documents WHERE DocumentName=? AND clientID=?', [loadedDocument, clientID])
    documentFetched = [ x[0] for x in cursor.fetchall()]
    fileDir = documentFetched[0]
    os.remove(fileDir)
    cursor.execute('DELETE from Documents WHERE DocumentName=? AND clientID=?', [loadedDocument, clientID])
    connect.commit()
    cursor.execute('SELECT DocumentName from Documents WHERE clientID=?', [clientID])
    documentsFetched = [ x[0] for x in cursor.fetchall()]
    documentsData = []
    for document in documentsFetched:
        documentsData.append(document)
    DocumentsSorted = sorted(documentsData)
    UpdateDocuments(DocumentsSorted)

def openLicenseImage():
    licenseImage.show()
   
def openDocument(self):
    clientID = clientIDfound.cget("text")
    loadedDocument = documentList.get(documentList.curselection())
    cursor.execute('SELECT document from Documents WHERE DocumentName=? AND clientID=?', [loadedDocument, clientID])
    documentFetched = [ x[0] for x in cursor.fetchall()]
    #
    #    os.startfile(file)
    #os.startfile(document)
    try:
        document = Image.open(io.BytesIO(documentFetched[0]))
        document.show()
    except:
        try:
            cursor.execute('SELECT documentDir from Documents WHERE DocumentName=? AND clientID=?', [loadedDocument, clientID])
            documentFetched = [ x[0] for x in cursor.fetchall()]
            fileDir = documentFetched[0]
            currentDir = os.path.abspath(os.getcwd())
            os.startfile(os.path.join(currentDir,fileDir))
        except:
            messagebox.showerror("Error", "Error.")

def quote():
    #os.system('python seleniumProj.py')
    # get chromedriver
    chrome_Options = Options()
    chrome_Options.add_argument("--headless")
    PATH = r"chromedriver.exe"
    CHROME_PATH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
    chrome_Options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(executable_path=PATH, options=chrome_Options)
    # USER DATA
    accountName = NameInsured.get()
    accountPassword = emailEntry.get()
    # setup website
    website = "https://bestserverglobal.com"
    driver.get(website)
    # print title
    print("Connected to ", driver.title)

    fecharButton = driver.find_element_by_name("fechar")
    if fecharButton:
        fecharButton.send_keys(Keys.RETURN)

    print("closed double tc ad")

    playNow = driver.find_element_by_name("Play Now")
    if playNow:
        playNow.send_keys(Keys.RETURN)
    print("went to login screen")

    insertAccountName = driver.find_element_by_name("account_login")
    insertAccountPassword = driver.find_element_by_name("password_login")
    if insertAccountName:
        #print(accountName)
        #print(accountPassword)
        insertAccountName.send_keys(accountName)
        insertAccountPassword.send_keys(accountPassword)
        insertAccountPassword.send_keys(Keys.RETURN)
    print("input credentials")
    driver.get_screenshot_as_file("capture.png")
    driver.close()

def Load(self):
    #connect = sqlite3.connect('MsClients.db')
    cursor.execute('SELECT * from Clients')
    clients = cursor.fetchall()
    try:
        loadedClient = clientList.get(clientList.curselection())
    except:
        messagebox.showerror("Error", "You must select a client from the list.")
        return
    
    for client in clients:
        if client[1] == loadedClient:
            clientIDfound.config(text=client[0])
            NameInsured.delete(0,END)
            NameInsured.insert(0, client[1])

            if client[2] == 1:
                MarriedChecked.select()
            else:
                MarriedChecked.deselect()

            emailEntry.delete(0,END)
            emailEntry.insert(0,client[3])
            phoneEntry.delete(0,END)
            phoneEntry.insert(0,client[4])
            addressEntry.delete(0,END)
            addressEntry.insert(0,client[5])
            AptEntry.delete(0,END)
            AptEntry.insert(0,client[6])
            cityEntry.delete(0,END)
            cityEntry.insert(0,client[7])
            stateEntry.delete(0,END)
            stateEntry.insert(0,client[8])
            zipEntry.delete(0,END)
            zipEntry.insert(0,client[9])

            if client[10] == 1:
                OwnedChecked.select()
            else:
                OwnedChecked.deselect()
                
            if client[11] == 1:
                SameAsMailingChecked.select()
            else:
                SameAsMailingChecked.deselect()

            mailingAddressEntry.delete(0,END)
            mailingAddressEntry.insert(0,client[12])
            mailingAptEntry.delete(0,END)
            mailingAptEntry.insert(0,client[13])
            mailingcityEntry.delete(0,END)
            mailingcityEntry.insert(0,client[14])
            mailingstateEntry.delete(0,END)
            mailingstateEntry.insert(0,client[15])
            mailingzipEntry.delete(0,END)
            mailingzipEntry.insert(0,client[16])
            
            driver1Entry.delete(0,END)
            driver1Entry.insert(0,client[17])
            driver1LicenseEntry.delete(0,END)
            driver1LicenseEntry.insert(0,client[18])
            driver1StateEntry.delete(0,END)
            driver1StateEntry.insert(0,client[19])
            driver1DobEntry.delete(0,END)
            driver1DobEntry.insert(0,client[20])

            if client[21] == 1:
                driver1MarriedChecked.select()
            else:
                driver1MarriedChecked.deselect()
            
            driver2Entry.delete(0,END)
            driver2Entry.insert(0,client[22])
            driver2LicenseEntry.delete(0,END)
            driver2LicenseEntry.insert(0,client[23])
            driver2StateEntry.delete(0,END)
            driver2StateEntry.insert(0,client[24])
            driver2DobEntry.delete(0,END)
            driver2DobEntry.insert(0,client[25])

            if client[26] == 1:
                driver2MarriedChecked.select()
            else:
                driver2MarriedChecked.deselect()

            driver3Entry.delete(0,END)
            driver3Entry.insert(0,client[27])
            driver3LicenseEntry.delete(0,END)
            driver3LicenseEntry.insert(0,client[28])
            driver3StateEntry.delete(0,END)
            driver3StateEntry.insert(0,client[29])
            driver3DobEntry.delete(0,END)
            driver3DobEntry.insert(0,client[30])

            if client[31] == 1:
                driver3MarriedChecked.select()
            else:
                driver3MarriedChecked.deselect()
            
            driver4Entry.delete(0,END)
            driver4Entry.insert(0,client[32])
            driver4LicenseEntry.delete(0,END)
            driver4LicenseEntry.insert(0,client[33])
            driver4StateEntry.delete(0,END)
            driver4StateEntry.insert(0,client[34])
            driver4DobEntry.delete(0,END)
            driver4DobEntry.insert(0,client[35])

            if client[36] == 1:
                driver4MarriedChecked.select()
            else:
                driver4MarriedChecked.deselect()
            
            driver5Entry.delete(0,END)
            driver5Entry.insert(0,client[37])
            driver5LicenseEntry.delete(0,END)
            driver5LicenseEntry.insert(0,client[38])
            driver5StateEntry.delete(0,END)
            driver5StateEntry.insert(0,client[39])
            driver5DobEntry.delete(0,END)
            driver5DobEntry.insert(0,client[40])

            if client[41] == 1:
                driver5MarriedChecked.select()
            else:
                driver5MarriedChecked.deselect()

            if client[42] == 1:
                priorInsuranceCheck.select()
            else:
                priorInsuranceCheck.deselect()

            carrierEntry.delete(0,END)
            carrierEntry.insert(0,client[43])
            policyNumberEntry.delete(0,END)
            policyNumberEntry.insert(0,client[44])
            yearsWithPolicyEntry.delete(0,END)
            yearsWithPolicyEntry.insert(0,client[45])
            expDatePolicyEntry.delete(0,END)
            expDatePolicyEntry.insert(0,client[46])

            if client[47] == 0:
                BiLimit.set(0)
            elif client[47] == 1:
                BiLimit.set(1)
            elif client[47] == 2:
                BiLimit.set(2)
            elif client[47] == 3:
                BiLimit.set(3)
            else:
                BiLimit.set(0)
                
            if client[48] == 0:
                PdLimit.set(0)
            elif client[48] == 1:
                PdLimit.set(1)
            elif client[48] == 2:
                PdLimit.set(2)
            elif client[48] == 3:
                PdLimit.set(3)
            elif client[48] == 4:
                PdLimit.set(4)
            else:
                PdLimit.set(0)

            if client[49] == 1:
                PipDeductibleChecked.select()
            else:
                PipDeductibleChecked.deselect()
                
            if client[50] == 1:
                PdForYourVehicleChecked.select()
            else:
                PdForYourVehicleChecked.deselect()

            if client[51] == 1:
                PdDeductibleForYourVehicle.set(1)
            elif client[51] == 2:
                PdDeductibleForYourVehicle.set(2)
            else:
                PdDeductibleForYourVehicle.set(0)
            
            vehicle1Entry.delete(0,END)
            vehicle1Entry.insert(0,client[52])
            vehicle1MakeEntry.delete(0,END)
            vehicle1MakeEntry.insert(0,client[53])
            vehicle1ModelEntry.delete(0,END)
            vehicle1ModelEntry.insert(0,client[54])
            vehicle1VINEntry.delete(0,END)
            vehicle1VINEntry.insert(0,client[55])            
            
            if client[56] == 1:
                vehicle1FinancedChecked.select()
            else:
                vehicle1FinancedChecked.deselect()
                
            if client[57] == 1:
                vehicle1LeasedChecked.select()
            else:
                vehicle1LeasedChecked.deselect()
            
            vehicle2Entry.delete(0,END)
            vehicle2Entry.insert(0,client[58])
            vehicle2MakeEntry.delete(0,END)
            vehicle2MakeEntry.insert(0,client[59])
            vehicle2ModelEntry.delete(0,END)
            vehicle2ModelEntry.insert(0,client[60])
            vehicle2VINEntry.delete(0,END)
            vehicle2VINEntry.insert(0,client[61])            
            
            if client[62] == 1:
                vehicle2FinancedChecked.select()
            else:
                vehicle2FinancedChecked.deselect()
                
            if client[63] == 1:
                vehicle2LeasedChecked.select()
            else:
                vehicle2LeasedChecked.deselect()
            
            vehicle3Entry.delete(0,END)
            vehicle3Entry.insert(0,client[64])
            vehicle3MakeEntry.delete(0,END)
            vehicle3MakeEntry.insert(0,client[65])
            vehicle3ModelEntry.delete(0,END)
            vehicle3ModelEntry.insert(0,client[66])
            vehicle3VINEntry.delete(0,END)
            vehicle3VINEntry.insert(0,client[67])            
            
            if client[68] == 1:
                vehicle3FinancedChecked.select()
            else:
                vehicle3FinancedChecked.deselect()
                
            if client[69] == 1:
                vehicle3LeasedChecked.select()
            else:
                vehicle3LeasedChecked.deselect()
            
            vehicle4Entry.delete(0,END)
            vehicle4Entry.insert(0,client[70])
            vehicle4MakeEntry.delete(0,END)
            vehicle4MakeEntry.insert(0,client[71])
            vehicle4ModelEntry.delete(0,END)
            vehicle4ModelEntry.insert(0,client[72])
            vehicle4VINEntry.delete(0,END)
            vehicle4VINEntry.insert(0,client[73])            
            
            if client[74] == 1:
                vehicle4FinancedChecked.select()
            else:
                vehicle4FinancedChecked.deselect()
                
            if client[75] == 1:
                vehicle4LeasedChecked.select()
            else:
                vehicle4LeasedChecked.deselect()
            
            vehicle5Entry.delete(0,END)
            vehicle5Entry.insert(0,client[76])
            vehicle5MakeEntry.delete(0,END)
            vehicle5MakeEntry.insert(0,client[77])
            vehicle5ModelEntry.delete(0,END)
            vehicle5ModelEntry.insert(0,client[78])
            vehicle5VINEntry.delete(0,END)
            vehicle5VINEntry.insert(0,client[79])            
            
            if client[80] == 1:
                vehicle5FinancedChecked.select()
            else:
                vehicle5FinancedChecked.deselect()
                
            if client[81] == 1:
                vehicle5LeasedChecked.select()
            else:
                vehicle5LeasedChecked.deselect()

            accident1Entry.delete(0,END)
            accident1Entry.insert(0,client[82])
            accident1TypeEntry.delete(0,END)
            accident1TypeEntry.insert(0,client[83])
            accident1DriverEntry.delete(0,END)
            accident1DriverEntry.insert(0,client[84])
            accident1PIPEntry.delete(0,END)
            accident1PIPEntry.insert(0,client[85])  
            accident1PointsOnLicenseEntry.delete(0,END)
            accident1PointsOnLicenseEntry.insert(0,client[86])

            accident2Entry.delete(0,END)
            accident2Entry.insert(0,client[87])
            accident2TypeEntry.delete(0,END)
            accident2TypeEntry.insert(0,client[88])
            accident2DriverEntry.delete(0,END)
            accident2DriverEntry.insert(0,client[89])
            accident2PIPEntry.delete(0,END)
            accident2PIPEntry.insert(0,client[90])  
            accident2PointsOnLicenseEntry.delete(0,END)
            accident2PointsOnLicenseEntry.insert(0,client[91])  
            
            accident3Entry.delete(0,END)
            accident3Entry.insert(0,client[92])
            accident3TypeEntry.delete(0,END)
            accident3TypeEntry.insert(0,client[93])
            accident3DriverEntry.delete(0,END)
            accident3DriverEntry.insert(0,client[94])
            accident3PIPEntry.delete(0,END)
            accident3PIPEntry.insert(0,client[95])  
            accident3PointsOnLicenseEntry.delete(0,END)
            accident3PointsOnLicenseEntry.insert(0,client[96])
            global licenseImage
            try:
                getClientLicensePhoto = Image.open(f'images/{client[0]}{client[1]}.png')
                #getClientLicensePhoto.show()
                showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
                licenseLabel.config(image=showClientLicensePhoto)
                licenseLabel.image = showClientLicensePhoto
                photoLabel.config(text=f'images/{client[0]}{client[1]}.png', fg='black')
                
                licenseImage = getClientLicensePhoto
                #print("carregou")
            except:
                getClientLicensePhoto = Image.open("imageicon.png")
                #getClientLicensePhoto.show()
                showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
                licenseLabel.config(image=showClientLicensePhoto)
                licenseLabel.image = showClientLicensePhoto
                photoLabel.config(text='')
                licenseImage = getClientLicensePhoto
                #print("nao carregou")
            try:
                cursor.execute('SELECT DocumentName from Documents WHERE clientID=?', [client[0]])
                documentsFetched = [ x[0] for x in cursor.fetchall()]
                documentsData = []
                for document in documentsFetched:
                    documentsData.append(document)
                DocumentsSorted = sorted(documentsData)
                UpdateDocuments(DocumentsSorted)
                #print(documentsFetched)
               # print(documentName)
            except:
                pass


    #print("Loaded")

def Update(data):  
    cursor.execute('SELECT * from Clients')
    clients = cursor.fetchall()
    clientList.delete(0, END)

    for client in data:
        clientList.insert(END, client)

def Search(search):
    searched = clientSearchEntry.get()

    cursor.execute('SELECT * from Clients')
    clients = cursor.fetchall()
    if searched == '':
        data = []
        for client in clients:
            data.append(client[1])
    else:
        data = []
        for client in clients:
            clientes = client[1]
            if searched.lower() in clientes.lower():
                data.append(clientes)

    Update(sorted(data))

def UpdateEmployees(data):  
    cursor.execute('SELECT * from Employees')
    cursor.fetchall()
    employeeList.delete(0, END)

    for employee in data:
        employeeList.insert(END, employee)

def UpdateDocuments(data):  
    cursor.execute('SELECT * from Documents')
    cursor.fetchall()
    documentList.delete(0, END)

    for document in data:
        documentList.insert(END, document)

def SearchEmployees(search):
    searched = employeeSearchEntry.get()

    cursor.execute('SELECT * from Employees')
    employees = cursor.fetchall()
    if searched == '':
        data = []
        for employee in employees:
            data.append(employee[1])
    else:
        data = []
        for employee in employees:
            employeesName = employee[1]
            if searched.lower() in employeesName.lower():
                data.append(employeesName)

    UpdateEmployees(sorted(data))

def SearchDocument(search):
    searched = documentSearchEntry.get()

    cursor.execute('SELECT DocumentName from Documents')
    documents = cursor.fetchall()
    if searched == '':
        data = []
        for document in documents:
            data.append(document[0])
    else:
        data = []
        for document in documents:
            documentName = document[0]
            if searched.lower() in documentName.lower():
                data.append(documentName)

    UpdateDocuments(sorted(data))

def Save():
    #connect = sqlite3.connect('MsClients.db')
    clientName = NameInsured.get()
    ClientMarried = Married.get()
    ClientHomeOwned = Owned.get()
    ClientEmail = emailEntry.get()
    ClientPhone = phoneEntry.get()
    ClientAddress = addressEntry.get()
    ClientAddressApt = AptEntry.get()
    ClientAddressCity = cityEntry.get()
    ClientAddressState = stateEntry.get()
    ClientAddressZipCode = zipEntry.get()
    ClientSameAsMailing = SameAsMailing.get()

    if ClientSameAsMailing == 1:
        ClientMailingAddress = addressEntry.get()
        ClientMailingAddressApt = AptEntry.get()
        ClientMailingAddressCity = cityEntry.get()
        ClientMailingAddressState = stateEntry.get()
        ClientMailingAddressZipCode = zipEntry.get()
    else:
        ClientMailingAddress = mailingAddressEntry.get()
        ClientMailingAddressApt = mailingAptEntry.get()
        ClientMailingAddressCity = mailingcityEntry.get()
        ClientMailingAddressState = mailingstateEntry.get()
        ClientMailingAddressZipCode = mailingzipEntry.get()

    ClientDriver1 = driver1Entry.get()
    ClientDriver1License = driver1LicenseEntry.get()
    ClientDriver1State = driver1StateEntry.get()
    ClientDriver1Dob = driver1DobEntry.get()
    ClientDriver1Married = driver1Married.get()

    ClientDriver2 = driver2Entry.get()
    ClientDriver2License = driver2LicenseEntry.get()
    ClientDriver2State = driver2StateEntry.get()
    ClientDriver2Dob = driver2DobEntry.get()
    ClientDriver2Married = driver2Married.get()

    ClientDriver3 = driver3Entry.get()
    ClientDriver3License = driver3LicenseEntry.get()
    ClientDriver3State = driver3StateEntry.get()
    ClientDriver3Dob = driver3DobEntry.get()
    ClientDriver3Married = driver3Married.get()
    
    ClientDriver4 = driver4Entry.get()
    ClientDriver4License = driver4LicenseEntry.get()
    ClientDriver4State = driver4StateEntry.get()
    ClientDriver4Dob = driver4DobEntry.get()
    ClientDriver4Married = driver4Married.get()
    
    ClientDriver5 = driver5Entry.get()
    ClientDriver5License = driver5LicenseEntry.get()
    ClientDriver5State = driver5StateEntry.get()
    ClientDriver5Dob = driver5DobEntry.get()
    ClientDriver5Married = driver5Married.get()

    ClientPriorInsurance = priorInsurance.get()
    ClientPriorInsuranceCarrier = carrierEntry.get()
    ClientPriorInsurancePolicyNumber = policyNumberEntry.get()    
    ClientPriorInsuranceYearsWithPolicy = yearsWithPolicyEntry.get()
    ClientPriorInsuranceExpDate = expDatePolicyEntry.get()

    ClientBiLimit = BiLimit.get()
    ClientPdLimit = PdLimit.get()
    ClientPipDeductible = PipDeductible.get()
    ClientPdForYourVehicle = PdForYourVehicle.get()
    ClientPdDeductibleForYourVehicle = PdDeductibleForYourVehicle.get()

    ClientVehicle1 = vehicle1Entry.get()
    ClientVehicle1MakeEntry = vehicle1MakeEntry.get()
    ClientVehicle1ModelEntry = vehicle1ModelEntry.get()
    ClientVehicle1VINEntry = vehicle1VINEntry.get()
    ClientVehicle1Financed = vehicle1Financed.get()
    ClientVehicle1Leased = vehicle1Leased.get()
    
    ClientVehicle2 = vehicle2Entry.get()
    ClientVehicle2MakeEntry = vehicle2MakeEntry.get()
    ClientVehicle2ModelEntry = vehicle2ModelEntry.get()
    ClientVehicle2VINEntry = vehicle2VINEntry.get()
    ClientVehicle2Financed = vehicle2Financed.get()
    ClientVehicle2Leased = vehicle2Leased.get()
    
    ClientVehicle3 = vehicle3Entry.get()
    ClientVehicle3MakeEntry = vehicle3MakeEntry.get()
    ClientVehicle3ModelEntry = vehicle3ModelEntry.get()
    ClientVehicle3VINEntry = vehicle3VINEntry.get()
    ClientVehicle3Financed = vehicle3Financed.get()
    ClientVehicle3Leased = vehicle3Leased.get()
    
    ClientVehicle4 = vehicle4Entry.get()
    ClientVehicle4MakeEntry = vehicle4MakeEntry.get()
    ClientVehicle4ModelEntry = vehicle4ModelEntry.get()
    ClientVehicle4VINEntry = vehicle4VINEntry.get()
    ClientVehicle4Financed = vehicle4Financed.get()
    ClientVehicle4Leased = vehicle4Leased.get()
    
    ClientVehicle5 = vehicle5Entry.get()
    ClientVehicle5MakeEntry = vehicle5MakeEntry.get()
    ClientVehicle5ModelEntry = vehicle5ModelEntry.get()
    ClientVehicle5VINEntry = vehicle5VINEntry.get()
    ClientVehicle5Financed = vehicle5Financed.get()
    ClientVehicle5Leased = vehicle5Leased.get()

    ClientAccident1Date = accident1Entry.get()
    ClientAccident1Type = accident1TypeEntry.get()
    ClientAccident1Driver = accident1DriverEntry.get()
    ClientAccident1PIP = accident1PIPEntry.get()
    ClientAccident1PointsOnLicense = accident1PointsOnLicenseEntry.get()
    
    ClientAccident2Date = accident2Entry.get()
    ClientAccident2Type = accident2TypeEntry.get()
    ClientAccident2Driver = accident2DriverEntry.get()
    ClientAccident2PIP = accident2PIPEntry.get()
    ClientAccident2PointsOnLicense = accident2PointsOnLicenseEntry.get()
    
    ClientAccident3Date = accident3Entry.get()
    ClientAccident3Type = accident3TypeEntry.get()
    ClientAccident3Driver = accident3DriverEntry.get()
    ClientAccident3PIP = accident3PIPEntry.get()
    ClientAccident3PointsOnLicense = accident3PointsOnLicenseEntry.get()

    try:
        
        LicensePhoto = convertToBinary(photoLabel.cget("text"))
    except:
        LicensePhoto = convertToBinary('imageicon.png')
    
    cursor.execute('''INSERT INTO Clients (name, married, email, phone, address, apt, city, state, zip, homeOwned, sameAsMailing,
                        mailingAddress, mailingApt, mailingCity, mailingState, mailingZip, 
                        driver1, driver1License, driver1State, driver1Dob, driver1Married,
                        driver2, driver2License, driver2State, driver2Dob, driver2Married, 
                        driver3, driver3License, driver3State, driver3Dob, driver3Married,
                        driver4, driver4License, driver4State, driver4Dob, driver4Married,
                        driver5, driver5License, driver5State, driver5Dob, driver5Married,
                        priorInsurance, priorInsuranceCarrier, priorInsurancePolicyNumber, priorInsuranceYearsWithPolicy, priorInsuranceExpDate,
                        BiLimit, PdLimit, PipDeductible, PdForYourVehicle, PdDeductibleForYourVehicle,
                        vehicle1, vehicle1Make, vehicle1Model, vehicle1VIN, vehicle1Financed, vehicle1Leased,
                        vehicle2, vehicle2Make, vehicle2Model, vehicle2VIN, vehicle2Financed, vehicle2Leased,
                        vehicle3, vehicle3Make, vehicle3Model, vehicle3VIN, vehicle3Financed, vehicle3Leased,
                        vehicle4, vehicle4Make, vehicle4Model, vehicle4VIN, vehicle4Financed, vehicle4Leased,
                        vehicle5, vehicle5Make, vehicle5Model, vehicle5VIN, vehicle5Financed, vehicle5Leased,
                        accident1Date, accident1Type, accident1Driver, accident1PIP, accident1PointsOnLicense, 
                        accident2Date, accident2Type, accident2Driver, accident2PIP, accident2PointsOnLicense, 
                        accident3Date, accident3Type, accident3Driver, accident3PIP, accident3PointsOnLicense, 
                        licensePhoto) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                ?, ?, ?, ?, ?, ?, ?)''', 
                        [clientName, ClientMarried, ClientEmail, ClientPhone,
                            ClientAddress, ClientAddressApt, ClientAddressCity, ClientAddressState, ClientAddressZipCode, ClientHomeOwned,
                            ClientSameAsMailing, ClientMailingAddress, ClientMailingAddressApt, ClientMailingAddressCity, ClientMailingAddressState, ClientMailingAddressZipCode,
                            ClientDriver1, ClientDriver1License, ClientDriver1State, ClientDriver1Dob, ClientDriver1Married,
                            ClientDriver2, ClientDriver2License, ClientDriver2State, ClientDriver2Dob, ClientDriver2Married,
                            ClientDriver3, ClientDriver3License, ClientDriver3State, ClientDriver3Dob, ClientDriver3Married,
                            ClientDriver4, ClientDriver4License, ClientDriver4State, ClientDriver4Dob, ClientDriver4Married,
                            ClientDriver5, ClientDriver5License, ClientDriver5State, ClientDriver5Dob, ClientDriver5Married,
                            ClientPriorInsurance, ClientPriorInsuranceCarrier, ClientPriorInsurancePolicyNumber, ClientPriorInsuranceYearsWithPolicy, ClientPriorInsuranceExpDate,
                            ClientBiLimit, ClientPdLimit, ClientPipDeductible, ClientPdForYourVehicle, ClientPdDeductibleForYourVehicle,
                            ClientVehicle1, ClientVehicle1MakeEntry, ClientVehicle1ModelEntry, ClientVehicle1VINEntry, ClientVehicle1Financed, ClientVehicle1Leased,
                            ClientVehicle2, ClientVehicle2MakeEntry, ClientVehicle2ModelEntry, ClientVehicle2VINEntry, ClientVehicle2Financed, ClientVehicle2Leased,
                            ClientVehicle3, ClientVehicle3MakeEntry, ClientVehicle3ModelEntry, ClientVehicle3VINEntry, ClientVehicle3Financed, ClientVehicle3Leased,
                            ClientVehicle4, ClientVehicle4MakeEntry, ClientVehicle4ModelEntry, ClientVehicle4VINEntry, ClientVehicle4Financed, ClientVehicle4Leased,
                            ClientVehicle5, ClientVehicle5MakeEntry, ClientVehicle5ModelEntry, ClientVehicle5VINEntry, ClientVehicle5Financed, ClientVehicle5Leased,
                            ClientAccident1Date, ClientAccident1Type, ClientAccident1Driver, ClientAccident1PIP, ClientAccident1PointsOnLicense,
                            ClientAccident2Date, ClientAccident2Type, ClientAccident2Driver, ClientAccident2PIP, ClientAccident2PointsOnLicense,
                            ClientAccident3Date, ClientAccident3Type, ClientAccident3Driver, ClientAccident3PIP, ClientAccident3PointsOnLicense,
                        LicensePhoto])
    clientList.insert(END, clientName)
    connect.commit()
    cursor.execute('SELECT * from Clients')
    clientsUpdated = cursor.fetchall()
    data = []
    for client in clientsUpdated:
        data.append(client[1])
        nomeDoCliente = client[1]
        if clientName.lower() == nomeDoCliente.lower():
            licenseImage = Image.open(io.BytesIO(client[97]))
            licenseImage.save(f'images/{client[0]}{client[1]}.png')
            getClientLicensePhoto = Image.open(f'images/{client[0]}{client[1]}.png')
            showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
            licenseLabel.config(image=showClientLicensePhoto)
            licenseLabel.image = showClientLicensePhoto
            photoLabel.config(text='')

    clientes = sorted(data)
    Update(clientes)

    messagebox.showinfo("Saved!", f"Client {clientName} was saved!")

def UpdateClient():
    ClientID = clientIDfound.cget("text")
    clientName = NameInsured.get()
    ClientMarried = Married.get()
    ClientHomeOwned = Owned.get()
    ClientEmail = emailEntry.get()
    ClientPhone = phoneEntry.get()
    ClientAddress = addressEntry.get()
    ClientAddressApt = AptEntry.get()
    ClientAddressCity = cityEntry.get()
    ClientAddressState = stateEntry.get()
    ClientAddressZipCode = zipEntry.get()
    ClientSameAsMailing = SameAsMailing.get()

    if ClientSameAsMailing == 1:
        ClientMailingAddress = addressEntry.get()
        ClientMailingAddressApt = AptEntry.get()
        ClientMailingAddressCity = cityEntry.get()
        ClientMailingAddressState = stateEntry.get()
        ClientMailingAddressZipCode = zipEntry.get()
    else:
        ClientMailingAddress = mailingAddressEntry.get()
        ClientMailingAddressApt = mailingAptEntry.get()
        ClientMailingAddressCity = mailingcityEntry.get()
        ClientMailingAddressState = mailingstateEntry.get()
        ClientMailingAddressZipCode = mailingzipEntry.get()

    ClientDriver1 = driver1Entry.get()
    ClientDriver1License = driver1LicenseEntry.get()
    ClientDriver1State = driver1StateEntry.get()
    ClientDriver1Dob = driver1DobEntry.get()
    ClientDriver1Married = driver1Married.get()

    ClientDriver2 = driver2Entry.get()
    ClientDriver2License = driver2LicenseEntry.get()
    ClientDriver2State = driver2StateEntry.get()
    ClientDriver2Dob = driver2DobEntry.get()
    ClientDriver2Married = driver2Married.get()

    ClientDriver3 = driver3Entry.get()
    ClientDriver3License = driver3LicenseEntry.get()
    ClientDriver3State = driver3StateEntry.get()
    ClientDriver3Dob = driver3DobEntry.get()
    ClientDriver3Married = driver3Married.get()
    
    ClientDriver4 = driver4Entry.get()
    ClientDriver4License = driver4LicenseEntry.get()
    ClientDriver4State = driver4StateEntry.get()
    ClientDriver4Dob = driver4DobEntry.get()
    ClientDriver4Married = driver4Married.get()
    
    ClientDriver5 = driver5Entry.get()
    ClientDriver5License = driver5LicenseEntry.get()
    ClientDriver5State = driver5StateEntry.get()
    ClientDriver5Dob = driver5DobEntry.get()
    ClientDriver5Married = driver5Married.get()

    ClientPriorInsurance = priorInsurance.get()
    ClientPriorInsuranceCarrier = carrierEntry.get()
    ClientPriorInsurancePolicyNumber = policyNumberEntry.get()    
    ClientPriorInsuranceYearsWithPolicy = yearsWithPolicyEntry.get()
    ClientPriorInsuranceExpDate = expDatePolicyEntry.get()

    ClientBiLimit = BiLimit.get()
    ClientPdLimit = PdLimit.get()
    ClientPipDeductible = PipDeductible.get()
    ClientPdForYourVehicle = PdForYourVehicle.get()
    ClientPdDeductibleForYourVehicle = PdDeductibleForYourVehicle.get()

    ClientVehicle1 = vehicle1Entry.get()
    ClientVehicle1MakeEntry = vehicle1MakeEntry.get()
    ClientVehicle1ModelEntry = vehicle1ModelEntry.get()
    ClientVehicle1VINEntry = vehicle1VINEntry.get()
    ClientVehicle1Financed = vehicle1Financed.get()
    ClientVehicle1Leased = vehicle1Leased.get()
    
    ClientVehicle2 = vehicle2Entry.get()
    ClientVehicle2MakeEntry = vehicle2MakeEntry.get()
    ClientVehicle2ModelEntry = vehicle2ModelEntry.get()
    ClientVehicle2VINEntry = vehicle2VINEntry.get()
    ClientVehicle2Financed = vehicle2Financed.get()
    ClientVehicle2Leased = vehicle2Leased.get()
    
    ClientVehicle3 = vehicle3Entry.get()
    ClientVehicle3MakeEntry = vehicle3MakeEntry.get()
    ClientVehicle3ModelEntry = vehicle3ModelEntry.get()
    ClientVehicle3VINEntry = vehicle3VINEntry.get()
    ClientVehicle3Financed = vehicle3Financed.get()
    ClientVehicle3Leased = vehicle3Leased.get()
    
    ClientVehicle4 = vehicle4Entry.get()
    ClientVehicle4MakeEntry = vehicle4MakeEntry.get()
    ClientVehicle4ModelEntry = vehicle4ModelEntry.get()
    ClientVehicle4VINEntry = vehicle4VINEntry.get()
    ClientVehicle4Financed = vehicle4Financed.get()
    ClientVehicle4Leased = vehicle4Leased.get()
    
    ClientVehicle5 = vehicle5Entry.get()
    ClientVehicle5MakeEntry = vehicle5MakeEntry.get()
    ClientVehicle5ModelEntry = vehicle5ModelEntry.get()
    ClientVehicle5VINEntry = vehicle5VINEntry.get()
    ClientVehicle5Financed = vehicle5Financed.get()
    ClientVehicle5Leased = vehicle5Leased.get()

    ClientAccident1Date = accident1Entry.get()
    ClientAccident1Type = accident1TypeEntry.get()
    ClientAccident1Driver = accident1DriverEntry.get()
    ClientAccident1PIP = accident1PIPEntry.get()
    ClientAccident1PointsOnLicense = accident1PointsOnLicenseEntry.get()
    
    ClientAccident2Date = accident2Entry.get()
    ClientAccident2Type = accident2TypeEntry.get()
    ClientAccident2Driver = accident2DriverEntry.get()
    ClientAccident2PIP = accident2PIPEntry.get()
    ClientAccident2PointsOnLicense = accident2PointsOnLicenseEntry.get()
    
    ClientAccident3Date = accident3Entry.get()
    ClientAccident3Type = accident3TypeEntry.get()
    ClientAccident3Driver = accident3DriverEntry.get()
    ClientAccident3PIP = accident3PIPEntry.get()
    ClientAccident3PointsOnLicense = accident3PointsOnLicenseEntry.get()

    try:
        LicensePhoto = convertToBinary(photoLabel.cget("text"))
    except:
        LicensePhoto = convertToBinary('imageicon.png')

    cursor.execute('''UPDATE Clients SET name=?, married=?, email=?, phone=?, address=?, apt=?, city=?, state=?, zip=?, homeOwned=?, sameAsMailing=?,
                        mailingAddress=?, mailingApt=?, mailingCity=?, mailingState=?, mailingZip=?, 
                        driver1=?, driver1License=?, driver1State=?, driver1Dob=?, driver1Married=?,
                        driver2=?, driver2License=?, driver2State=?, driver2Dob=?, driver2Married=?, 
                        driver3=?, driver3License=?, driver3State=?, driver3Dob=?, driver3Married=?,
                        driver4=?, driver4License=?, driver4State=?, driver4Dob=?, driver4Married=?,
                        driver5=?, driver5License=?, driver5State=?, driver5Dob=?, driver5Married=?,
                        priorInsurance=?, priorInsuranceCarrier=?, priorInsurancePolicyNumber=?, priorInsuranceYearsWithPolicy=?, priorInsuranceExpDate=?,
                        BiLimit=?, PdLimit=?, PipDeductible=?, PdForYourVehicle=?, PdDeductibleForYourVehicle=?,
                        vehicle1=?, vehicle1Make=?, vehicle1Model=?, vehicle1VIN=?, vehicle1Financed=?, vehicle1Leased=?,
                        vehicle2=?, vehicle2Make=?, vehicle2Model=?, vehicle2VIN=?, vehicle2Financed=?, vehicle2Leased=?,
                        vehicle3=?, vehicle3Make=?, vehicle3Model=?, vehicle3VIN=?, vehicle3Financed=?, vehicle3Leased=?,
                        vehicle4=?, vehicle4Make=?, vehicle4Model=?, vehicle4VIN=?, vehicle4Financed=?, vehicle4Leased=?,
                        vehicle5=?, vehicle5Make=?, vehicle5Model=?, vehicle5VIN=?, vehicle5Financed=?, vehicle5Leased=?,
                        accident1Date=?, accident1Type=?, accident1Driver=?, accident1PIP=?, accident1PointsOnLicense=?, 
                        accident2Date=?, accident2Type=?, accident2Driver=?, accident2PIP=?, accident2PointsOnLicense=?, 
                        accident3Date=?, accident3Type=?, accident3Driver=?, accident3PIP=?, accident3PointsOnLicense=?,
                        licensePhoto=? WHERE id=?''', 
                            (clientName, ClientMarried, ClientEmail, ClientPhone,
                            ClientAddress, ClientAddressApt, ClientAddressCity, ClientAddressState, ClientAddressZipCode, ClientHomeOwned,
                            ClientSameAsMailing, ClientMailingAddress, ClientMailingAddressApt, ClientMailingAddressCity, ClientMailingAddressState, ClientMailingAddressZipCode,
                            ClientDriver1, ClientDriver1License, ClientDriver1State, ClientDriver1Dob, ClientDriver1Married,
                            ClientDriver2, ClientDriver2License, ClientDriver2State, ClientDriver2Dob, ClientDriver2Married,
                            ClientDriver3, ClientDriver3License, ClientDriver3State, ClientDriver3Dob, ClientDriver3Married,
                            ClientDriver4, ClientDriver4License, ClientDriver4State, ClientDriver4Dob, ClientDriver4Married,
                            ClientDriver5, ClientDriver5License, ClientDriver5State, ClientDriver5Dob, ClientDriver5Married,
                            ClientPriorInsurance, ClientPriorInsuranceCarrier, ClientPriorInsurancePolicyNumber, ClientPriorInsuranceYearsWithPolicy, ClientPriorInsuranceExpDate,
                            ClientBiLimit, ClientPdLimit, ClientPipDeductible, ClientPdForYourVehicle, ClientPdDeductibleForYourVehicle,
                            ClientVehicle1, ClientVehicle1MakeEntry, ClientVehicle1ModelEntry, ClientVehicle1VINEntry, ClientVehicle1Financed, ClientVehicle1Leased,
                            ClientVehicle2, ClientVehicle2MakeEntry, ClientVehicle2ModelEntry, ClientVehicle2VINEntry, ClientVehicle2Financed, ClientVehicle2Leased,
                            ClientVehicle3, ClientVehicle3MakeEntry, ClientVehicle3ModelEntry, ClientVehicle3VINEntry, ClientVehicle3Financed, ClientVehicle3Leased,
                            ClientVehicle4, ClientVehicle4MakeEntry, ClientVehicle4ModelEntry, ClientVehicle4VINEntry, ClientVehicle4Financed, ClientVehicle4Leased,
                            ClientVehicle5, ClientVehicle5MakeEntry, ClientVehicle5ModelEntry, ClientVehicle5VINEntry, ClientVehicle5Financed, ClientVehicle5Leased,
                            ClientAccident1Date, ClientAccident1Type, ClientAccident1Driver, ClientAccident1PIP, ClientAccident1PointsOnLicense,
                            ClientAccident2Date, ClientAccident2Type, ClientAccident2Driver, ClientAccident2PIP, ClientAccident2PointsOnLicense,
                            ClientAccident3Date, ClientAccident3Type, ClientAccident3Driver, ClientAccident3PIP, ClientAccident3PointsOnLicense,
                            LicensePhoto, ClientID))
    connect.commit()
    cursor.execute('SELECT * from Clients')
    clientsUpdated = cursor.fetchall()
    data = []
    for client in clientsUpdated:
        data.append(client[1])
        nomeDoCliente = client[1]
        if clientName.lower() == nomeDoCliente.lower():
            licenseImage = Image.open(io.BytesIO(client[97]))
            licenseImage.save(f'images/{client[0]}{client[1]}.png')
            getClientLicensePhoto = Image.open(f'images/{client[0]}{client[1]}.png')
            showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
            licenseLabel.config(image=showClientLicensePhoto)
            licenseLabel.image = showClientLicensePhoto
            photoLabel.config(text='')
            
    clientes = sorted(data)
    Update(clientes)
    messagebox.showinfo("Updated!", f"Client {clientName} was updated!")

def Timer():

    global counting
    global timeDifferenceWhenLoggedIn
    global workedTimeInSeconds

    day = time.strftime("%A")
    userId = UserIDfound.cget("text")
    today = date.today()
    
    if day == "Monday":
        cursor.execute('SELECT mondayDay from Employees WHERE id=?',[userId])
        fetchedUserMondayDay = [ x[0] for x in cursor.fetchall()]
        MondayDay = fetchedUserMondayDay[0]
        cursor.execute('SELECT mondayTimeWorked from Employees WHERE id=?',[userId])
        fetchedUserMondayTimeWorked = [ x[0] for x in cursor.fetchall()]
        MondayTimeWorkedDb = fetchedUserMondayTimeWorked[0]
        workedTimeInSeconds = MondayTimeWorkedDb + timeDifferenceWhenLoggedIn
        newTime = timedelta(seconds=workedTimeInSeconds)
        #print(timedelta(seconds=workedTimeInSeconds))
        if MondayDay == currentDate:
            workedTimeInSeconds += 1
            calculateSalary()
            MondayTimer.config(text=newTime)
            dbTime = MondayTimer.cget("text")
            timeXOut = int(time.time())
            cursor.execute('UPDATE Employees SET mondayTimer=? WHERE id=?',(dbTime, userId))
            cursor.execute('UPDATE Employees SET timeOnClose=? WHERE id=?',(timeXOut, userId))
            cursor.execute('UPDATE Employees SET mondayTimeWorked=? WHERE id=?',(workedTimeInSeconds, userId))
            cursor.execute('UPDATE EmployeeHours SET TimeWorked=? WHERE EmployeeID=? AND Date=?',(workedTimeInSeconds, userId, currentDate))
        else:
            cursor.execute('UPDATE Employees SET mondayDay=? WHERE id=?',(currentDate, userId))
            cursor.execute('UPDATE Employees SET mondayTimer=? WHERE id=?',("0:00:00", userId))
            cursor.execute('UPDATE Employees SET mondayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET tuesdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET wednesdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET thursdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET fridayTimeWorked=? WHERE id=?',(0, userId))
            MondayTimer.config(text=newTime)
        TuesdayTimer.config(text="0:00:00")
        WednesdayTimer.config(text="0:00:00")
        ThursdayTimer.config(text="0:00:00")
        FridayTimer.config(text="0:00:00")
    elif day == "Tuesday":
        getMondayDate = today - timedelta(days = 1)
        cursor.execute('SELECT mondayDay from Employees WHERE id=?',[userId])
        fetchedUserMondayDay = [ x[0] for x in cursor.fetchall()]
        MondayDate = fetchedUserMondayDay[0]
        if str(getMondayDate) == MondayDate:
            cursor.execute('SELECT mondayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserMondayTimeWorked = [ x[0] for x in cursor.fetchall()]
            MondayTimeWorkedDb = timedelta(seconds=fetchedUserMondayTimeWorked[0])
            MondayTimer.config(text=MondayTimeWorkedDb)
        else:
            MondayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET mondayTimeWorked=? WHERE id=?',(0, userId))
        #
        cursor.execute('SELECT tuesdayDay from Employees WHERE id=?',[userId])
        fetchedUserTuesdayDay = [ x[0] for x in cursor.fetchall()]
        TuesdayDay = fetchedUserTuesdayDay[0]
        cursor.execute('SELECT tuesdayTimeWorked from Employees WHERE id=?',[userId])
        fetchedUserTuesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
        TuesdayTimeWorkedDb = fetchedUserTuesdayTimeWorked[0]
        workedTimeInSeconds = TuesdayTimeWorkedDb + timeDifferenceWhenLoggedIn
        newTime = timedelta(seconds=workedTimeInSeconds)
        #print(timedelta(seconds=workedTimeInSeconds))
        if TuesdayDay == currentDate:
            workedTimeInSeconds += 1
            calculateSalary()
            TuesdayTimer.config(text=newTime)
            dbTime = TuesdayTimer.cget("text")
            timeXOut = int(time.time())
            cursor.execute('UPDATE Employees SET tuesdayTimer=? WHERE id=?',(dbTime, userId))
            cursor.execute('UPDATE Employees SET timeOnClose=? WHERE id=?',(timeXOut, userId))
            cursor.execute('UPDATE Employees SET tuesdayTimeWorked=? WHERE id=?',(workedTimeInSeconds, userId))
            cursor.execute('UPDATE EmployeeHours SET TimeWorked=? WHERE EmployeeID=? AND Date=?',(workedTimeInSeconds, userId, currentDate))
        else:
            cursor.execute('UPDATE Employees SET tuesdayDay=? WHERE id=?',(currentDate, userId))
            cursor.execute('UPDATE Employees SET tuesdayTimer=? WHERE id=?',("0:00:00", userId))
            cursor.execute('UPDATE Employees SET tuesdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET wednesdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET thursdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET fridayTimeWorked=? WHERE id=?',(0, userId))
            TuesdayTimer.config(text=newTime)
        WednesdayTimer.config(text="0:00:00")
        ThursdayTimer.config(text="0:00:00")
        FridayTimer.config(text="0:00:00")
    elif day == "Wednesday":
        getMondayDate = today - timedelta(days = 2)
        cursor.execute('SELECT mondayDay from Employees WHERE id=?',[userId])
        fetchedUserMondayDay = [ x[0] for x in cursor.fetchall()]
        MondayDate = fetchedUserMondayDay[0]
        if str(getMondayDate) == MondayDate:
            cursor.execute('SELECT mondayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserMondayTimeWorked = [ x[0] for x in cursor.fetchall()]
            MondayTimeWorkedDb = timedelta(seconds=fetchedUserMondayTimeWorked[0])
            MondayTimer.config(text=MondayTimeWorkedDb)
        else:
            MondayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET mondayTimeWorked=? WHERE id=?',(0, userId))
        #
        getTuesdayDate = today - timedelta(days = 1)
        cursor.execute('SELECT tuesdayDay from Employees WHERE id=?',[userId])
        fetchedUserTuesdayDay = [ x[0] for x in cursor.fetchall()]
        TuesdayDay = fetchedUserTuesdayDay[0]
        if str(getTuesdayDate) == TuesdayDay:
            cursor.execute('SELECT tuesdayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserTuesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
            TuesdayTimeWorkedDb = timedelta(seconds=fetchedUserTuesdayTimeWorked[0])
            TuesdayTimer.config(text=TuesdayTimeWorkedDb)
        else:
            TuesdayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET tuesdayTimeWorked=? WHERE id=?',(0, userId))
        #
        cursor.execute('SELECT wednesdayDay from Employees WHERE id=?',[userId])
        fetchedUserWednesdayDay = [ x[0] for x in cursor.fetchall()]
        WednesdayDay = fetchedUserWednesdayDay[0]
        cursor.execute('SELECT wednesdayTimeWorked from Employees WHERE id=?',[userId])
        fetchedUserWednesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
        WednesdayTimeWorkedDb = fetchedUserWednesdayTimeWorked[0]
        workedTimeInSeconds = WednesdayTimeWorkedDb + timeDifferenceWhenLoggedIn
        newTime = timedelta(seconds=workedTimeInSeconds)
        #print(timedelta(seconds=workedTimeInSeconds))
        if WednesdayDay == currentDate:
            workedTimeInSeconds += 1
            calculateSalary()
            WednesdayTimer.config(text=newTime)
            dbTime = WednesdayTimer.cget("text")
            timeXOut = int(time.time())
            cursor.execute('UPDATE Employees SET wednesdayTimer=? WHERE id=?',(dbTime, userId))
            cursor.execute('UPDATE Employees SET timeOnClose=? WHERE id=?',(timeXOut, userId))
            cursor.execute('UPDATE Employees SET wednesdayTimeWorked=? WHERE id=?',(workedTimeInSeconds, userId))
            cursor.execute('UPDATE EmployeeHours SET TimeWorked=? WHERE EmployeeID=? AND Date=?',(workedTimeInSeconds, userId, currentDate))
        else:
            cursor.execute('UPDATE Employees SET wednesdayDay=? WHERE id=?',(currentDate, userId))
            cursor.execute('UPDATE Employees SET wednesdayTimer=? WHERE id=?',("0:00:00", userId))
            cursor.execute('UPDATE Employees SET wednesdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET thursdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET fridayTimeWorked=? WHERE id=?',(0, userId))
            WednesdayTimer.config(text=newTime)
        ThursdayTimer.config(text="0:00:00")
        FridayTimer.config(text="0:00:00")
    elif day == "Thursday":
        getMondayDate = today - timedelta(days = 3)
        cursor.execute('SELECT mondayDay from Employees WHERE id=?',[userId])
        fetchedUserMondayDay = [ x[0] for x in cursor.fetchall()]
        MondayDate = fetchedUserMondayDay[0]
        if str(getMondayDate) == MondayDate:
            cursor.execute('SELECT mondayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserMondayTimeWorked = [ x[0] for x in cursor.fetchall()]
            MondayTimeWorkedDb = timedelta(seconds=fetchedUserMondayTimeWorked[0])
            MondayTimer.config(text=MondayTimeWorkedDb)
        else:
            MondayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET mondayTimeWorked=? WHERE id=?',(0, userId))
        #
        getTuesdayDate = today - timedelta(days = 2)
        cursor.execute('SELECT tuesdayDay from Employees WHERE id=?',[userId])
        fetchedUserTuesdayDay = [ x[0] for x in cursor.fetchall()]
        TuesdayDay = fetchedUserTuesdayDay[0]
        if str(getTuesdayDate) == TuesdayDay:
            cursor.execute('SELECT tuesdayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserTuesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
            TuesdayTimeWorkedDb = timedelta(seconds=fetchedUserTuesdayTimeWorked[0])
            TuesdayTimer.config(text=TuesdayTimeWorkedDb)
        else:
            TuesdayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET tuesdayTimeWorked=? WHERE id=?',(0, userId))
        #
        getWednesdayDate = today - timedelta(days = 1)
        cursor.execute('SELECT wednesdayDay from Employees WHERE id=?',[userId])
        fetchedUserWednesdayDay = [ x[0] for x in cursor.fetchall()]
        WednesdayDay = fetchedUserWednesdayDay[0]
        if str(getWednesdayDate) == WednesdayDay:
            cursor.execute('SELECT wednesdayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserWednesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
            WednesdayTimeWorkedDb = timedelta(seconds=fetchedUserWednesdayTimeWorked[0])
            WednesdayTimer.config(text=WednesdayTimeWorkedDb)
        else:
            WednesdayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET wednesdayTimeWorked=? WHERE id=?',(0, userId))
        #
        cursor.execute('SELECT thursdayDay from Employees WHERE id=?',[userId])
        fetchedUserThursdayDay = [ x[0] for x in cursor.fetchall()]
        ThursdayDay = fetchedUserThursdayDay[0]
        cursor.execute('SELECT thursdayTimeWorked from Employees WHERE id=?',[userId])
        fetchedUserThursdayTimeWorked = [ x[0] for x in cursor.fetchall()]
        ThursdayTimeWorkedDb = fetchedUserThursdayTimeWorked[0]
        workedTimeInSeconds = ThursdayTimeWorkedDb + timeDifferenceWhenLoggedIn
        newTime = timedelta(seconds=workedTimeInSeconds)
        #print(timedelta(seconds=workedTimeInSeconds))
        if ThursdayDay == currentDate:
            workedTimeInSeconds += 1
            calculateSalary()
            ThursdayTimer.config(text=newTime)
            dbTime = ThursdayTimer.cget("text")
            timeXOut = int(time.time())
            cursor.execute('UPDATE Employees SET thursdayTimer=? WHERE id=?',(dbTime, userId))
            cursor.execute('UPDATE Employees SET timeOnClose=? WHERE id=?',(timeXOut, userId))
            cursor.execute('UPDATE Employees SET thursdayTimeWorked=? WHERE id=?',(workedTimeInSeconds, userId))
            cursor.execute('UPDATE EmployeeHours SET TimeWorked=? WHERE EmployeeID=? AND Date=?',(workedTimeInSeconds, userId, currentDate))
        else:
            cursor.execute('UPDATE Employees SET thursdayDay=? WHERE id=?',(currentDate, userId))
            cursor.execute('UPDATE Employees SET thursdayTimer=? WHERE id=?',("0:00:00", userId))
            cursor.execute('UPDATE Employees SET thursdayTimeWorked=? WHERE id=?',(0, userId))
            cursor.execute('UPDATE Employees SET fridayTimeWorked=? WHERE id=?',(0, userId))
            ThursdayTimer.config(text=newTime)
        FridayTimer.config(text="0:00:00")

    elif day == "Friday":
        getMondayDate = today - timedelta(days = 4)
        cursor.execute('SELECT mondayDay from Employees WHERE id=?',[userId])
        fetchedUserMondayDay = [ x[0] for x in cursor.fetchall()]
        MondayDate = fetchedUserMondayDay[0]
        if str(getMondayDate) == MondayDate:
            cursor.execute('SELECT mondayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserMondayTimeWorked = [ x[0] for x in cursor.fetchall()]
            MondayTimeWorkedDb = timedelta(seconds=fetchedUserMondayTimeWorked[0])
            MondayTimer.config(text=MondayTimeWorkedDb)
        else:
            MondayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET mondayTimeWorked=? WHERE id=?',(0, userId))
        #
        getTuesdayDate = today - timedelta(days = 3)
        cursor.execute('SELECT tuesdayDay from Employees WHERE id=?',[userId])
        fetchedUserTuesdayDay = [ x[0] for x in cursor.fetchall()]
        TuesdayDay = fetchedUserTuesdayDay[0]
        if str(getTuesdayDate) == TuesdayDay:
            cursor.execute('SELECT tuesdayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserTuesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
            TuesdayTimeWorkedDb = timedelta(seconds=fetchedUserTuesdayTimeWorked[0])
            TuesdayTimer.config(text=TuesdayTimeWorkedDb)
        else:
            TuesdayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET tuesdayTimeWorked=? WHERE id=?',(0, userId))
        #
        getWednesdayDate = today - timedelta(days = 2)
        cursor.execute('SELECT wednesdayDay from Employees WHERE id=?',[userId])
        fetchedUserWednesdayDay = [ x[0] for x in cursor.fetchall()]
        WednesdayDay = fetchedUserWednesdayDay[0]
        if str(getWednesdayDate) == WednesdayDay:
            cursor.execute('SELECT wednesdayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserWednesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
            WednesdayTimeWorkedDb = timedelta(seconds=fetchedUserWednesdayTimeWorked[0])
            WednesdayTimer.config(text=WednesdayTimeWorkedDb)
        else:
            WednesdayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET wednesdayTimeWorked=? WHERE id=?',(0, userId))
        #
        getThursdayDate = today - timedelta(days = 1)
        cursor.execute('SELECT thursdayDay from Employees WHERE id=?',[userId])
        fetchedUserThursdayDay = [ x[0] for x in cursor.fetchall()]
        ThursdayDay = fetchedUserThursdayDay[0]
        #print(getThursdayDate)
        ##print(ThursdayDay)
        if str(getThursdayDate) == ThursdayDay:
            cursor.execute('SELECT thursdayTimeWorked from Employees WHERE id=?',[userId])
            fetchedUserThursdayTimeWorked = [ x[0] for x in cursor.fetchall()]
            ThursdayTimeWorkedDb = timedelta(seconds=fetchedUserThursdayTimeWorked[0])
            ThursdayTimer.config(text=ThursdayTimeWorkedDb)
        else:
            ThursdayTimer.config(text="0:00:00")
            cursor.execute('UPDATE Employees SET thursdayTimeWorked=? WHERE id=?',(0, userId))
        #
        cursor.execute('SELECT fridayDay from Employees WHERE id=?',[userId])
        fetchedUserFridayDay = [ x[0] for x in cursor.fetchall()]
        FridayDay = fetchedUserFridayDay[0]
        cursor.execute('SELECT fridayTimeWorked from Employees WHERE id=?',[userId])
        fetchedUserFridayTimeWorked = [ x[0] for x in cursor.fetchall()]
        FridayTimeWorkedDb = fetchedUserFridayTimeWorked[0]
        workedTimeInSeconds = FridayTimeWorkedDb + timeDifferenceWhenLoggedIn
        newTime = timedelta(seconds=workedTimeInSeconds)
        #print(timedelta(seconds=workedTimeInSeconds))
        if FridayDay == currentDate:
            workedTimeInSeconds += 1
            calculateSalary()
            FridayTimer.config(text=newTime)
            dbTime = FridayTimer.cget("text")
            timeXOut = int(time.time())
            cursor.execute('UPDATE Employees SET fridayTimer=? WHERE id=?',(dbTime, userId))
            cursor.execute('UPDATE Employees SET timeOnClose=? WHERE id=?',(timeXOut, userId))
            cursor.execute('UPDATE Employees SET fridayTimeWorked=? WHERE id=?',(workedTimeInSeconds, userId))
            cursor.execute('UPDATE EmployeeHours SET TimeWorked=? WHERE EmployeeID=? AND Date=?',(workedTimeInSeconds, userId, currentDate))
        else:
            cursor.execute('UPDATE Employees SET fridayDay=? WHERE id=?',(currentDate, userId))
            cursor.execute('UPDATE Employees SET fridayTimer=? WHERE id=?',("0:00:00", userId))
            cursor.execute('UPDATE Employees SET fridayTimeWorked=? WHERE id=?',(0, userId))
            FridayTimer.config(text=newTime)
    
    timeDifferenceWhenLoggedIn = 0
    connect.commit()

def Clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    ClockLabel.config(text=f"{hour}:{minute}:{second}")
    ClockLabel.after(1000, Clock)

    global counting
    global currentDate
    #global CreateClient

    clientId = clientIDfound.cget("text")
    if clientId == "" and CreateClient["state"] == DISABLED:
        CreateClient["state"] = NORMAL
    elif clientId != "" and CreateClient["state"] == NORMAL:
        CreateClient["state"] = DISABLED
    
    if clientId == "" and UpdateClientInfo["state"] == NORMAL:
        UpdateClientInfo["state"] = DISABLED
    elif clientId != "" and UpdateClientInfo["state"] == DISABLED:
        UpdateClientInfo["state"] = NORMAL

    
    currentDate = time.strftime("%Y-%m-%d")
    
    if counting == True:
        Timer()

def ClockIn():
    ClockInButton.place_forget()
    global counting
    counting = True
    ClockedInTime = ClockLabel.cget("text")
    userId = UserIDfound.cget("text")
    cursor.execute('UPDATE Employees SET clockedIn=? WHERE id=?',(1, userId))

    #clickClockedIn = Label(ClockWindow, text="Clocked In: " + ClockedInTime, font=("Helvetica", 15), fg="white", bg="green")
    #clickClockedIn.pack()
    try:
        cursor.execute('SELECT ClockedIn1 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn1 = [ x[0] for x in cursor.fetchall()]
        fetchedTime1 = fetchedClockedIn1[0]

        cursor.execute('SELECT ClockedIn2 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn2 = [ x[0] for x in cursor.fetchall()]
        fetchedTime2 = fetchedClockedIn2[0]

        cursor.execute('SELECT ClockedIn3 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn3 = [ x[0] for x in cursor.fetchall()]
        fetchedTime3 = fetchedClockedIn3[0]

        cursor.execute('SELECT ClockedIn4 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn4 = [ x[0] for x in cursor.fetchall()]
        fetchedTime4 = fetchedClockedIn4[0]

        cursor.execute('SELECT ClockedIn5 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn5 = [ x[0] for x in cursor.fetchall()]
        fetchedTime5 = fetchedClockedIn5[0]

        cursor.execute('SELECT ClockedIn6 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn6 = [ x[0] for x in cursor.fetchall()]
        fetchedTime6 = fetchedClockedIn6[0]

        cursor.execute('SELECT ClockedIn7 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn7 = [ x[0] for x in cursor.fetchall()]
        fetchedTime7 = fetchedClockedIn7[0]

        cursor.execute('SELECT ClockedIn8 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn8 = [ x[0] for x in cursor.fetchall()]
        fetchedTime8 = fetchedClockedIn8[0]

        cursor.execute('SELECT ClockedIn9 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn9 = [ x[0] for x in cursor.fetchall()]
        fetchedTime9 = fetchedClockedIn9[0]

        cursor.execute('SELECT ClockedIn10 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedIn10 = [ x[0] for x in cursor.fetchall()]
        fetchedTime10 = fetchedClockedIn10[0]
        print("entrou no if")
        if fetchedTime1 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn1=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))                                    
        elif fetchedTime2 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn2=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        elif fetchedTime3 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn3=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        elif fetchedTime4 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn4=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        elif fetchedTime5 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn5=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        elif fetchedTime6 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn6=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        elif fetchedTime7 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn7=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        elif fetchedTime8 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn8=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        elif fetchedTime9 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn9=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
        else:
            cursor.execute('''UPDATE EmployeeHours SET ClockedIn10=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedInTime, currentDate, userId))
    except:
        cursor.execute('''INSERT INTO EmployeeHours (EmployeeID, Date, ClockedIn1) 
                        VALUES (?, ?, ?)''', 
                        [userId, currentDate, ClockedInTime])
        print("created new date")
    
    connect.commit()
    getHoursWorkedOnTheDay()
    print("updated")
    ClockOutButton.place(x=1200, y=3)

def ClockOut():
    global counting
    ClockedOutTime = ClockLabel.cget("text")
    #clickClockedOut = Label(ClockWindow, text="Clocked Out: " + ClockedOutTime, font=("Helvetica", 15), fg="white", bg="red")
    #clickClockedOut.pack()
    userId = UserIDfound.cget("text")
    cursor.execute('UPDATE Employees SET clockedIn=? WHERE id=?',(0, userId))
    cursor.execute('UPDATE Employees SET timeOnClose=? WHERE id=?',(0, userId))

    ClockInButton.place(x=1200, y=3)
    counting = False
    try:
        cursor.execute('SELECT ClockedOut1 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut1 = [ x[0] for x in cursor.fetchall()]
        fetchedTime1 = fetchedClockedOut1[0]
        
        cursor.execute('SELECT ClockedOut2 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut2 = [ x[0] for x in cursor.fetchall()]
        fetchedTime2 = fetchedClockedOut2[0]
        
        cursor.execute('SELECT ClockedOut3 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut3 = [ x[0] for x in cursor.fetchall()]
        fetchedTime3 = fetchedClockedOut3[0]
        
        cursor.execute('SELECT ClockedOut4 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut4 = [ x[0] for x in cursor.fetchall()]
        fetchedTime4 = fetchedClockedOut4[0]
        
        cursor.execute('SELECT ClockedOut5 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut5 = [ x[0] for x in cursor.fetchall()]
        fetchedTime5 = fetchedClockedOut5[0]
        
        cursor.execute('SELECT ClockedOut6 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut6 = [ x[0] for x in cursor.fetchall()]
        fetchedTime6 = fetchedClockedOut6[0]
        
        cursor.execute('SELECT ClockedOut7 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut7 = [ x[0] for x in cursor.fetchall()]
        fetchedTime7 = fetchedClockedOut7[0]
        
        cursor.execute('SELECT ClockedOut8 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut8 = [ x[0] for x in cursor.fetchall()]
        fetchedTime8 = fetchedClockedOut8[0]
        
        cursor.execute('SELECT ClockedOut9 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut9 = [ x[0] for x in cursor.fetchall()]
        fetchedTime9 = fetchedClockedOut9[0]
        
        cursor.execute('SELECT ClockedOut10 from EmployeeHours WHERE Date=? AND EmployeeID=?',[currentDate, userId])
        fetchedClockedOut10 = [ x[0] for x in cursor.fetchall()]
        fetchedTime10 = fetchedClockedOut10[0]

        print("entrou no if clockout")
        if fetchedTime1 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut1=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))                                    
        elif fetchedTime2 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut2=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        elif fetchedTime3 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut3=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        elif fetchedTime4 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut4=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        elif fetchedTime5 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut5=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        elif fetchedTime6 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut6=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        elif fetchedTime7 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut7=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        elif fetchedTime8 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut8=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        elif fetchedTime9 == None:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut9=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        else:
            cursor.execute('''UPDATE EmployeeHours SET ClockedOut10=? WHERE Date=? AND EmployeeID=?''', 
                                (ClockedOutTime, currentDate, userId))
        connect.commit()
    except:
        cursor.execute('''INSERT INTO EmployeeHours (EmployeeID, Date, ClockedOut1) 
                                    VALUES (?, ?, ?)''', 
                                    [userId, currentDate, ClockedOutTime])
        print("inserted exception clockout")
    connect.commit()
    getHoursWorkedOnTheDay()
    ClockOutButton.place_forget()

def Logout():
    LoggedInWindow.place_forget()
    LoginScreen.place(relwidth=0.4, relheight=0.8, x=450,y=50)
    TopMenuButtons.place_forget()
    getTab = currentTab.cget("text")
    if getTab == "Home Quote":
        HomeQuote.place_forget()
    elif getTab == "Life Quote":
        LifeQuote.place_forget()
    elif getTab == "Health Quote":
        HealthQuote.place_forget()
    elif getTab == "General Liability Quote":
        GeneralLiabilityQuote.place_forget()
    elif getTab == "Workers Comp Quote":
        WorkersCompQuote.place_forget()
    elif getTab == "Motorcycle Quote":
        MotorcycleQuote.place_forget()
    elif getTab == "Boat Quote":
        BoatQuote.place_forget()
    elif getTab == "Flood Quote":
        FloodQuote.place_forget()
    elif getTab == "Umbrella Quote":
        UmbrellaQuote.place_forget()
    elif getTab == "Admin Panel":
        AdminPanel.place_forget()
    AutoQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)
    currentTab.config(text="Login")
    UserIDfound.config(text="")
    global counting
    counting = False
    for widget in ClockWindow.winfo_children():
        widget.destroy()
    
    for widget in GetDaysAndHoursWorked.winfo_children():
        widget.destroy()
    for windows in topWindowsToCloseOnLogout:
        windows.destroy()
    employeeSearchEntry.delete(0, END)
    employeeSearchEntry.insert(0, "Search Employee...")
    employeeSearchEntry.config(fg="grey")
    Username.focus()
    clientSearchEntry.delete(0, END)
    clientSearchEntry.insert(0, "Search Client...")
    clientSearchEntry.config(fg="grey")
    documentSearchEntry.delete(0, END)
    documentSearchEntry.insert(0, "Search Document...")
    documentSearchEntry.config(fg="grey")
    NameInsured.delete(0,END)
    MarriedChecked.deselect()
    emailEntry.delete(0,END)
    phoneEntry.delete(0,END)
    addressEntry.delete(0,END)
    AptEntry.delete(0,END)
    cityEntry.delete(0,END)
    stateEntry.delete(0,END)
    zipEntry.delete(0,END)
    OwnedChecked.deselect()
    SameAsMailingChecked.deselect()
    mailingAddressEntry.delete(0,END)
    mailingAptEntry.delete(0,END)
    mailingcityEntry.delete(0,END)
    mailingstateEntry.delete(0,END)
    mailingzipEntry.delete(0,END)
    driver1Entry.delete(0,END)
    driver1LicenseEntry.delete(0,END)
    driver1StateEntry.delete(0,END)
    driver1DobEntry.delete(0,END)
    driver1MarriedChecked.deselect()
    driver2Entry.delete(0,END)
    driver2LicenseEntry.delete(0,END)
    driver2StateEntry.delete(0,END)
    driver2DobEntry.delete(0,END)
    driver2MarriedChecked.deselect()
    driver3Entry.delete(0,END)
    driver3LicenseEntry.delete(0,END)
    driver3StateEntry.delete(0,END)
    driver3DobEntry.delete(0,END)
    driver3MarriedChecked.deselect()
    driver4Entry.delete(0,END)
    driver4LicenseEntry.delete(0,END)
    driver4StateEntry.delete(0,END)
    driver4DobEntry.delete(0,END)
    driver4MarriedChecked.deselect()
    driver5Entry.delete(0,END)
    driver5LicenseEntry.delete(0,END)
    driver5StateEntry.delete(0,END)
    driver5DobEntry.delete(0,END)
    driver5MarriedChecked.deselect()
    priorInsuranceCheck.deselect()
    carrierEntry.delete(0,END)
    policyNumberEntry.delete(0,END)
    yearsWithPolicyEntry.delete(0,END)
    expDatePolicyEntry.delete(0,END)
    BiLimit.set(0)
    PdLimit.set(0)
    PipDeductibleChecked.deselect()
    PdForYourVehicleChecked.deselect()
    PdDeductibleForYourVehicle.set(0)
    vehicle1Entry.delete(0,END)
    vehicle1MakeEntry.delete(0,END)
    vehicle1ModelEntry.delete(0,END)
    vehicle1VINEntry.delete(0,END)         
    vehicle1FinancedChecked.deselect()
    vehicle1LeasedChecked.deselect()
    vehicle2Entry.delete(0,END)
    vehicle2MakeEntry.delete(0,END)
    vehicle2ModelEntry.delete(0,END)
    vehicle2VINEntry.delete(0,END)    
    vehicle2FinancedChecked.deselect()
    vehicle2LeasedChecked.deselect()
    vehicle3Entry.delete(0,END)
    vehicle3MakeEntry.delete(0,END)
    vehicle3ModelEntry.delete(0,END)
    vehicle3VINEntry.delete(0,END)         
    vehicle3FinancedChecked.deselect()
    vehicle3LeasedChecked.deselect()
    vehicle4Entry.delete(0,END)
    vehicle4MakeEntry.delete(0,END)
    vehicle4ModelEntry.delete(0,END)
    vehicle4VINEntry.delete(0,END)         
    vehicle4FinancedChecked.deselect()
    vehicle4LeasedChecked.deselect()
    vehicle5Entry.delete(0,END)
    vehicle5MakeEntry.delete(0,END)
    vehicle5ModelEntry.delete(0,END)
    vehicle5VINEntry.delete(0,END)         
    vehicle5FinancedChecked.deselect()
    vehicle5LeasedChecked.deselect()
    accident1Entry.delete(0,END)
    accident1TypeEntry.delete(0,END)
    accident1DriverEntry.delete(0,END)
    accident1PIPEntry.delete(0,END)
    accident1PointsOnLicenseEntry.delete(0,END)
    accident2Entry.delete(0,END)
    accident2TypeEntry.delete(0,END)
    accident2DriverEntry.delete(0,END)
    accident2PIPEntry.delete(0,END)
    accident2PointsOnLicenseEntry.delete(0,END)
    accident3Entry.delete(0,END)
    accident3TypeEntry.delete(0,END)
    accident3DriverEntry.delete(0,END)
    accident3PIPEntry.delete(0,END)
    accident3PointsOnLicenseEntry.delete(0,END)
    getClientLicensePhoto = Image.open("imageicon.png")
    showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
    licenseLabel.config(image=showClientLicensePhoto)
    licenseLabel.image = showClientLicensePhoto
    MainWindow.bind('<Return>', Login)

def Login(self):
    cursor.execute('SELECT * from Employees')
    AllUsers = cursor.fetchall()
    for Users in AllUsers:
        getUser = [ x for x in Users]
        getUserID = getUser[0]
        getUsername = getUser[1]
        getPassword = getUser[2]
        getAccess = getUser[6]
        clockedIn = getUser[17]
        if getUsername == Username.get() and getPassword == Password.get():
            LoggedInWindow.place(relwidth=1, relheight=1, x=0,y=40)
            ClockWindow.place(relwidth=0.135, relheight=0.61, x=1290,y=300)
            LoginScreen.place_forget()
            currentTab.config(text="Auto Quote")
            UserIDfound.config(text=getUserID)
            TopMenuButtons.place(relwidth=1, relheight=0.04, x=0,y=0)
            if getAccess == 999:
                AdminPanelButton.place(x=1350, y=5)
                for employee in employees:
                    data = []
                    for employee in employees:
                        data.append(employee[1])
                    employeesSorted = sorted(data)
                    UpdateEmployees(employeesSorted)
            else:
                AdminPanelButton.place_forget()

            if clockedIn == 1:
                ClockOutButton.place(x=1200, y=3)
                ClockInButton.place_forget()
                global counting
                global timeDifferenceWhenLoggedIn
                timeQuittedWhileLoggedIn = int(getUser[33])
                timeWhenLoggedIn = int(time.time())
                timeDifferenceWhenLoggedIn = timeWhenLoggedIn - timeQuittedWhileLoggedIn
                #print(timeDifferenceWhenLoggedIn)
                showDatesAndHoursWorked()
                counting = True
            else:
                showDatesAndHoursWorked()
                ClockOutButton.place_forget()
                ClockInButton.place(x=1200, y=3)

            getHoursWorkedOnTheDay()

            for client in clients:
                data = []
                for client in clients:
                    data.append(client[1])
                clientes = sorted(data)
                Update(clientes)
        
            #Label(LoginScreen, text="Wrong username or password", background="black", fg="black").place(x=230, y=379)
            #print("still binded")   
            MainWindow.unbind('<Return>', LoginBind)
            Clock()
            return
        else:
            Label(LoginScreen, text="Wrong username or password", background="black", fg="red") .place(x=230, y=379)

def CreateUserPopUp():
    createUserWindow = Toplevel(bg="#516CC2")
    createUserWindow.iconbitmap('favicon-16x16.ico')
    createUserWindow.title("Create User")
    createUserWindow.geometry("500x650")
    createUserWindow.resizable(False, False)
    topWindowsToCloseOnLogout.append(createUserWindow)

    def CreateUser():
        EmployeeUsername = NewEmployeeUsername.get()
        EmployeePassword = NewEmployeePassword.get()
        EmployeeFirstName = NewEmployeeFirstName.get()
        EmployeeMiddleName = NewEmployeeMiddleName.get()
        EmployeeLastName = NewEmployeeLastName.get()
        EmployeeAccess = NewEmployeeAccess.get()
        EmployeeEmail = NewEmployeeEmail.get()
        EmployeePhone = NewEmployeePhone.get()
        EmployeeAddress = NewEmployeeAddress.get()
        EmployeeApt = NewEmployeeApt.get()
        EmployeeCity = NewEmployeeCity.get()
        EmployeeState = NewEmployeeState.get()
        EmployeeZip = NewEmployeeZip.get()
        EmployeeSSN = NewEmployeeSSN.get()
        EmployeeSalary = NewEmployeeSalary.get()
        EmployeePhoto = NewEmployeeSSN.get()
        cursor.execute('''INSERT INTO Employees (Username, Password, FirstName, MiddleName, LastName, Access, email, phone, address,
                            apt, city, state, zip, SSN, salary, photo) 
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                                    ?, ?, ?, ?, ?)''', 
                            [EmployeeUsername, EmployeePassword, EmployeeFirstName, EmployeeMiddleName, EmployeeLastName, EmployeeAccess, EmployeeEmail,
                             EmployeePhone, EmployeeAddress, EmployeeApt, EmployeeCity, EmployeeState, EmployeeZip, EmployeeSSN, EmployeeSalary, EmployeePhoto])
        connect.commit()
        EmployeeUsername = NewEmployeeUsername.delete(0, END)
        EmployeePassword = NewEmployeePassword.delete(0, END)
        EmployeeFirstName = NewEmployeeFirstName.delete(0, END)
        EmployeeMiddleName = NewEmployeeMiddleName.delete(0, END)
        EmployeeLastName = NewEmployeeLastName.delete(0, END)
        EmployeeAccess = NewEmployeeAccess.delete(0, END)
        EmployeeEmail = NewEmployeeEmail.delete(0, END)
        EmployeePhone = NewEmployeePhone.delete(0, END)
        EmployeeAddress = NewEmployeeAddress.delete(0, END)
        EmployeeApt = NewEmployeeApt.delete(0, END)
        EmployeeCity = NewEmployeeCity.delete(0, END)
        EmployeeState = NewEmployeeState.delete(0, END)
        EmployeeZip = NewEmployeeZip.delete(0, END)
        EmployeeSSN = NewEmployeeSSN.delete(0, END)
        EmployeeSalary = NewEmployeeSalary.delete(0, END)
        messagebox.showinfo(createUserWindow, "Created!", f"User for {EmployeeFirstName} {EmployeeMiddleName} {EmployeeLastName} has been created!")

    Label(createUserWindow, text="Username", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=10)
    NewEmployeeUsername = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeeUsername.place(x=180, y=10)
    
    Label(createUserWindow, text="Password", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=50)
    NewEmployeePassword = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeePassword.place(x=180, y=50)
    
    Label(createUserWindow, text="First Name", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=90)
    NewEmployeeFirstName = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeeFirstName.place(x=180, y=90)
    
    Label(createUserWindow, text="Middle Name", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=130)
    NewEmployeeMiddleName = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeeMiddleName.place(x=180, y=130)
    
    Label(createUserWindow, text="Last Name", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=170)
    NewEmployeeLastName = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeeLastName.place(x=180, y=170)
    
    Label(createUserWindow, text="Access", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=210)
    NewEmployeeAccess = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeeAccess.place(x=180, y=210)
    
    Label(createUserWindow, text="Email", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=250)
    NewEmployeeEmail = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeeEmail.place(x=180, y=250)
    
    Label(createUserWindow, text="Phone", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=290)
    NewEmployeePhone = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeePhone.place(x=180, y=290)

    Label(createUserWindow, text="Address", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=330)
    NewEmployeeAddress = Entry(createUserWindow, font=("Arial", 15), width=20, bg="white")
    NewEmployeeAddress.place(x=180, y=330)
    
    Label(createUserWindow, text="Apt", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=370)
    NewEmployeeApt = Entry(createUserWindow, font=("Arial", 15), width=5, bg="white")
    NewEmployeeApt.place(x=180, y=370)

    Label(createUserWindow, text="City", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=410)
    NewEmployeeCity = Entry(createUserWindow, font=("Arial", 15), width=15, bg="white")
    NewEmployeeCity.place(x=180, y=410)
    
    Label(createUserWindow, text="State", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=450)
    NewEmployeeState = Entry(createUserWindow, font=("Arial", 15), width=5, bg="white")
    NewEmployeeState.place(x=180, y=450)
    
    Label(createUserWindow, text="ZIP", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=490)
    NewEmployeeZip = Entry(createUserWindow, font=("Arial", 15), width=15, bg="white")
    NewEmployeeZip.place(x=180, y=490)
    
    Label(createUserWindow, text="SSN", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=530)
    NewEmployeeSSN = Entry(createUserWindow, font=("Arial", 15), width=15, bg="white")
    NewEmployeeSSN.place(x=180, y=530)
    
    Label(createUserWindow, text="Salary", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=570)
    NewEmployeeSalary = Entry(createUserWindow, font=("Arial", 15), width=15, bg="white")
    NewEmployeeSalary.place(x=180, y=570)
    
    CreateUserButton = tk.Button(createUserWindow, text="Create", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=CreateUser)
    CreateUserButton.place(x=220, y=620)

def ManageUsersPopUp():
    manageUserWindow = Toplevel(bg="#516CC2")
    manageUserWindow.iconbitmap('favicon-16x16.ico')
    manageUserWindow.title("Manage User")
    manageUserWindow.geometry("800x650")
    manageUserWindow.resizable(False, False)
    topWindowsToCloseOnLogout.append(manageUserWindow)

    employeeListManagerFrame = Frame(manageUserWindow)
    employeeListManagerFrame.place(relwidth=0.2, relheight=0.3, x=610,y=90)
    employeeListManagerScrollBar = Scrollbar(employeeListManagerFrame, orient=VERTICAL)

    employeeListManager = Listbox(manageUserWindow, yscrollcommand=employeeListManagerScrollBar.set)
    employeeListManager.place(relwidth=0.18, relheight=0.3, x=610,y=90)
    employeeListManagerScrollBar.config(command=employeeListManager.yview)
    employeeListManagerScrollBar.pack(side=RIGHT, fill=Y)
    cursor.execute('SELECT id from Employees')
    cursor.fetchall()
    
    def UpdateEmployeesOnManager(data):  
        cursor.execute('SELECT * from Employees')
        cursor.fetchall()
        employeeListManager.delete(0, END)

        for employee in data:
            employeeListManager.insert(END, employee)

    def SearchEmployeesOnManager(search):
        searched = employeeSearchOnManagerEntry.get()

        cursor.execute('SELECT * from Employees')
        employees = cursor.fetchall()
        if searched == '':
            data = []
            for employee in employees:
                data.append(employee[1])
        else:
            data = []
            for employee in employees:
                employeesName = employee[1]
                if searched.lower() in employeesName.lower():
                    data.append(employeesName)

        UpdateEmployeesOnManager(sorted(data))

    for employee in employees:
        data = []
        for employee in employees:
            data.append(employee[1])
        employeesSorted = sorted(data)
        UpdateEmployeesOnManager(employeesSorted)
        
    def LoadEmployeeOnManager(self):
        #connect = sqlite3.connect('MsClients.db')
        cursor.execute('SELECT * from Employees')
        Employees = cursor.fetchall()
        try:
            loadedEmployee = employeeListManager.get(employeeListManager.curselection())
        except:
            messagebox.showerror("Error", "You must select a client from the list.")
            return
        
        for employee in Employees:
            if employee[1] == loadedEmployee:
                EmployeeIDLabel.config(text=employee[0])
                EmployeeUsernameEntry.delete(0,END)
                EmployeeUsernameEntry.insert(0, employee[1])

                #if employee[2] == 1:
                #    MarriedChecked.select()
                #else:
                #    MarriedChecked.deselect()

                EmployeePasswordEntry.delete(0,END)
                EmployeePasswordEntry.insert(0,employee[2])
                EmployeeFirstNameEntry.delete(0,END)
                EmployeeFirstNameEntry.insert(0,employee[3])
                EmployeeMiddleNameEntry.delete(0,END)
                EmployeeMiddleNameEntry.insert(0,employee[4])
                EmployeeLastNameEntry.delete(0,END)
                EmployeeLastNameEntry.insert(0,employee[5])
                EmployeeAccessEntry.delete(0,END)
                EmployeeAccessEntry.insert(0,employee[6])
                EmployeeEmailEntry.delete(0,END)
                EmployeeEmailEntry.insert(0,employee[7])
                EmployeePhoneEntry.delete(0,END)
                EmployeePhoneEntry.insert(0,employee[8])
                EmployeeAddressEntry.delete(0,END)
                EmployeeAddressEntry.insert(0,employee[9])
                EmployeeAptEntry.delete(0,END)
                EmployeeAptEntry.insert(0,employee[10])
                EmployeeCityEntry.delete(0,END)
                EmployeeCityEntry.insert(0,employee[11])
                EmployeeStateEntry.delete(0,END)
                EmployeeStateEntry.insert(0,employee[12])
                EmployeeZipEntry.delete(0,END)
                EmployeeZipEntry.insert(0,employee[13])
                EmployeeSSNEntry.delete(0,END)
                EmployeeSSNEntry.insert(0,employee[14])
                EmployeeSalaryEntry.delete(0,END)
                EmployeeSalaryEntry.insert(0,employee[15])

                #if client[41] == 1:
                #    driver5MarriedChecked.select()
                #else:
                #    driver5MarriedChecked.deselect()
                #
                #if client[42] == 1:
                #    priorInsuranceCheck.select()
                #else:
                #    priorInsuranceCheck.deselect()

                #if client[47] == 0:
                #    BiLimit.set(0)
                #elif client[47] == 1:
                #    BiLimit.set(1)
                #elif client[47] == 2:
                #    BiLimit.set(2)
                #elif client[47] == 3:
                #    BiLimit.set(3)
                #else:
                #    BiLimit.set(0)

                #try:
                #    getClientLicensePhoto = Image.open(f'images/{client[0]}{client[1]}.png')
                #    #getClientLicensePhoto.show()
                #    showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
                #    licenseLabel.config(image=showClientLicensePhoto)
                #    licenseLabel.image = showClientLicensePhoto
                #    photoLabel.config(text=f'images/{client[0]}{client[1]}.png', fg='black')
                #    print("carregou")
                #except:
                #    getClientLicensePhoto = Image.open("imageicon.png")
                #    #getClientLicensePhoto.show()
                #    showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
                #    licenseLabel.config(image=showClientLicensePhoto)
                #    licenseLabel.image = showClientLicensePhoto
                #    photoLabel.config(text='')
                #    print("nao carregou")
                #    pass

        #print("Loaded")

    def onSearchEmployeeManagerClick(event):
        if employeeSearchOnManagerEntry.get() == "Search Employee...":
            employeeSearchOnManagerEntry.delete(0, END)
            employeeSearchOnManagerEntry.insert(0, "")
            employeeSearchOnManagerEntry.config(fg="black")
        
    def onSearchEmployeeManagerFocusOut(event):
        if employeeSearchOnManagerEntry.get() == "":
            employeeSearchOnManagerEntry.insert(0, "Search Employee...")
            employeeSearchOnManagerEntry.config(fg="grey")

    def UpdateUser():
        EmployeeID = EmployeeIDLabel.cget("text")
        EmployeeUsername = EmployeeUsernameEntry.get()
        EmployeePassword = EmployeePasswordEntry.get()
        EmployeeFirstName = EmployeeFirstNameEntry.get()
        EmployeeMiddleName = EmployeeMiddleNameEntry.get()
        EmployeeLastName = EmployeeLastNameEntry.get()
        EmployeeAccess = EmployeeAccessEntry.get()
        EmployeeEmail = EmployeeEmailEntry.get()
        EmployeePhone = EmployeePhoneEntry.get()
        EmployeeAddress = EmployeeAddressEntry.get()
        EmployeeApt = EmployeeAptEntry.get()
        EmployeeCity = EmployeeCityEntry.get()
        EmployeeState = EmployeeStateEntry.get()
        EmployeeZip = EmployeeZipEntry.get()
        EmployeeSSN = EmployeeSSNEntry.get()
        EmployeeSalary = EmployeeSalaryEntry.get()
        EmployeePhoto = EmployeeSSNEntry.get()
        ##REVISE
        cursor.execute('''UPDATE Employees SET Username=?, Password=?, FirstName=?, MiddleName=?, LastName=?, Access=?, email=?, phone=?, address=?,
                            apt=?, city=?, state=?, zip=?, SSN=?, salary=?, photo=? WHERE id=?''', 
                            (EmployeeUsername, EmployeePassword, EmployeeFirstName, EmployeeMiddleName, EmployeeLastName, EmployeeAccess, EmployeeEmail,
                             EmployeePhone, EmployeeAddress, EmployeeApt, EmployeeCity, EmployeeState, EmployeeZip, EmployeeSSN, EmployeeSalary, EmployeePhoto, EmployeeID))
        connect.commit()
        
        messagebox.showinfo("Updated!", f"User for {EmployeeFirstName} {EmployeeMiddleName} {EmployeeLastName} has been updated!")

    employeeSearchOnManagerEntry = Entry(manageUserWindow,font=("Helvetica", 15), width=14, bg="white", fg="grey")
    employeeSearchOnManagerEntry.place(x=610, y=308)
    employeeSearchOnManagerEntry.insert(0, "Search Employee...")
    employeeListManager.bind("<Double-Button-1>", LoadEmployeeOnManager)
    employeeSearchOnManagerEntry.bind("<KeyRelease>", SearchEmployeesOnManager)
    employeeSearchOnManagerEntry.bind("<FocusIn>", onSearchEmployeeManagerClick)
    employeeSearchOnManagerEntry.bind("<FocusOut>", onSearchEmployeeManagerFocusOut)

    Label(manageUserWindow, text="ID", font=("Arial", 15), background="#516CC2", fg="white") .place(x=1850, y=10)
    EmployeeIDLabel = Label(manageUserWindow, text="", font=("Arial", 15), bg="#516CC2")
    EmployeeIDLabel.place(x=1800, y=10)

    Label(manageUserWindow, text="Username", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=10)
    EmployeeUsernameEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeeUsernameEntry.place(x=180, y=10)
    
    Label(manageUserWindow, text="Password", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=50)
    EmployeePasswordEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeePasswordEntry.place(x=180, y=50)
    
    Label(manageUserWindow, text="First Name", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=90)
    EmployeeFirstNameEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeeFirstNameEntry.place(x=180, y=90)
    
    Label(manageUserWindow, text="Middle Name", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=130)
    EmployeeMiddleNameEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeeMiddleNameEntry.place(x=180, y=130)
    
    Label(manageUserWindow, text="Last Name", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=170)
    EmployeeLastNameEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeeLastNameEntry.place(x=180, y=170)
    
    Label(manageUserWindow, text="Access", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=210)
    EmployeeAccessEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeeAccessEntry.place(x=180, y=210)
    
    Label(manageUserWindow, text="Email", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=250)
    EmployeeEmailEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeeEmailEntry.place(x=180, y=250)
    
    Label(manageUserWindow, text="Phone", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=290)
    EmployeePhoneEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeePhoneEntry.place(x=180, y=290)

    Label(manageUserWindow, text="Address", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=330)
    EmployeeAddressEntry = Entry(manageUserWindow, font=("Arial", 15), width=20, bg="white")
    EmployeeAddressEntry.place(x=180, y=330)
    
    Label(manageUserWindow, text="Apt", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=370)
    EmployeeAptEntry = Entry(manageUserWindow, font=("Arial", 15), width=5, bg="white")
    EmployeeAptEntry.place(x=180, y=370)

    Label(manageUserWindow, text="City", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=410)
    EmployeeCityEntry = Entry(manageUserWindow, font=("Arial", 15), width=15, bg="white")
    EmployeeCityEntry.place(x=180, y=410)
    
    Label(manageUserWindow, text="State", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=450)
    EmployeeStateEntry = Entry(manageUserWindow, font=("Arial", 15), width=5, bg="white")
    EmployeeStateEntry.place(x=180, y=450)
    
    Label(manageUserWindow, text="ZIP", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=490)
    EmployeeZipEntry = Entry(manageUserWindow, font=("Arial", 15), width=15, bg="white")
    EmployeeZipEntry.place(x=180, y=490)
    
    Label(manageUserWindow, text="SSN", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=530)
    EmployeeSSNEntry = Entry(manageUserWindow, font=("Arial", 15), width=15, bg="white")
    EmployeeSSNEntry.place(x=180, y=530)
    
    Label(manageUserWindow, text="Salary", font=("Arial", 15), background="#516CC2", fg="white") .place(x=50, y=570)
    EmployeeSalaryEntry = Entry(manageUserWindow, font=("Arial", 15), width=15, bg="white")
    EmployeeSalaryEntry.place(x=180, y=570)
    
    UpdateUserButton = tk.Button(manageUserWindow, text="Update", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=UpdateUser)
    UpdateUserButton.place(x=220, y=620)

    LoadUserButton = tk.Button(manageUserWindow, text="Load", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=LoadEmployee)
    LoadUserButton.place(x=600, y=580)

def clickToLogin():
    Login(0)

def clickToLoad():
    Load(0)

def clickToManageEmployee():
    ManageUsersPopUp

def LoadEmployee(self):
    #connect = sqlite3.connect('MsClients.db')
    cursor.execute('SELECT * from Employees')
    Employees = cursor.fetchall()
    try:
        loadedEmployee = employeeList.get(employeeList.curselection())
    except:
        messagebox.showerror("Error", "You must select a client from the list.")
        return
    
    for employee in Employees:
        if employee[1] == loadedEmployee:
            EmployeeID.config(text=employee[0])
            EmployeeUsername.config(text=employee[1])

            #if employee[2] == 1:
            #    MarriedChecked.select()
            #else:
            #    MarriedChecked.deselect()

            EmployeePassword.config(text=employee[2])
            EmployeeFirstName.config(text=employee[3])
            EmployeeMiddleName.config(text=employee[4])
            EmployeeLastName.config(text=employee[5])
            EmployeeAccess.config(text=employee[6])
            EmployeeEmail.config(text=employee[7])
            EmployeePhone.config(text=employee[8])
            EmployeeAddress.config(text=employee[9])
            EmployeeApt.config(text=employee[10])
            EmployeeCity.config(text=employee[11])
            EmployeeState.config(text=employee[12])
            EmployeeZip.config(text=employee[13])
            EmployeeSSN.config(text=employee[14])
            EmployeeSalary.config(text=employee[15])

            #if client[41] == 1:
            #    driver5MarriedChecked.select()
            #else:
            #    driver5MarriedChecked.deselect()
            #
            #if client[42] == 1:
            #    priorInsuranceCheck.select()
            #else:
            #    priorInsuranceCheck.deselect()

            #if client[47] == 0:
            #    BiLimit.set(0)
            #elif client[47] == 1:
            #    BiLimit.set(1)
            #elif client[47] == 2:
            #    BiLimit.set(2)
            #elif client[47] == 3:
            #    BiLimit.set(3)
            #else:
            #    BiLimit.set(0)

            #try:
            #    getClientLicensePhoto = Image.open(f'images/{client[0]}{client[1]}.png')
            #    #getClientLicensePhoto.show()
            #    showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
            #    licenseLabel.config(image=showClientLicensePhoto)
            #    licenseLabel.image = showClientLicensePhoto
            #    photoLabel.config(text=f'images/{client[0]}{client[1]}.png', fg='black')
            #    print("carregou")
            #except:
            #    getClientLicensePhoto = Image.open("imageicon.png")
            #    #getClientLicensePhoto.show()
            #    showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
            #    licenseLabel.config(image=showClientLicensePhoto)
            #    licenseLabel.image = showClientLicensePhoto
            #    photoLabel.config(text='')
            #    print("nao carregou")
            #    pass

    #print("Loaded")

def splitWord(word):
    return [char for char in word]

def hoursCheckPopUp():
    hoursCheckWindow = Toplevel(bg="#516CC2")
    hoursCheckWindow.iconbitmap('favicon-16x16.ico')
    hoursCheckWindow.title("Employees Hours")
    hoursCheckWindow.geometry("700x650")
    #hoursCheckWindow.resizable(False, False)
    topWindowsToCloseOnLogout.append(hoursCheckWindow)
    
    global firstDatePicked
    global firstDatePicked
    global firstDatePicked
    global lastDatePicked
    global lastDatePicked
    global lastDatePicked
    
    firstDatePickedYear = int(firstDatePicked.get_date().year)
    firstDatePickedMonth = int(firstDatePicked.get_date().month)
    firstDatePickedDay = int(firstDatePicked.get_date().day)
    lastDatePickedYear = int(lastDatePicked.get_date().year)
    lastDatePickedMonth = int(lastDatePicked.get_date().month)
    lastDatePickedDay = int(lastDatePicked.get_date().day)
    
    topframe = Frame(hoursCheckWindow, bg="#516CC2")
    topframe.pack(side=TOP)

    centerFrame = Frame(hoursCheckWindow, bg="#516CC2")
    centerFrame.place(relwidth=0.33, relheight=0.825, x=250,y=40)
    #centerFrame.place(relwidth=0.33, relheight=0.8, x=250,y=40)
    centerCanvas = Canvas(hoursCheckWindow, bg="#516CC2", width=230, height=550, highlightthickness=0)
    anotherFrame = Frame(centerCanvas, bg="#516CC2")
    centerCanvas.create_window((10,0), window=anotherFrame, anchor="nw")
    centerCanvas.bind('<Configure>', lambda e: centerCanvas.configure(scrollregion=centerCanvas.bbox("all")))
    #centerCanvas.place(relwidth=0.3, relheight=0.8, x=250,y=40)
    centerCanvas.pack()
    hoursCheckWindowScrollBar = Scrollbar(centerFrame, orient=VERTICAL, command=centerCanvas.yview)
    centerCanvas.configure(yscrollcommand=hoursCheckWindowScrollBar.set)
    bottomframe = Frame(hoursCheckWindow, bg="#516CC2")
    bottomframe.pack(side=BOTTOM)
    hoursCheckWindowScrollBar.pack(side=RIGHT, fill=Y)


    empID = EmployeeID.cget("text")
    empFirst = EmployeeFirstName.cget("text")
    empMiddle = EmployeeMiddleName.cget("text")
    empLast = EmployeeLastName.cget("text")
    cursor.execute('SELECT salary from Employees WHERE id=?',[empID])
    fetchedEmpID = [ x[0] for x in cursor.fetchall()]
    EmployeeSalary = fetchedEmpID[0]
    salaryConvertedTimes100 = (float(EmployeeSalary) * 100.0)
    divideSalaryBySeconds = (salaryConvertedTimes100 / 60.0) / 60.0
    totalTimeWorked = []
    labelEmpName = Label(topframe, text=f"{empFirst} {empMiddle} {empLast}", font=("Arial", 15), background="#516CC2", fg="white")
    labelEmpName.pack()
    sdate = date(firstDatePickedYear,firstDatePickedMonth,firstDatePickedDay)
    edate = date(lastDatePickedYear,lastDatePickedMonth,lastDatePickedDay)
    dates = pandas.date_range(sdate, edate, freq='d')
    def updateDateLoop():
        index = 0
        for i in dates:
            cursor.execute('SELECT Date from EmployeeHours WHERE EmployeeID=?',[empID])
            #fetchedDate = [ x[0] for x in cursor.fetchall()]
            for fetchedDate in cursor.fetchall():
                getDateFromDb = fetchedDate[0]
                if getDateFromDb == str(i.strftime('%Y-%m-%d')):
                    cursor.execute('SELECT TimeWorked from EmployeeHours WHERE EmployeeID=?',[empID])
                    fetchedTimeWorked = [ x[0] for x in cursor.fetchall()]
                    getTimeWorkedFromDb = fetchedTimeWorked[index]
                    index += 1
                    labelDate = Label(anotherFrame, text=f"{str(i.strftime('%Y-%m-%d'))}:", font=("Arial", 15), background="#516CC2", fg="white")
                    labelDate.pack()
                    labelHoursWorked = Label(anotherFrame, text=f"Hours Worked: {timedelta(seconds=getTimeWorkedFromDb)}", font=("Arial", 15), background="#516CC2", fg="white")
                    labelHoursWorked.pack()
                    totalTimeWorked.append(getTimeWorkedFromDb)
                    cursor.execute('SELECT ClockedIn1 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn1 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn1FromDb = fetchedClockedIn1[0]
                    cursor.execute('SELECT ClockedOut1 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut1 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut1FromDb = fetchedClockedOut1[0]
                    if getClockedIn1FromDb != None:
                        labelClockedIn1 = Label(anotherFrame, text=f"{getClockedIn1FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn1.pack()
                    if getClockedOut1FromDb != None:
                        labelClockedOut1 = Label(anotherFrame, text=f"{getClockedOut1FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut1.pack()
                    cursor.execute('SELECT ClockedIn2 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn2 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn2FromDb = fetchedClockedIn2[0]
                    cursor.execute('SELECT ClockedOut2 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut2 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut2FromDb = fetchedClockedOut2[0]
                    if getClockedIn2FromDb != None:
                        labelClockedIn2 = Label(anotherFrame, text=f"{getClockedIn2FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn2.pack()
                    if getClockedOut2FromDb != None:
                        labelClockedOut2 = Label(anotherFrame, text=f"{getClockedOut2FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut2.pack()
                    cursor.execute('SELECT ClockedIn3 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn3 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn3FromDb = fetchedClockedIn3[0]
                    cursor.execute('SELECT ClockedOut3 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut3 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut3FromDb = fetchedClockedOut3[0]
                    if getClockedIn3FromDb != None:
                        labelClockedIn3 = Label(anotherFrame, text=f"{getClockedIn3FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn3.pack()
                    if getClockedOut3FromDb != None:
                        labelClockedOut3 = Label(anotherFrame, text=f"{getClockedOut3FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut3.pack()
                    cursor.execute('SELECT ClockedIn4 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn4 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn4FromDb = fetchedClockedIn4[0]
                    cursor.execute('SELECT ClockedOut4 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut4 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut4FromDb = fetchedClockedOut4[0]
                    if getClockedIn4FromDb != None:
                        labelClockedIn4 = Label(anotherFrame, text=f"{getClockedIn4FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn4.pack()
                    if getClockedOut4FromDb != None:
                        labelClockedOut4 = Label(anotherFrame, text=f"{getClockedOut4FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut4.pack()
                    cursor.execute('SELECT ClockedIn5 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn5 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn5FromDb = fetchedClockedIn5[0]
                    cursor.execute('SELECT ClockedOut5 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut5 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut5FromDb = fetchedClockedOut5[0]
                    if getClockedIn5FromDb != None:
                        labelClockedIn5 = Label(anotherFrame, text=f"{getClockedIn5FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn5.pack()
                    if getClockedOut5FromDb != None:
                        labelClockedOut5 = Label(anotherFrame, text=f"{getClockedOut5FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut5.pack()
                    cursor.execute('SELECT ClockedIn6 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn6 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn6FromDb = fetchedClockedIn6[0]
                    cursor.execute('SELECT ClockedOut6 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut6 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut6FromDb = fetchedClockedOut6[0]
                    if getClockedIn6FromDb != None:
                        labelClockedIn6 = Label(anotherFrame, text=f"{getClockedIn6FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn6.pack()
                    if getClockedOut6FromDb != None:
                        labelClockedOut6 = Label(anotherFrame, text=f"{getClockedOut6FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut6.pack()
                    cursor.execute('SELECT ClockedIn7 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn7 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn7FromDb = fetchedClockedIn7[0]
                    cursor.execute('SELECT ClockedOut7 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut7 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut7FromDb = fetchedClockedOut7[0]
                    if getClockedIn7FromDb != None:
                        labelClockedIn7 = Label(anotherFrame, text=f"{getClockedIn7FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn7.pack()
                    if getClockedOut7FromDb != None:
                        labelClockedOut7 = Label(anotherFrame, text=f"{getClockedOut7FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut7.pack()
                    cursor.execute('SELECT ClockedIn8 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn8 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn8FromDb = fetchedClockedIn8[0]
                    cursor.execute('SELECT ClockedOut8 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut8 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut8FromDb = fetchedClockedOut8[0]
                    if getClockedIn8FromDb != None:
                        labelClockedIn8 = Label(anotherFrame, text=f"{getClockedIn8FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn8.pack()
                    if getClockedOut8FromDb != None:
                        labelClockedOut8 = Label(anotherFrame, text=f"{getClockedOut8FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut8.pack()
                    cursor.execute('SELECT ClockedIn9 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn9 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn9FromDb = fetchedClockedIn9[0]
                    cursor.execute('SELECT ClockedOut9 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut9 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut9FromDb = fetchedClockedOut9[0]
                    if getClockedIn9FromDb != None:
                        labelClockedIn9 = Label(anotherFrame, text=f"{getClockedIn9FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn9.pack()
                    if getClockedOut9FromDb != None:
                        labelClockedOut9 = Label(anotherFrame, text=f"{getClockedOut9FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut9.pack()
                    cursor.execute('SELECT ClockedIn10 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedIn10 = [ x[0] for x in cursor.fetchall()]
                    getClockedIn10FromDb = fetchedClockedIn10[0]
                    cursor.execute('SELECT ClockedOut10 from EmployeeHours WHERE EmployeeID=? AND Date=?',[empID, getDateFromDb])
                    fetchedClockedOut10 = [ x[0] for x in cursor.fetchall()]
                    getClockedOut10FromDb = fetchedClockedOut10[0]
                    if getClockedIn10FromDb != None:
                        labelClockedIn10 = Label(anotherFrame, text=f"{getClockedIn10FromDb}", font=("Arial", 15), background="green", fg="white")
                        labelClockedIn10.pack()
                    if getClockedOut10FromDb != None:
                        labelClockedOut10 = Label(anotherFrame, text=f"{getClockedOut10FromDb}", font=("Arial", 15), background="red", fg="white")
                        labelClockedOut10.pack()
    updateDateLoop()
    totalMoneyEarned = (divideSalaryBySeconds * float(sum(totalTimeWorked))) / 100.0
    totalHoursWorked = timedelta(seconds=sum(totalTimeWorked))
    totalHoursLabel =Label(bottomframe, text=f"Total Hours Worked: {totalHoursWorked}", font=("Arial", 15), background="black", fg="white")
    totalHoursLabel.pack()
    totalHoursLabel =Label(bottomframe, text=f"Total Money Earned: {totalMoneyEarned}", font=("Arial", 15), background="black", fg="white")
    totalHoursLabel.pack()

def calculateSalary():
    userID = UserIDfound.cget("text")
    cursor.execute('SELECT salary from Employees WHERE id=?',[userID])
    fetchedUserID = [ x[0] for x in cursor.fetchall()]
    EmployeeSalary = fetchedUserID[0]
    salaryConvertedTimes100 = (float(EmployeeSalary) * 100.0)
    divideSalaryBySeconds = (salaryConvertedTimes100 / 60.0) / 60.0
    
    cursor.execute('SELECT mondayTimeWorked from Employees WHERE id=?',[userID])
    fetchedMondayTimeWorked = [ x[0] for x in cursor.fetchall()]
    getMondayTimeWorked = fetchedMondayTimeWorked[0]
    #
    cursor.execute('SELECT tuesdayTimeWorked from Employees WHERE id=?',[userID])
    fetchedTuesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
    getTuesdayTimeWorked = fetchedTuesdayTimeWorked[0]  
    #
    cursor.execute('SELECT wednesdayTimeWorked from Employees WHERE id=?',[userID])
    fetchedWednesdayTimeWorked = [ x[0] for x in cursor.fetchall()]
    getWednesdayTimeWorked = fetchedWednesdayTimeWorked[0]
    #
    cursor.execute('SELECT thursdayTimeWorked from Employees WHERE id=?',[userID])
    fetchedThursdayTimeWorked = [ x[0] for x in cursor.fetchall()]
    getThursdayTimeWorked = fetchedThursdayTimeWorked[0]
    #
    cursor.execute('SELECT fridayTimeWorked from Employees WHERE id=?',[userID])
    fetchedFridayTimeWorked = [ x[0] for x in cursor.fetchall()]
    getFridayTimeWorked = fetchedFridayTimeWorked[0]

    totalMoneyEarned = (divideSalaryBySeconds * float(getMondayTimeWorked + getTuesdayTimeWorked + getWednesdayTimeWorked + getThursdayTimeWorked + getFridayTimeWorked)) / 100.0
    salaryEarned.config(text=totalMoneyEarned)

def onSearchEmployeeClick(event):
    if employeeSearchEntry.get() == "Search Employee...":
        employeeSearchEntry.delete(0, END)
        employeeSearchEntry.insert(0, "")
        employeeSearchEntry.config(fg="black")

def onSearchEmployeeFocusOut(event):
    if employeeSearchEntry.get() == "":
        employeeSearchEntry.insert(0, "Search Employee...")
        employeeSearchEntry.config(fg="grey")

def onSearchClientClick(event):
    if clientSearchEntry.get() == "Search Client...":
        clientSearchEntry.delete(0, END)
        clientSearchEntry.insert(0, "")
        clientSearchEntry.config(fg="black")

def onSearchClientFocusOut(event):
    if clientSearchEntry.get() == "":
        clientSearchEntry.insert(0, "Search Client...")
        clientSearchEntry.config(fg="grey")

def onSearchDocumentClick(event):
    if documentSearchEntry.get() == "Search Document...":
        documentSearchEntry.delete(0, END)
        documentSearchEntry.insert(0, "")
        documentSearchEntry.config(fg="black")

def onSearchDocumentFocusOut(event):
    if documentSearchEntry.get() == "":
        documentSearchEntry.insert(0, "Search Document...")
        documentSearchEntry.config(fg="grey")

def showDatesAndHoursWorked():
    global MondayTimer
    global TuesdayTimer
    global WednesdayTimer
    global ThursdayTimer
    global FridayTimer
    global salaryEarned
    
    Label(GetDaysAndHoursWorked, text="Monday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=0)
    MondayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
    MondayTimer.place(x=110, y=0)
    Label(GetDaysAndHoursWorked, text="Tuesday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=30)
    TuesdayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
    TuesdayTimer.place(x=110, y=30)
    Label(GetDaysAndHoursWorked, text="Wednesday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=60)
    WednesdayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
    WednesdayTimer.place(x=130, y=60)
    Label(GetDaysAndHoursWorked, text="Thursday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=90)
    ThursdayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
    ThursdayTimer.place(x=110, y=90)
    Label(GetDaysAndHoursWorked, text="Friday:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=120)
    FridayTimer = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
    FridayTimer.place(x=110, y=120)
    
    Label(GetDaysAndHoursWorked, text="Salary Earned:", font=("Helvetica", 15), fg="white", bg="black").place(x=0, y=200)
    salaryEarned = Label(GetDaysAndHoursWorked, text="", font=("Helvetica", 15), fg="white", bg="black")
    salaryEarned.place(x=140, y=200)

def getHoursWorkedOnTheDay():
    for widget in ClockWindow.winfo_children():
        widget.destroy()
    try:    
        getEmployeeID = UserIDfound.cget("text")
        cursor.execute('SELECT ClockedIn1 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn1 = [ x[0] for x in cursor.fetchall()]
        getClockedIn1FromDb = fetchedClockedIn1[0]
        cursor.execute('SELECT ClockedOut1 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut1 = [ x[0] for x in cursor.fetchall()]
        getClockedOut1FromDb = fetchedClockedOut1[0]
        if getClockedIn1FromDb != None:
            labelClockedIn1 = Label(ClockWindow, text=f"{getClockedIn1FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn1.pack()
        if getClockedOut1FromDb != None:
            labelClockedOut1 = Label(ClockWindow, text=f"{getClockedOut1FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut1.pack()
        cursor.execute('SELECT ClockedIn2 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn2 = [ x[0] for x in cursor.fetchall()]
        getClockedIn2FromDb = fetchedClockedIn2[0]
        cursor.execute('SELECT ClockedOut2 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut2 = [ x[0] for x in cursor.fetchall()]
        getClockedOut2FromDb = fetchedClockedOut2[0]
        if getClockedIn2FromDb != None:
            labelClockedIn2 = Label(ClockWindow, text=f"{getClockedIn2FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn2.pack()
        if getClockedOut2FromDb != None:
            labelClockedOut2 = Label(ClockWindow, text=f"{getClockedOut2FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut2.pack()
        cursor.execute('SELECT ClockedIn3 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn3 = [ x[0] for x in cursor.fetchall()]
        getClockedIn3FromDb = fetchedClockedIn3[0]
        cursor.execute('SELECT ClockedOut3 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut3 = [ x[0] for x in cursor.fetchall()]
        getClockedOut3FromDb = fetchedClockedOut3[0]
        if getClockedIn3FromDb != None:
            labelClockedIn3 = Label(ClockWindow, text=f"{getClockedIn3FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn3.pack()
        if getClockedOut3FromDb != None:
            labelClockedOut3 = Label(ClockWindow, text=f"{getClockedOut3FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut3.pack()
        cursor.execute('SELECT ClockedIn4 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn4 = [ x[0] for x in cursor.fetchall()]
        getClockedIn4FromDb = fetchedClockedIn4[0]
        cursor.execute('SELECT ClockedOut4 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut4 = [ x[0] for x in cursor.fetchall()]
        getClockedOut4FromDb = fetchedClockedOut4[0]
        if getClockedIn4FromDb != None:
            labelClockedIn4 = Label(ClockWindow, text=f"{getClockedIn4FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn4.pack()
        if getClockedOut4FromDb != None:
            labelClockedOut4 = Label(ClockWindow, text=f"{getClockedOut4FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut4.pack()
        cursor.execute('SELECT ClockedIn5 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn5 = [ x[0] for x in cursor.fetchall()]
        getClockedIn5FromDb = fetchedClockedIn5[0]
        cursor.execute('SELECT ClockedOut5 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut5 = [ x[0] for x in cursor.fetchall()]
        getClockedOut5FromDb = fetchedClockedOut5[0]
        if getClockedIn5FromDb != None:
            labelClockedIn5 = Label(ClockWindow, text=f"{getClockedIn5FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn5.pack()
        if getClockedOut5FromDb != None:
            labelClockedOut5 = Label(ClockWindow, text=f"{getClockedOut5FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut5.pack()
        cursor.execute('SELECT ClockedIn6 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn6 = [ x[0] for x in cursor.fetchall()]
        getClockedIn6FromDb = fetchedClockedIn6[0]
        cursor.execute('SELECT ClockedOut6 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut6 = [ x[0] for x in cursor.fetchall()]
        getClockedOut6FromDb = fetchedClockedOut6[0]
        if getClockedIn6FromDb != None:
            labelClockedIn6 = Label(ClockWindow, text=f"{getClockedIn6FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn6.pack()
        if getClockedOut6FromDb != None:
            labelClockedOut6 = Label(ClockWindow, text=f"{getClockedOut6FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut6.pack()
        cursor.execute('SELECT ClockedIn7 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn7 = [ x[0] for x in cursor.fetchall()]
        getClockedIn7FromDb = fetchedClockedIn7[0]
        cursor.execute('SELECT ClockedOut7 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut7 = [ x[0] for x in cursor.fetchall()]
        getClockedOut7FromDb = fetchedClockedOut7[0]
        if getClockedIn7FromDb != None:
            labelClockedIn7 = Label(ClockWindow, text=f"{getClockedIn7FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn7.pack()
        if getClockedOut7FromDb != None:
            labelClockedOut7 = Label(ClockWindow, text=f"{getClockedOut7FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut7.pack()
        cursor.execute('SELECT ClockedIn8 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn8 = [ x[0] for x in cursor.fetchall()]
        getClockedIn8FromDb = fetchedClockedIn8[0]
        cursor.execute('SELECT ClockedOut8 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut8 = [ x[0] for x in cursor.fetchall()]
        getClockedOut8FromDb = fetchedClockedOut8[0]
        if getClockedIn8FromDb != None:
            labelClockedIn8 = Label(ClockWindow, text=f"{getClockedIn8FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn8.pack()
        if getClockedOut8FromDb != None:
            labelClockedOut8 = Label(ClockWindow, text=f"{getClockedOut8FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut8.pack()
        cursor.execute('SELECT ClockedIn9 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn9 = [ x[0] for x in cursor.fetchall()]
        getClockedIn9FromDb = fetchedClockedIn9[0]
        cursor.execute('SELECT ClockedOut9 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut9 = [ x[0] for x in cursor.fetchall()]
        getClockedOut9FromDb = fetchedClockedOut9[0]
        if getClockedIn9FromDb != None:
            labelClockedIn9 = Label(ClockWindow, text=f"{getClockedIn9FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn9.pack()
        if getClockedOut9FromDb != None:
            labelClockedOut9 = Label(ClockWindow, text=f"{getClockedOut9FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut9.pack()
        cursor.execute('SELECT ClockedIn10 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedIn10 = [ x[0] for x in cursor.fetchall()]
        getClockedIn10FromDb = fetchedClockedIn10[0]
        cursor.execute('SELECT ClockedOut10 from EmployeeHours WHERE EmployeeID=? AND Date=?',[getEmployeeID, currentDate])
        fetchedClockedOut10 = [ x[0] for x in cursor.fetchall()]
        getClockedOut10FromDb = fetchedClockedOut10[0]
        if getClockedIn10FromDb != None:
            labelClockedIn10 = Label(ClockWindow, text=f"{getClockedIn10FromDb}", font=("Arial", 15), background="green", fg="white")
            labelClockedIn10.pack()
        if getClockedOut10FromDb != None:
            labelClockedOut10 = Label(ClockWindow, text=f"{getClockedOut10FromDb}", font=("Arial", 15), background="red", fg="white")
            labelClockedOut10.pack()
    except:
        pass

def newAutoForm():
    clientIDfound.config(text="")
    NameInsured.delete(0,END)
    MarriedChecked.deselect()
    emailEntry.delete(0,END)
    phoneEntry.delete(0,END)
    addressEntry.delete(0,END)
    AptEntry.delete(0,END)
    cityEntry.delete(0,END)
    stateEntry.delete(0,END)
    zipEntry.delete(0,END)
    OwnedChecked.deselect()
    SameAsMailingChecked.deselect()
    mailingAddressEntry.delete(0,END)
    mailingAptEntry.delete(0,END)
    mailingcityEntry.delete(0,END)
    mailingstateEntry.delete(0,END)
    mailingzipEntry.delete(0,END)
    driver1Entry.delete(0,END)
    driver1LicenseEntry.delete(0,END)
    driver1StateEntry.delete(0,END)
    driver1DobEntry.delete(0,END)
    driver1MarriedChecked.deselect()
    driver2Entry.delete(0,END)
    driver2LicenseEntry.delete(0,END)
    driver2StateEntry.delete(0,END)
    driver2DobEntry.delete(0,END)
    driver2MarriedChecked.deselect()
    driver3Entry.delete(0,END)
    driver3LicenseEntry.delete(0,END)
    driver3StateEntry.delete(0,END)
    driver3DobEntry.delete(0,END)
    driver3MarriedChecked.deselect()
    driver4Entry.delete(0,END)
    driver4LicenseEntry.delete(0,END)
    driver4StateEntry.delete(0,END)
    driver4DobEntry.delete(0,END)
    driver4MarriedChecked.deselect()
    driver5Entry.delete(0,END)
    driver5LicenseEntry.delete(0,END)
    driver5StateEntry.delete(0,END)
    driver5DobEntry.delete(0,END)
    driver5MarriedChecked.deselect()
    priorInsuranceCheck.deselect()
    carrierEntry.delete(0,END)
    policyNumberEntry.delete(0,END)
    yearsWithPolicyEntry.delete(0,END)
    expDatePolicyEntry.delete(0,END)
    BiLimit.set(0)
    PdLimit.set(0)
    PipDeductibleChecked.deselect()
    PdForYourVehicleChecked.deselect()
    PdDeductibleForYourVehicle.set(0)
    vehicle1Entry.delete(0,END)
    vehicle1MakeEntry.delete(0,END)
    vehicle1ModelEntry.delete(0,END)
    vehicle1VINEntry.delete(0,END)         
    vehicle1FinancedChecked.deselect()
    vehicle1LeasedChecked.deselect()
    vehicle2Entry.delete(0,END)
    vehicle2MakeEntry.delete(0,END)
    vehicle2ModelEntry.delete(0,END)
    vehicle2VINEntry.delete(0,END)    
    vehicle2FinancedChecked.deselect()
    vehicle2LeasedChecked.deselect()
    vehicle3Entry.delete(0,END)
    vehicle3MakeEntry.delete(0,END)
    vehicle3ModelEntry.delete(0,END)
    vehicle3VINEntry.delete(0,END)         
    vehicle3FinancedChecked.deselect()
    vehicle3LeasedChecked.deselect()
    vehicle4Entry.delete(0,END)
    vehicle4MakeEntry.delete(0,END)
    vehicle4ModelEntry.delete(0,END)
    vehicle4VINEntry.delete(0,END)         
    vehicle4FinancedChecked.deselect()
    vehicle4LeasedChecked.deselect()
    vehicle5Entry.delete(0,END)
    vehicle5MakeEntry.delete(0,END)
    vehicle5ModelEntry.delete(0,END)
    vehicle5VINEntry.delete(0,END)         
    vehicle5FinancedChecked.deselect()
    vehicle5LeasedChecked.deselect()
    accident1Entry.delete(0,END)
    accident1TypeEntry.delete(0,END)
    accident1DriverEntry.delete(0,END)
    accident1PIPEntry.delete(0,END)
    accident1PointsOnLicenseEntry.delete(0,END)
    accident2Entry.delete(0,END)
    accident2TypeEntry.delete(0,END)
    accident2DriverEntry.delete(0,END)
    accident2PIPEntry.delete(0,END)
    accident2PointsOnLicenseEntry.delete(0,END)
    accident3Entry.delete(0,END)
    accident3TypeEntry.delete(0,END)
    accident3DriverEntry.delete(0,END)
    accident3PIPEntry.delete(0,END)
    accident3PointsOnLicenseEntry.delete(0,END)
    getClientLicensePhoto = Image.open("imageicon.png")
    showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
    licenseLabel.config(image=showClientLicensePhoto)
    licenseLabel.image = showClientLicensePhoto
    documentsData = []
    UpdateDocuments(documentsData)

#Auto
AutoQuote = Frame(LoggedInWindow, bg="black")
AutoQuote.place(relwidth=0.525, relheight=0.75, x=10,y=190)

#Auto Quote
Label(AutoQuote, text="Name Insured", background="black", fg="white") .place(x=5, y=10)
NameInsured = Entry(AutoQuote, width=20, bg="white")
NameInsured.place(x=100, y=10)

Married = IntVar()
Label(AutoQuote, text="Married", background="black", fg="white") .place(x=230, y=10)
MarriedChecked = Checkbutton(AutoQuote, variable=Married, bg="black")
MarriedChecked.place(x=280, y=10)

Label(AutoQuote, text="Email", background="black", fg="white") .place(x=5, y=40)
emailEntry = Entry(AutoQuote, width=20, bg="white")
emailEntry.place(x=100, y=40)

Label(AutoQuote, text="Phone", background="black", fg="white") .place(x=230, y=40)
phoneEntry = Entry(AutoQuote, width=20, bg="white")
phoneEntry.place(x=280, y=40)

Label(AutoQuote, text="Address", background="black", fg="white") .place(x=5, y=70)
addressEntry = Entry(AutoQuote, width=30, bg="white")
addressEntry.place(x=100, y=70)

Label(AutoQuote, text="Apt", background="black", fg="white") .place(x=290, y=70)
AptEntry = Entry(AutoQuote, width=5, bg="white")
AptEntry.place(x=320, y=70)

Owned = IntVar()
Label(AutoQuote, text="Owned", background="black", fg="white") .place(x=355, y=70)
OwnedChecked = Checkbutton(AutoQuote, variable=Owned, bg="black")
OwnedChecked.place(x=395, y=70)

Label(AutoQuote, text="City", background="black", fg="white") .place(x=5, y=100)
cityEntry = Entry(AutoQuote, width=15, bg="white")
cityEntry.place(x=100, y=100)

Label(AutoQuote, text="State", background="black", fg="white") .place(x=200, y=100)
stateEntry = Entry(AutoQuote, width=5, bg="white")
stateEntry.place(x=240, y=100)

Label(AutoQuote, text="Zip Code", background="black", fg="white") .place(x=280, y=100)
zipEntry = Entry(AutoQuote, width=10, bg="white")
zipEntry.place(x=340, y=100)

SameAsMailing = IntVar()
Label(AutoQuote, text="Same As Mailing", background="black", fg="white") .place(x=525, y=30)
SameAsMailingChecked = Checkbutton(AutoQuote, variable=SameAsMailing, bg="black")
SameAsMailingChecked.place(x=625, y=30)

#separators
ttk.Separator(AutoQuote, orient="vertical").place(x=420,y=5, height=130, width=1)

ttk.Separator(AutoQuote, orient="vertical").place(x=780,y=5, height=330, width=1)

#mailing address
Label(AutoQuote, text="Mailing Address", background="black", fg="white") .place(x=430, y=70)
mailingAddressEntry = Entry(AutoQuote, width=28, bg="white")
mailingAddressEntry.place(x=525, y=70)

Label(AutoQuote, text="Apt", background="black", fg="white") .place(x=700, y=70)
mailingAptEntry = Entry(AutoQuote, width=5, bg="white")
mailingAptEntry.place(x=730, y=70)

Label(AutoQuote, text="City", background="black", fg="white") .place(x=430, y=100)
mailingcityEntry = Entry(AutoQuote, width=15, bg="white")
mailingcityEntry.place(x=460, y=100)

Label(AutoQuote, text="State", background="black", fg="white") .place(x=560, y=100)
mailingstateEntry = Entry(AutoQuote, width=5, bg="white")
mailingstateEntry.place(x=600, y=100)

Label(AutoQuote, text="Zip Code", background="black", fg="white") .place(x=640, y=100)
mailingzipEntry = Entry(AutoQuote, width=10, bg="white")
mailingzipEntry.place(x=700, y=100)

#drivers
Label(AutoQuote, text="Driver 1", background="black", fg="white") .place(x=5, y=150)
driver1Entry = Entry(AutoQuote, width=20, bg="white")
driver1Entry.place(x=100, y=150)

Label(AutoQuote, text="License #", background="black", fg="white") .place(x=230, y=150)
driver1LicenseEntry = Entry(AutoQuote, width=20, bg="white")
driver1LicenseEntry.place(x=290, y=150)

Label(AutoQuote, text="State", background="black", fg="white") .place(x=420, y=150)
driver1StateEntry = Entry(AutoQuote, width=5, bg="white")
driver1StateEntry.place(x=455, y=150)

Label(AutoQuote, text="Date Of Birth", background="black", fg="white") .place(x=495, y=150)
driver1DobEntry = Entry(AutoQuote, width=15, bg="white")
driver1DobEntry.place(x=575, y=150)

driver1Married = IntVar()
Label(AutoQuote, text="Married", background="black", fg="white") .place(x=675, y=150)
driver1MarriedChecked = Checkbutton(AutoQuote, variable=driver1Married, bg="black")
driver1MarriedChecked.place(x=720, y=150)

Label(AutoQuote, text="Driver 2", background="black", fg="white") .place(x=5, y=180)
driver2Entry = Entry(AutoQuote, width=20, bg="white")
driver2Entry.place(x=100, y=180)

Label(AutoQuote, text="License #", background="black", fg="white") .place(x=230, y=180)
driver2LicenseEntry = Entry(AutoQuote, width=20, bg="white")
driver2LicenseEntry.place(x=290, y=180)

Label(AutoQuote, text="State", background="black", fg="white") .place(x=420, y=180)
driver2StateEntry = Entry(AutoQuote, width=5, bg="white")
driver2StateEntry.place(x=455, y=180)

Label(AutoQuote, text="Date Of Birth", background="black", fg="white") .place(x=495, y=180)
driver2DobEntry = Entry(AutoQuote, width=15, bg="white")
driver2DobEntry.place(x=575, y=180)

driver2Married = IntVar()
Label(AutoQuote, text="Married", background="black", fg="white") .place(x=675, y=180)
driver2MarriedChecked = Checkbutton(AutoQuote, variable=driver2Married, bg="black")
driver2MarriedChecked.place(x=720, y=180)

Label(AutoQuote, text="Driver 3", background="black", fg="white") .place(x=5, y=210)
driver3Entry = Entry(AutoQuote, width=20, bg="white")
driver3Entry.place(x=100, y=210)

Label(AutoQuote, text="License #", background="black", fg="white") .place(x=230, y=210)
driver3LicenseEntry = Entry(AutoQuote, width=20, bg="white")
driver3LicenseEntry.place(x=290, y=210)

Label(AutoQuote, text="State", background="black", fg="white") .place(x=420, y=210)
driver3StateEntry = Entry(AutoQuote, width=5, bg="white")
driver3StateEntry.place(x=455, y=210)

Label(AutoQuote, text="Date Of Birth", background="black", fg="white") .place(x=495, y=210)
driver3DobEntry = Entry(AutoQuote, width=15, bg="white")
driver3DobEntry.place(x=575, y=210)

driver3Married = IntVar()
Label(AutoQuote, text="Married", background="black", fg="white") .place(x=675, y=210)
driver3MarriedChecked = Checkbutton(AutoQuote, variable=driver3Married, bg="black")
driver3MarriedChecked.place(x=720, y=210)

Label(AutoQuote, text="Driver 4", background="black", fg="white") .place(x=5, y=240)
driver4Entry = Entry(AutoQuote, width=20, bg="white")
driver4Entry.place(x=100, y=240)

Label(AutoQuote, text="License #", background="black", fg="white") .place(x=230, y=240)
driver4LicenseEntry = Entry(AutoQuote, width=20, bg="white")
driver4LicenseEntry.place(x=290, y=240)

Label(AutoQuote, text="State", background="black", fg="white") .place(x=420, y=240)
driver4StateEntry = Entry(AutoQuote, width=5, bg="white")
driver4StateEntry.place(x=455, y=240)

Label(AutoQuote, text="Date Of Birth", background="black", fg="white") .place(x=495, y=240)
driver4DobEntry = Entry(AutoQuote, width=15, bg="white")
driver4DobEntry.place(x=575, y=240)

driver4Married = IntVar()
Label(AutoQuote, text="Married", background="black", fg="white") .place(x=675, y=240)
driver4MarriedChecked = Checkbutton(AutoQuote, variable=driver4Married, bg="black")
driver4MarriedChecked.place(x=720, y=240)

Label(AutoQuote, text="Driver 5", background="black", fg="white") .place(x=5, y=270)
driver5Entry = Entry(AutoQuote, width=20, bg="white")
driver5Entry.place(x=100, y=270)

Label(AutoQuote, text="License #", background="black", fg="white") .place(x=230, y=270)
driver5LicenseEntry = Entry(AutoQuote, width=20, bg="white")
driver5LicenseEntry.place(x=290, y=270)

Label(AutoQuote, text="State", background="black", fg="white") .place(x=420, y=270)
driver5StateEntry = Entry(AutoQuote, width=5, bg="white")
driver5StateEntry.place(x=455, y=270)

Label(AutoQuote, text="Date Of Birth", background="black", fg="white") .place(x=495, y=270)
driver5DobEntry = Entry(AutoQuote, width=15, bg="white")
driver5DobEntry.place(x=575, y=270)

driver5Married = IntVar()
Label(AutoQuote, text="Married", background="black", fg="white") .place(x=675, y=270)
driver5MarriedChecked = Checkbutton(AutoQuote, variable=driver5Married, bg="black")
driver5MarriedChecked.place(x=720, y=270)

#prior Insurance
priorInsurance = IntVar()
Label(AutoQuote, text="6 months of Prior Insurance", background="black", fg="white") .place(x=5, y=300)
priorInsuranceCheck = Checkbutton(AutoQuote, variable=priorInsurance, bg="black")
priorInsuranceCheck.place(x=170, y=300)

Label(AutoQuote, text="Carrier", background="black", fg="white") .place(x=200, y=300)
carrierEntry = Entry(AutoQuote, width=20, bg="white")
carrierEntry.place(x=240, y=300)

Label(AutoQuote, text="Policy #", background="black", fg="white") .place(x=350, y=300)
policyNumberEntry = Entry(AutoQuote, width=20, bg="white")
policyNumberEntry.place(x=400, y=300)

Label(AutoQuote, text="Years W/ Policy", background="black", fg="white") .place(x=520, y=300)
yearsWithPolicyEntry = Entry(AutoQuote, width=5, bg="white")
yearsWithPolicyEntry.place(x=610, y=300)

Label(AutoQuote, text="Exp Date", background="black", fg="white") .place(x=640, y=300)
expDatePolicyEntry = Entry(AutoQuote, width=10, bg="white")
expDatePolicyEntry.place(x=695, y=300)

#Liability Limits
BiLimit = IntVar()
Label(AutoQuote, text="BI Limit:", background="black", fg="white") .place(x=5, y=330)
Label(AutoQuote, text="10/20", background="black", fg="white") .place(x=80, y=330)
Bi1020 = Radiobutton(AutoQuote, variable=BiLimit, value=1, bg="black").place(x=115, y=330)
Label(AutoQuote, text="25/50", background="black", fg="white") .place(x=150, y=330)
Bi2550 = Radiobutton(AutoQuote, variable=BiLimit, value=2, bg="black").place(x=185, y=330)
Label(AutoQuote, text="100+", background="black", fg="white") .place(x=220, y=330)
Bi100Plus = Radiobutton(AutoQuote, variable=BiLimit, value=3, bg="black").place(x=250, y=330)

PdLimit = IntVar()
Label(AutoQuote, text="PD Limit:", background="black", fg="white") .place(x=320, y=330)
Label(AutoQuote, text="10", background="black", fg="white") .place(x=380, y=330)
Pd10 = Radiobutton(AutoQuote, variable=PdLimit, value=1, bg="black").place(x=400, y=330)
Label(AutoQuote, text="25", background="black", fg="white") .place(x=430, y=330)
Pd25 = Radiobutton(AutoQuote, variable=PdLimit, value=2, bg="black").place(x=450, y=330)
Label(AutoQuote, text="50", background="black", fg="white") .place(x=480, y=330)
Pd50 = Radiobutton(AutoQuote, variable=PdLimit, value=3, bg="black").place(x=500, y=330)
Label(AutoQuote, text="100", background="black", fg="white") .place(x=530, y=330)
Pd100 = Radiobutton(AutoQuote, variable=PdLimit, value=4, bg="black").place(x=555, y=330)

PipDeductible = IntVar()
Label(AutoQuote, text="PIP Deductible", background="black", fg="white") .place(x=600, y=330)
PipDeductibleChecked = Checkbutton(AutoQuote, variable=PipDeductible, bg="black")
PipDeductibleChecked.place(x=680, y=330)

PdForYourVehicle = IntVar()
Label(AutoQuote, text="PD For Your Vehicle", background="black", fg="white") .place(x=5, y=360)
PdForYourVehicleChecked = Checkbutton(AutoQuote, variable=PdForYourVehicle, bg="black")
PdForYourVehicleChecked.place(x=130, y=360)

PdDeductibleForYourVehicle = IntVar()
Label(AutoQuote, text="If Yes, Deductible:", background="black", fg="white") .place(x=180, y=360)
Label(AutoQuote, text="$500", background="black", fg="white") .place(x=300, y=360)
PdDeductible500 = Radiobutton(AutoQuote, variable=PdDeductibleForYourVehicle, value=1, bg="black").place(x=330, y=360)
Label(AutoQuote, text="$1000", background="black", fg="white") .place(x=360, y=360)
PdDeductible1000 = Radiobutton(AutoQuote, variable=PdDeductibleForYourVehicle, value=2, bg="black").place(x=400, y=360)
#PdDeductibleOther = Entry(AutoQuote, width=10, bg="white")
#PdDeductibleOther.place(x=295, y=360)

#Vehicles
Label(AutoQuote, text="Vehicle 1: Year", background="black", fg="white") .place(x=5, y=410)
vehicle1Entry = Entry(AutoQuote, width=10, bg="white")
vehicle1Entry.place(x=100, y=410)

Label(AutoQuote, text="Make", background="black", fg="white") .place(x=170, y=410)
vehicle1MakeEntry = Entry(AutoQuote, width=20, bg="white")
vehicle1MakeEntry.place(x=210, y=410)

Label(AutoQuote, text="Model", background="black", fg="white") .place(x=340, y=410)
vehicle1ModelEntry = Entry(AutoQuote, width=20, bg="white")
vehicle1ModelEntry.place(x=385, y=410)

Label(AutoQuote, text="VIN", background="black", fg="white") .place(x=510, y=410)
vehicle1VINEntry = Entry(AutoQuote, width=20, bg="white")
vehicle1VINEntry.place(x=535, y=410)

vehicle1Financed= IntVar()
Label(AutoQuote, text="Financed", background="black", fg="white") .place(x=660, y=410)
vehicle1FinancedChecked = Checkbutton(AutoQuote, variable=vehicle1Financed, bg="black")
vehicle1FinancedChecked.place(x=710, y=410)

vehicle1Leased= IntVar()
Label(AutoQuote, text="Leased", background="black", fg="white") .place(x=730, y=410)
vehicle1LeasedChecked = Checkbutton(AutoQuote, variable=vehicle1Leased, bg="black")
vehicle1LeasedChecked.place(x=770, y=410)

Label(AutoQuote, text="Vehicle 2: Year", background="black", fg="white") .place(x=5, y=440)
vehicle2Entry = Entry(AutoQuote, width=10, bg="white")
vehicle2Entry.place(x=100, y=440)

Label(AutoQuote, text="Make", background="black", fg="white") .place(x=170, y=440)
vehicle2MakeEntry = Entry(AutoQuote, width=20, bg="white")
vehicle2MakeEntry.place(x=210, y=440)

Label(AutoQuote, text="Model", background="black", fg="white") .place(x=340, y=440)
vehicle2ModelEntry = Entry(AutoQuote, width=20, bg="white")
vehicle2ModelEntry.place(x=385, y=440)

Label(AutoQuote, text="VIN", background="black", fg="white") .place(x=510, y=440)
vehicle2VINEntry = Entry(AutoQuote, width=20, bg="white")
vehicle2VINEntry.place(x=535, y=440)

vehicle2Financed= IntVar()
Label(AutoQuote, text="Financed", background="black", fg="white") .place(x=660, y=440)
vehicle2FinancedChecked = Checkbutton(AutoQuote, variable=vehicle2Financed, bg="black")
vehicle2FinancedChecked.place(x=710, y=440)

vehicle2Leased= IntVar()
Label(AutoQuote, text="Leased", background="black", fg="white") .place(x=730, y=440)
vehicle2LeasedChecked = Checkbutton(AutoQuote, variable=vehicle2Leased, bg="black")
vehicle2LeasedChecked.place(x=770, y=440)

Label(AutoQuote, text="Vehicle 3: Year", background="black", fg="white") .place(x=5, y=470)
vehicle3Entry = Entry(AutoQuote, width=10, bg="white")
vehicle3Entry.place(x=100, y=470)

Label(AutoQuote, text="Make", background="black", fg="white") .place(x=170, y=470)
vehicle3MakeEntry = Entry(AutoQuote, width=20, bg="white")
vehicle3MakeEntry.place(x=210, y=470)

Label(AutoQuote, text="Model", background="black", fg="white") .place(x=340, y=470)
vehicle3ModelEntry = Entry(AutoQuote, width=20, bg="white")
vehicle3ModelEntry.place(x=385, y=470)

Label(AutoQuote, text="VIN", background="black", fg="white") .place(x=510, y=470)
vehicle3VINEntry = Entry(AutoQuote, width=20, bg="white")
vehicle3VINEntry.place(x=535, y=470)

vehicle3Financed= IntVar()
Label(AutoQuote, text="Financed", background="black", fg="white") .place(x=660, y=470)
vehicle3FinancedChecked = Checkbutton(AutoQuote, variable=vehicle3Financed, bg="black")
vehicle3FinancedChecked.place(x=710, y=470)

vehicle3Leased= IntVar()
Label(AutoQuote, text="Leased", background="black", fg="white") .place(x=730, y=470)
vehicle3LeasedChecked = Checkbutton(AutoQuote, variable=vehicle3Leased, bg="black")
vehicle3LeasedChecked.place(x=770, y=470)

Label(AutoQuote, text="Vehicle 4: Year", background="black", fg="white") .place(x=5, y=500)
vehicle4Entry = Entry(AutoQuote, width=10, bg="white")
vehicle4Entry.place(x=100, y=500)

Label(AutoQuote, text="Make", background="black", fg="white") .place(x=170, y=500)
vehicle4MakeEntry = Entry(AutoQuote, width=20, bg="white")
vehicle4MakeEntry.place(x=210, y=500)

Label(AutoQuote, text="Model", background="black", fg="white") .place(x=340, y=500)
vehicle4ModelEntry = Entry(AutoQuote, width=20, bg="white")
vehicle4ModelEntry.place(x=385, y=500)

Label(AutoQuote, text="VIN", background="black", fg="white") .place(x=510, y=500)
vehicle4VINEntry = Entry(AutoQuote, width=20, bg="white")
vehicle4VINEntry.place(x=535, y=500)

vehicle4Financed= IntVar()
Label(AutoQuote, text="Financed", background="black", fg="white") .place(x=660, y=500)
vehicle4FinancedChecked = Checkbutton(AutoQuote, variable=vehicle4Financed, bg="black")
vehicle4FinancedChecked.place(x=710, y=500)

vehicle4Leased= IntVar()
Label(AutoQuote, text="Leased", background="black", fg="white") .place(x=730, y=500)
vehicle4LeasedChecked = Checkbutton(AutoQuote, variable=vehicle4Leased, bg="black")
vehicle4LeasedChecked.place(x=770, y=500)

Label(AutoQuote, text="Vehicle 5: Year", background="black", fg="white") .place(x=5, y=530)
vehicle5Entry = Entry(AutoQuote, width=10, bg="white")
vehicle5Entry.place(x=100, y=530)

Label(AutoQuote, text="Make", background="black", fg="white") .place(x=170, y=530)
vehicle5MakeEntry = Entry(AutoQuote, width=20, bg="white")
vehicle5MakeEntry.place(x=210, y=530)

Label(AutoQuote, text="Model", background="black", fg="white") .place(x=340, y=530)
vehicle5ModelEntry = Entry(AutoQuote, width=20, bg="white")
vehicle5ModelEntry.place(x=385, y=530)

Label(AutoQuote, text="VIN", background="black", fg="white") .place(x=510, y=530)
vehicle5VINEntry = Entry(AutoQuote, width=20, bg="white")
vehicle5VINEntry.place(x=535, y=530)

vehicle5Financed= IntVar()
Label(AutoQuote, text="Financed", background="black", fg="white") .place(x=660, y=530)
vehicle5FinancedChecked = Checkbutton(AutoQuote, variable=vehicle5Financed, bg="black")
vehicle5FinancedChecked.place(x=710, y=530)

vehicle5Leased= IntVar()
Label(AutoQuote, text="Leased", background="black", fg="white") .place(x=730, y=530)
vehicle5LeasedChecked = Checkbutton(AutoQuote, variable=vehicle5Leased, bg="black")
vehicle5LeasedChecked.place(x=770, y=530)

#Accidents
Label(AutoQuote, text="Accident 1: Date", background="black", fg="white") .place(x=5, y=580)
accident1Entry = Entry(AutoQuote, width=10, bg="white")
accident1Entry.place(x=110, y=580)

Label(AutoQuote, text="Type Of Accident", background="black", fg="white") .place(x=175, y=580)
accident1TypeEntry = Entry(AutoQuote, width=20, bg="white")
accident1TypeEntry.place(x=275, y=580)

Label(AutoQuote, text="Driver", background="black", fg="white") .place(x=375, y=580)
accident1DriverEntry = Entry(AutoQuote, width=20, bg="white")
accident1DriverEntry.place(x=415, y=580)

Label(AutoQuote, text="PIP Claim", background="black", fg="white") .place(x=540, y=580)
accident1PIPEntry = Entry(AutoQuote, width=20, bg="white")
accident1PIPEntry.place(x=595, y=580)

Label(AutoQuote, text="Points DL", background="black", fg="white") .place(x=700, y=580)
accident1PointsOnLicenseEntry = Entry(AutoQuote, width=5, bg="white")
accident1PointsOnLicenseEntry.place(x=760, y=580)

Label(AutoQuote, text="Accident 2: Date", background="black", fg="white") .place(x=5, y=610)
accident2Entry = Entry(AutoQuote, width=10, bg="white")
accident2Entry.place(x=110, y=610)

Label(AutoQuote, text="Type Of Accident", background="black", fg="white") .place(x=175, y=610)
accident2TypeEntry = Entry(AutoQuote, width=20, bg="white")
accident2TypeEntry.place(x=275, y=610)

Label(AutoQuote, text="Driver", background="black", fg="white") .place(x=375, y=610)
accident2DriverEntry = Entry(AutoQuote, width=20, bg="white")
accident2DriverEntry.place(x=415, y=610)

Label(AutoQuote, text="PIP Claim", background="black", fg="white") .place(x=540, y=610)
accident2PIPEntry = Entry(AutoQuote, width=20, bg="white")
accident2PIPEntry.place(x=595, y=610)

Label(AutoQuote, text="Points DL", background="black", fg="white") .place(x=700, y=610)
accident2PointsOnLicenseEntry = Entry(AutoQuote, width=5, bg="white")
accident2PointsOnLicenseEntry.place(x=760, y=610)

Label(AutoQuote, text="Accident 3: Date", background="black", fg="white") .place(x=5, y=640)
accident3Entry = Entry(AutoQuote, width=10, bg="white")
accident3Entry.place(x=110, y=640)

Label(AutoQuote, text="Type Of Accident", background="black", fg="white") .place(x=175, y=640)
accident3TypeEntry = Entry(AutoQuote, width=20, bg="white")
accident3TypeEntry.place(x=275, y=640)

Label(AutoQuote, text="Driver", background="black", fg="white") .place(x=375, y=640)
accident3DriverEntry = Entry(AutoQuote, width=20, bg="white")
accident3DriverEntry.place(x=415, y=640)

Label(AutoQuote, text="PIP Claim", background="black", fg="white") .place(x=540, y=640)
accident3PIPEntry = Entry(AutoQuote, width=20, bg="white")
accident3PIPEntry.place(x=595, y=640)

Label(AutoQuote, text="Points DL", background="black", fg="white") .place(x=700, y=640)
accident3PointsOnLicenseEntry = Entry(AutoQuote, width=5, bg="white")
accident3PointsOnLicenseEntry.place(x=760, y=640)

#Home
HomeQuote = Frame(LoggedInWindow, bg="black")
HomeQuote.place_forget()

Label(HomeQuote, text="HOME UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)


#Life
LifeQuote = Frame(LoggedInWindow, bg="black")
LifeQuote.place_forget()

Label(LifeQuote, text="LIFE UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Health
HealthQuote = Frame(LoggedInWindow, bg="black")
HealthQuote.place_forget()

Label(HealthQuote, text="HEALTH UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#General Liability
GeneralLiabilityQuote = Frame(LoggedInWindow, bg="black")
GeneralLiabilityQuote.place_forget()

Label(GeneralLiabilityQuote, text="GL UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Workers Comp
WorkersCompQuote = Frame(LoggedInWindow, bg="black")
WorkersCompQuote.place_forget()

Label(WorkersCompQuote, text="WC UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Motorcycle
MotorcycleQuote = Frame(LoggedInWindow, bg="black")
MotorcycleQuote.place_forget()

Label(MotorcycleQuote, text="MOTORCYCLE UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Boat
BoatQuote = Frame(LoggedInWindow, bg="black")
BoatQuote.place_forget()

Label(BoatQuote, text="BOAT UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Flood
FloodQuote = Frame(LoggedInWindow, bg="black")
FloodQuote.place_forget()

Label(FloodQuote, text="FLOOD UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Umbrella
UmbrellaQuote = Frame(LoggedInWindow, bg="black")
UmbrellaQuote.place_forget()

Label(UmbrellaQuote, text="UMBRELLA UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Admin Panel
AdminPanel = Frame(LoggedInWindow, bg="black")
AdminPanel.place_forget()
    
ttk.Separator(AdminPanel, orient="vertical").place(x=780,y=5, height=780, width=1)

cursor.execute('SELECT * from Employees')
employees = cursor.fetchall()

employeeListFrame = Frame(AdminPanel)
employeeListFrame.place(relwidth=0.2, relheight=0.3, x=610,y=90)
employeeListScrollBar = Scrollbar(employeeListFrame, orient=VERTICAL)

employeeList = Listbox(AdminPanel, yscrollcommand=employeeListScrollBar.set)
employeeList.place(relwidth=0.18, relheight=0.3, x=610,y=90)
employeeListScrollBar.config(command=employeeList.yview)
employeeListScrollBar.pack(side=RIGHT, fill=Y)

Label(AdminPanel, text="ID", font=("Arial", 15), background="black", fg="black") .place(x=5, y=90)
EmployeeID = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="black")
EmployeeID.place(x=515, y=559)

Label(AdminPanel, text="Username:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=90)
EmployeeUsername = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeUsername.place(x=135, y=90)

Label(AdminPanel, text="Password:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=130)
EmployeePassword = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeePassword.place(x=135, y=130)

Label(AdminPanel, text="First Name:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=170)
EmployeeFirstName = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeFirstName.place(x=135, y=170)

Label(AdminPanel, text="Middle Name:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=210)
EmployeeMiddleName = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeMiddleName.place(x=135, y=210)

Label(AdminPanel, text="Last Name:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=250)
EmployeeLastName = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeLastName.place(x=135, y=250)

Label(AdminPanel, text="Access:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=290)
EmployeeAccess = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeAccess.place(x=135, y=290)

Label(AdminPanel, text="Email:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=330)
EmployeeEmail = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeEmail.place(x=135, y=330)

Label(AdminPanel, text="Phone:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=370)
EmployeePhone = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeePhone.place(x=135, y=370)

Label(AdminPanel, text="Address:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=410)
EmployeeAddress = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeAddress.place(x=135, y=410)

Label(AdminPanel, text="Apt:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=450)
EmployeeApt = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeApt.place(x=135, y=450)

Label(AdminPanel, text="City:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=490)
EmployeeCity = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeCity.place(x=135, y=490)

Label(AdminPanel, text="State:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=530)
EmployeeState = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeState.place(x=135, y=530)

Label(AdminPanel, text="ZIP:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=570)
EmployeeZip = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeZip.place(x=135, y=570)

Label(AdminPanel, text="SSN:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=610)
EmployeeSSN = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeSSN.place(x=135, y=610)
    
Label(AdminPanel, text="Salary:", font=("Arial", 15), background="black", fg="white") .place(x=5, y=650)
EmployeeSalary = Label(AdminPanel, text="", font=("Arial", 15), background="black", fg="white")
EmployeeSalary.place(x=135, y=650)

currentYear = int(time.strftime("%Y"))

Label(AdminPanel, text="Hours Worked", font=("Arial", 15), background="black", fg="white") .place(x=555, y=370)
Label(AdminPanel, text="To", font=("Arial", 15), background="black", fg="white") .place(x=605, y=405)
firstDatePicked = DateEntry(AdminPanel, dateformat=3,width=12, background='darkblue',
                    foreground='white', borderwidth=4, Calendar=currentYear)
firstDatePicked.place(x=500, y=410)
lastDatePicked = DateEntry(AdminPanel, dateformat=3, width=12, background='darkblue',
                    foreground='white', borderwidth=4, Calendar=currentYear)
lastDatePicked.place(x=650, y=410)
#print(firstDatePicked.get_date().year)
#print(firstDatePicked.get_date().month)
#print(firstDatePicked.get_date().day)
#print(lastDatePicked.get_date().year)
#print(lastDatePicked.get_date().month)
#print(lastDatePicked.get_date().day)

#print(datetime.date(int(str(dates.date[1]))))

#Search

employeeSearchEntry = Entry(AdminPanel, font=("Helvetica", 15), width=14, bg="white", fg="grey")
employeeSearchEntry.place(x=610, y=308)
employeeSearchEntry.insert(0, "Search Employee...")
clientSearchEntry = Entry(LoggedInWindow,font=("Helvetica", 15), width=21, bg="white", fg="grey")
clientSearchEntry.place(x=950, y=368)
clientSearchEntry.insert(0, "Search Client...")
documentSearchEntry = Entry(LoggedInWindow,font=("Helvetica", 15), width=21, bg="white", fg="grey")
documentSearchEntry.place(x=950, y=790)
documentSearchEntry.insert(0, "Search Document...")

clientList.bind("<Double-Button-1>", Load)
employeeList.bind("<Double-Button-1>", LoadEmployee)
documentList.bind("<Double-Button-1>", openDocument)
clientSearchEntry.bind("<KeyRelease>", Search)
clientSearchEntry.bind("<FocusIn>", onSearchClientClick)
clientSearchEntry.bind("<FocusOut>", onSearchClientFocusOut)
employeeSearchEntry.bind("<KeyRelease>", SearchEmployees)
employeeSearchEntry.bind("<FocusIn>", onSearchEmployeeClick)
employeeSearchEntry.bind("<FocusOut>", onSearchEmployeeFocusOut)
documentSearchEntry.bind("<KeyRelease>", SearchDocument)
documentSearchEntry.bind("<FocusIn>", onSearchDocumentClick)
documentSearchEntry.bind("<FocusOut>", onSearchDocumentFocusOut)

#buttons
SaveClient = tk.Button(AutoQuote, text="New Client", padx=10, pady=5, fg="white", bg="#263D42", command=newAutoForm).place(x=420, y=0)
Button(AutoQuote, text="QUOTE", padx=10, pady=5, fg="white", bg="#263D42", command=quote) .place(x=350, y=675)
Button(LoggedInWindow, text="Upload Document", padx=10, pady=5, fg="white", bg="#263D42", command=uploadDocument) .place(x=945, y=830)
Button(LoggedInWindow, text="Upload Profile Picture", padx=10, pady=5, fg="white", bg="#263D42", command=get_photo) .place(x=10, y=10)
CreateClient = tk.Button(LoggedInWindow, text="Create Client", state=NORMAL, padx=10, pady=5, fg="white", bg="#263D42", command=Save)
CreateClient.place(x=950, y=410)
#LoadClient = tk.Button(LoggedInWindow, text="Load Client", padx=10, pady=5, fg="white", bg="#263D42", command=clickToLoad).place(x=840, y=400)
UpdateClientInfo = tk.Button(LoggedInWindow, text="Save Client", padx=10, pady=5, fg="white", bg="#263D42", command=UpdateClient)
UpdateClientInfo.place(x=1100, y=410)
openLicensePhoto = tk.Button(LoggedInWindow, text="Delete Document", padx=10, pady=5, fg="white", bg="#263D42", command=deleteDocument).place(x=1075, y=830)
#openLicensePhoto = tk.Button(LoggedInWindow, text="Show Document", padx=10, pady=5, fg="white", bg="#263D42", command=openLicenseImage).place(x=1075, y=830)


ClockInButton = tk.Button(LoggedInWindow, text="  Clock In ", padx=2, pady=2, fg="white", bg="#263D42", command=ClockIn)
ClockInButton.place_forget()
ClockOutButton = tk.Button(LoggedInWindow, text="Clock Out", padx=2, pady=2, fg="white", bg="#263D42", command=ClockOut)
ClockOutButton.place_forget()

AutoQuoteButton = tk.Button(TopMenuButtons, text="Auto Quote", padx=2, pady=2, fg="white", bg="#263D42", command=AutoQuoteTab)
AutoQuoteButton.place(x=10, y=5)

HomeQuoteButton = tk.Button(TopMenuButtons, text="Home Quote", padx=2, pady=2, fg="white", bg="#263D42", command=HomeQuoteTab)
HomeQuoteButton.place(x=92, y=5)

LifeQuoteButton = tk.Button(TopMenuButtons, text="Life Quote", padx=2, pady=2, fg="white", bg="#263D42", command=LifeQuoteTab)
LifeQuoteButton.place(x=180, y=5)

HealthQuoteButton = tk.Button(TopMenuButtons, text="Health Quote", padx=2, pady=2, fg="white", bg="#263D42", command=HealthQuoteTab)
HealthQuoteButton.place(x=255, y=5)

GeneralLiabilityQuoteButton = tk.Button(TopMenuButtons, text="General Liability Quote", padx=2, pady=2, fg="white", bg="#263D42", command=GeneralLiabilityQuoteTab)
GeneralLiabilityQuoteButton.place(x=345, y=5)

WorkersCompQuoteButton = tk.Button(TopMenuButtons, text="Workers Comp Quote", padx=2, pady=2, fg="white", bg="#263D42", command=WorkersCompQuoteTab)
WorkersCompQuoteButton.place(x=485, y=5)

MotorcycleQuoteButton = tk.Button(TopMenuButtons, text="Motorcycle Quote", padx=2, pady=2, fg="white", bg="#263D42", command=MotorcycleQuoteTab)
MotorcycleQuoteButton.place(x=620, y=5)

BoatQuoteButton = tk.Button(TopMenuButtons, text="Boat Quote", padx=2, pady=2, fg="white", bg="#263D42", command=BoatQuoteTab)
BoatQuoteButton.place(x=735, y=5)

FloodQuoteButton = tk.Button(TopMenuButtons, text="Flood Quote", padx=2, pady=2, fg="white", bg="#263D42", command=FloodQuoteTab)
FloodQuoteButton.place(x=815, y=5)

UmbrellaQuoteButton = tk.Button(TopMenuButtons, text="Umbrella Quote", padx=2, pady=2, fg="white", bg="#263D42", command=UmbrellaQuoteTab)
UmbrellaQuoteButton.place(x=900, y=5)

AdminPanelButton = tk.Button(TopMenuButtons, text="Admin Panel", padx=2, pady=2, fg="white", bg="#263D42", command=AdminPanelTab)
#AdminPanelButton.place_forget()

LogoutButton = tk.Button(TopMenuButtons, text="Logout", padx=2, pady=2, fg="white", bg="#263D42", command=Logout)
LogoutButton.place(x=1440, y=5)

LoginButton = tk.Button(LoginScreen, text="Login", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=clickToLogin)
LoginBind = MainWindow.bind('<Return>', Login)
LoginButton.place(x=255, y=650)

CreateUserPopUpButton = tk.Button(AdminPanel, text="Create User", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=CreateUserPopUp)
CreateUserPopUpButton.place(x=5, y=5)

ManageUserPopUpButton = tk.Button(AdminPanel, text="Manage Users", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=ManageUsersPopUp)
ManageUserPopUpButton.place(x=150, y=5)

checkEmployeeHoursPopUpButton = tk.Button(AdminPanel, text="Check Hours", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=hoursCheckPopUp)
checkEmployeeHoursPopUpButton.place(x=555, y=450)

def on_close():
    close = messagebox.askokcancel("Exit", "Are you sure you want to exit?")
    if close:
        #print("closing db connection")
        connect.close()
        MainWindow.destroy()

MainWindow.protocol("WM_DELETE_WINDOW",  on_close)

Label(MainWindow, text="Developed By: JTelloTech.com", font=("Arial", 10), background="black", fg="white") .place(x=1320, y=930)
#
#mainloop
MainWindow.mainloop()