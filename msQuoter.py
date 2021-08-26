from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sqlite3
import io
import time

#main
MainWindow = Tk()
MainWindow.title("Morning Star Quick Quoter")
MainWindow.configure(background="black")
MainWindow.iconbitmap('favicon-16x16.ico')
MainWindow.geometry("1500x950")
MainWindow.resizable(False,False)

#Top Menu
TopMenuButtons = Frame(MainWindow, bg="blue")
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

Label(LoginScreen, text="Password", font=("Arial", 15), background="#516CC2", fg="white") .place(x=185, y=530)
Password = Entry(LoginScreen, width=20, font=("Arial", 15), bg="white")
Password.place(x=185, y=560)

#Logged In
LoggedInWindow = Frame(MainWindow, bg="black")
LoggedInWindow.place_forget()

connect = sqlite3.connect('MsClients.db')
cursor = connect.cursor()
#logo
Logo = PhotoImage(file="morning-star-logo.png")
Label(LoggedInWindow, image=Logo, bg="white") .place(x=340, y=50)

#clock
ClockLabel = Label(LoggedInWindow, text="", font=("Helvetica", 15), fg="white", bg="black")
ClockLabel.place(x=1270,y=0)

#days
Label(LoggedInWindow, text="Monday:", font=("Helvetica", 15), fg="white", bg="black").place(x=1200, y=40)
Label(LoggedInWindow, text="Tuesday:", font=("Helvetica", 15), fg="white", bg="black").place(x=1200, y=70)
Label(LoggedInWindow, text="Wednesday:", font=("Helvetica", 15), fg="white", bg="black").place(x=1200, y=100)
Label(LoggedInWindow, text="Thurdsday:", font=("Helvetica", 15), fg="white", bg="black").place(x=1200, y=130)
Label(LoggedInWindow, text="Friday:", font=("Helvetica", 15), fg="white", bg="black").place(x=1200, y=160)

#clients saved
clientListFrame = Frame(LoggedInWindow)
clientListFrame.place(relwidth=0.257, relheight=0.74, x=800,y=20)
clientListScrollBar = Scrollbar(clientListFrame, orient=VERTICAL)

clientList = Listbox(LoggedInWindow, yscrollcommand=clientListScrollBar.set)
clientList.place(relwidth=0.247, relheight=0.74, x=800,y=20)
clientListScrollBar.config(command=clientList.yview)
clientListScrollBar.pack(side=RIGHT, fill=Y)


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

def Logout():
    LoggedInWindow.place_forget()
    LoginScreen.place(relwidth=0.4, relheight=0.8, x=450,y=50)
    TopMenuButtons.place_forget()
    currentTab.config(text="Login")

def Login():
    LoggedInWindow.place(relwidth=1, relheight=1, x=0,y=40)
    LoginScreen.place_forget()
    currentTab.config(text="Auto Quote")
    TopMenuButtons.place(relwidth=1, relheight=0.04, x=0,y=0)

def get_photo():
    filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=((".png","*.png"), ("all files", "*.*")))
    photoLabel.config(text=filename, fg='white')
    return filename

def convertToBinary(filename):
    with open(filename, 'rb') as file:
        photo = file.read()
    return photo

def openLicenseImage():
    licenseImage.show()
   
def quote():
    #os.system('python seleniumProj.py')
    # get chromedriver
    PATH = r"chromedriver.exe"
    driver = webdriver.Chrome(PATH)
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
        print(accountName)
        print(accountPassword)
        insertAccountName.send_keys(accountName)
        insertAccountPassword.send_keys(accountPassword)
        insertAccountPassword.send_keys(Keys.RETURN)
    print("input credentials")
    #driver.close()

def Load():
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

            try:
                getClientLicensePhoto = Image.open(f'images/{client[0]}{client[1]}.png')
                #getClientLicensePhoto.show()
                showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
                licenseLabel.config(image=showClientLicensePhoto)
                licenseLabel.image = showClientLicensePhoto
                photoLabel.config(text=f'images/{client[0]}{client[1]}.png', fg='black')
                print("carregou")
            except:
                getClientLicensePhoto = Image.open("imageicon.png")
                #getClientLicensePhoto.show()
                showClientLicensePhoto = ImageTk.PhotoImage(getClientLicensePhoto.resize(imageSize, Image.ANTIALIAS))
                licenseLabel.config(image=showClientLicensePhoto)
                licenseLabel.image = showClientLicensePhoto
                photoLabel.config(text='')
                print("nao carregou")
                pass
            #img2 = ImageTk.PhotoImage(img1.resize(imageSize, Image.ANTIALIAS))
            #photoLabel.config(text=client[97])

    print("Loaded")
    #connect.close()
 
def Update(data):  
    cursor.execute('SELECT * from Clients')
    clients = cursor.fetchall()
    clientList.delete(0, END)

    for client in data:
        clientList.insert(END, client)

def Search(SearchName):
    #connect.execute('SELECT * from Clients WHERE name = (?)',(SearchName,))
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
    try:
        loadedClient = clientList.get(clientList.curselection())
    except:
        messagebox.showerror("Error", "You must select a client from the list.")
        return
    
    cursor.execute('SELECT id from Clients WHERE name=?',[loadedClient])
    fetchedClient = [ x[0] for x in cursor.fetchall()]
    ClientID = fetchedClient[0]
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

def Clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")

    ClockLabel.config(text=f"{hour}:{minute}:{second}")
    ClockLabel.after(1000, Clock)

def ClockIn():
    ClockInButton.place_forget()
    ClockOutButton.place(x=1200, y=3)

def ClockOut():
    ClockInButton.place(x=1200, y=3)
    ClockOutButton.place_forget()

for client in clients:
    data = []
    for client in clients:
        data.append(client[1])
    clientes = sorted(data)
    Update(clientes)

Clock()

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

Label(AdminPanel, text="ADMPANEL UNDER CONSTRUCTION", font=("Arial", 40), background="black", fg="white") .place(x=10, y=250)

#Search
Label(LoggedInWindow, text="Search: ", font=("Helvetica", 15), background="black", fg="white") .place(x=797, y=723)
clientSearchEntry = Entry(LoggedInWindow,font=("Helvetica", 15), width=28, bg="white")
clientSearchEntry.place(x=872, y=725)

clientSearchEntry.bind("<KeyRelease>", Search)

#buttons
Button(LoggedInWindow, text="QUOTE", padx=10, pady=5, fg="white", bg="#263D42", command=quote) .place(x=960, y=820)
Button(LoggedInWindow, text="Upload File", padx=10, pady=5, fg="white", bg="#263D42", command=get_photo) .place(x=860, y=820)
SaveClient = tk.Button(LoggedInWindow, text="Save Client", padx=10, pady=5, fg="white", bg="#263D42", command=Save).place(x=940, y=770)
LoadClient = tk.Button(LoggedInWindow, text="Load Client", padx=10, pady=5, fg="white", bg="#263D42", command=Load).place(x=840, y=770)
UpdateClientInfo = tk.Button(LoggedInWindow, text="Update Client", padx=10, pady=5, fg="white", bg="#263D42", command=UpdateClient).place(x=1037, y=770)
openLicensePhoto = tk.Button(LoggedInWindow, text="Show License", padx=10, pady=5, fg="white", bg="#263D42", command=openLicenseImage).place(x=1037, y=820)
ClockInButton = tk.Button(LoggedInWindow, text="  Clock In ", padx=2, pady=2, fg="white", bg="#263D42", command=ClockIn)
ClockInButton.place(x=1200, y=3)
ClockOutButton = tk.Button(LoggedInWindow, text="Clock Out", padx=2, pady=2, fg="white", bg="#263D42", command=ClockOut)
ClockOutButton.place(x=1200, y=3000)

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
AdminPanelButton.place(x=1350, y=5)

LogoutButton = tk.Button(TopMenuButtons, text="Logout", padx=2, pady=2, fg="white", bg="#263D42", command=Logout)
LogoutButton.place(x=1440, y=5)

LoginButton = tk.Button(LoginScreen, text="Login", font=("Arial", 15), padx=10, pady=1, fg="white", bg="#263D42", command=Login)
LoginButton.place(x=255, y=650)

def on_close():
    close = messagebox.askokcancel("Exit", "Are you sure you want to exit?")
    if close:
        #print("closing db connection")
        connect.close()
        MainWindow.destroy()

MainWindow.protocol("WM_DELETE_LoggedInWindow",  on_close)

#
#mainloop
MainWindow.mainloop()