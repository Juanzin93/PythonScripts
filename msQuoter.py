from tkinter import *
from tkinter import ttk
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import sqlite3

#main
window = Tk()
window.title("Morning Star Quick Quoter")
window.configure(background="black")
window.iconbitmap('favicon-16x16.ico')
window.geometry("1200x900")
window.resizable(False,False)

connect = sqlite3.connect('MsClients.db')
cursor = connect.cursor()
#logo
Logo = PhotoImage(file="morning-star-logo.png")
Label(window, image=Logo, bg="white") .place(x=340, y=50)

#clients saved
clientList = Listbox(window)
clientList.place(relwidth=0.32, relheight=0.78, x=800,y=20)

cursor.execute('CREATE TABLE IF NOT EXISTS Clients(id integer PRIMARY KEY, name TEXT, married integer)')
    
cursor.execute('SELECT * from Clients')
clients = cursor.fetchall()
for client in clients:
    clientList.insert(END, client[1])
#functions
def quote():
    #os.system('python seleniumProj.py')
    # get chromedriver
    PATH = r"C:\Users\juanz\Documents\Python Scripts\chromedriver.exe"
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

def Save():
    #connect = sqlite3.connect('MsClients.db')
    clientName = NameInsured.get()
    ClientMarried = Married.get()
    print(clientName)
    cursor.execute('INSERT INTO Clients (name, married) VALUES (?, ?)', [clientName, ClientMarried])
    print("Saved")
    clientList.insert(END, clientName)
    connect.commit()
    #connect.close()

def Load():
    #connect = sqlite3.connect('MsClients.db')
    loadedClient = clientList.get(clientList.curselection())
    for client in clients:
        print(client[1])
        print(loadedClient)
        if client[1] == loadedClient:
            NameInsured.delete(0,END)
            NameInsured.insert(0, client[1])
    print("Loaded")
    #connect.close()

def Update(data):
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

    Update(data)

#Client Info
Label(window, text="Name Insured", background="black", fg="white") .place(x=15, y=200)
NameInsured = Entry(window, width=20, bg="white")
NameInsured.place(x=100, y=200)

Married = IntVar()
Label(window, text="Married", background="black", fg="white") .place(x=230, y=200)
MarriedChecked = Checkbutton(window, variable=Married, bg="black")
MarriedChecked.place(x=280, y=200)

Owned = IntVar()
Label(window, text="Owned", background="black", fg="white") .place(x=355, y=260)
OwnedChecked = Checkbutton(window, variable=Owned, bg="black")
OwnedChecked.place(x=395, y=260)

Label(window, text="Email", background="black", fg="white") .place(x=15, y=230)
emailEntry = Entry(window, width=20, bg="white")
emailEntry.place(x=100, y=230)

Label(window, text="Phone", background="black", fg="white") .place(x=230, y=230)
phoneEntry = Entry(window, width=20, bg="white")
phoneEntry.place(x=280, y=230)

Label(window, text="Address", background="black", fg="white") .place(x=15, y=260)
addressEntry = Entry(window, width=30, bg="white")
addressEntry.place(x=100, y=260)

Label(window, text="Apt", background="black", fg="white") .place(x=290, y=260)
AptEntry = Entry(window, width=5, bg="white")
AptEntry.place(x=320, y=260)

Label(window, text="City", background="black", fg="white") .place(x=15, y=290)
cityEntry = Entry(window, width=15, bg="white")
cityEntry.place(x=100, y=290)

Label(window, text="State", background="black", fg="white") .place(x=200, y=290)
stateEntry = Entry(window, width=5, bg="white")
stateEntry.place(x=240, y=290)

Label(window, text="Zip Code", background="black", fg="white") .place(x=280, y=290)
zipEntry = Entry(window, width=10, bg="white")
zipEntry.place(x=340, y=290)

SameAsMailing = IntVar()
Label(window, text="Same As Mailing", background="black", fg="white") .place(x=525, y=220)
SameAsMailingChecked = Checkbutton(window, variable=SameAsMailing, bg="black")
SameAsMailingChecked.place(x=625, y=220)

#separators
ttk.Separator(window, orient="vertical").place(x=420,y=200, height=130, width=1)

ttk.Separator(window, orient="vertical").place(x=780,y=200, height=330, width=1)

#mailing address
Label(window, text="Mailing Address", background="black", fg="white") .place(x=430, y=260)
mailingAddressEntry = Entry(window, width=28, bg="white")
mailingAddressEntry.place(x=525, y=260)

Label(window, text="Apt", background="black", fg="white") .place(x=700, y=260)
mailingAptEntry = Entry(window, width=5, bg="white")
mailingAptEntry.place(x=730, y=260)

Label(window, text="City", background="black", fg="white") .place(x=430, y=290)
mailingcityEntry = Entry(window, width=15, bg="white")
mailingcityEntry.place(x=460, y=290)

Label(window, text="State", background="black", fg="white") .place(x=560, y=290)
mailingstateEntry = Entry(window, width=5, bg="white")
mailingstateEntry.place(x=600, y=290)

Label(window, text="Zip Code", background="black", fg="white") .place(x=640, y=290)
mailingzipEntry = Entry(window, width=10, bg="white")
mailingzipEntry.place(x=700, y=290)

#drivers
Label(window, text="Driver 1", background="black", fg="white") .place(x=15, y=340)
driver1Entry = Entry(window, width=20, bg="white")
driver1Entry.place(x=100, y=340)

Label(window, text="License #", background="black", fg="white") .place(x=230, y=340)
driver1LicenseEntry = Entry(window, width=20, bg="white")
driver1LicenseEntry.place(x=290, y=340)

Label(window, text="State", background="black", fg="white") .place(x=420, y=340)
driver1StateEntry = Entry(window, width=5, bg="white")
driver1StateEntry.place(x=455, y=340)

Label(window, text="Date Of Birth", background="black", fg="white") .place(x=495, y=340)
driver1DobEntry = Entry(window, width=15, bg="white")
driver1DobEntry.place(x=575, y=340)

driver1Married = IntVar()
Label(window, text="Married", background="black", fg="white") .place(x=675, y=340)
driver1MarriedChecked = Checkbutton(window, variable=driver1Married, bg="black")
driver1MarriedChecked.place(x=720, y=340)

Label(window, text="Driver 2", background="black", fg="white") .place(x=15, y=370)
driver2Entry = Entry(window, width=20, bg="white")
driver2Entry.place(x=100, y=370)

Label(window, text="License #", background="black", fg="white") .place(x=230, y=370)
driver2LicenseEntry = Entry(window, width=20, bg="white")
driver2LicenseEntry.place(x=290, y=370)

Label(window, text="State", background="black", fg="white") .place(x=420, y=370)
driver2StateEntry = Entry(window, width=5, bg="white")
driver2StateEntry.place(x=455, y=370)

Label(window, text="Date Of Birth", background="black", fg="white") .place(x=495, y=370)
driver2DobEntry = Entry(window, width=15, bg="white")
driver2DobEntry.place(x=575, y=370)

driver2Married = IntVar()
Label(window, text="Married", background="black", fg="white") .place(x=675, y=370)
driver2MarriedChecked = Checkbutton(window, variable=driver2Married, bg="black")
driver2MarriedChecked.place(x=720, y=370)

Label(window, text="Driver 3", background="black", fg="white") .place(x=15, y=400)
driver3Entry = Entry(window, width=20, bg="white")
driver3Entry.place(x=100, y=400)

Label(window, text="License #", background="black", fg="white") .place(x=230, y=400)
driver3LicenseEntry = Entry(window, width=20, bg="white")
driver3LicenseEntry.place(x=290, y=400)

Label(window, text="State", background="black", fg="white") .place(x=420, y=400)
driver3StateEntry = Entry(window, width=5, bg="white")
driver3StateEntry.place(x=455, y=400)

Label(window, text="Date Of Birth", background="black", fg="white") .place(x=495, y=400)
driver3DobEntry = Entry(window, width=15, bg="white")
driver3DobEntry.place(x=575, y=400)

driver3Married = IntVar()
Label(window, text="Married", background="black", fg="white") .place(x=675, y=400)
driver3MarriedChecked = Checkbutton(window, variable=driver3Married, bg="black")
driver3MarriedChecked.place(x=720, y=400)

Label(window, text="Driver 4", background="black", fg="white") .place(x=15, y=430)
driver4Entry = Entry(window, width=20, bg="white")
driver4Entry.place(x=100, y=430)

Label(window, text="License #", background="black", fg="white") .place(x=230, y=430)
driver4LicenseEntry = Entry(window, width=20, bg="white")
driver4LicenseEntry.place(x=290, y=430)

Label(window, text="State", background="black", fg="white") .place(x=420, y=430)
driver4StateEntry = Entry(window, width=5, bg="white")
driver4StateEntry.place(x=455, y=430)

Label(window, text="Date Of Birth", background="black", fg="white") .place(x=495, y=430)
driver4DobEntry = Entry(window, width=15, bg="white")
driver4DobEntry.place(x=575, y=430)

driver4Married = IntVar()
Label(window, text="Married", background="black", fg="white") .place(x=675, y=430)
driver4MarriedChecked = Checkbutton(window, variable=driver4Married, bg="black")
driver4MarriedChecked.place(x=720, y=430)

Label(window, text="Driver 5", background="black", fg="white") .place(x=15, y=460)
driver5Entry = Entry(window, width=20, bg="white")
driver5Entry.place(x=100, y=460)

Label(window, text="License #", background="black", fg="white") .place(x=230, y=460)
driver5LicenseEntry = Entry(window, width=20, bg="white")
driver5LicenseEntry.place(x=290, y=460)

Label(window, text="State", background="black", fg="white") .place(x=420, y=460)
driver5StateEntry = Entry(window, width=5, bg="white")
driver5StateEntry.place(x=455, y=460)

Label(window, text="Date Of Birth", background="black", fg="white") .place(x=495, y=460)
driver5DobEntry = Entry(window, width=15, bg="white")
driver5DobEntry.place(x=575, y=460)

driver5Married = IntVar()
Label(window, text="Married", background="black", fg="white") .place(x=675, y=460)
driver5MarriedChecked = Checkbutton(window, variable=driver5Married, bg="black")
driver5MarriedChecked.place(x=720, y=460)

#prior Insurance
priorInsurance = IntVar()
Label(window, text="6 months of Prior Insurance", background="black", fg="white") .place(x=15, y=500)
priorInsurance = Checkbutton(window, variable=priorInsurance, bg="black")
priorInsurance.place(x=170, y=500)

Label(window, text="Carrier", background="black", fg="white") .place(x=200, y=500)
carrierEntry = Entry(window, width=20, bg="white")
carrierEntry.place(x=240, y=500)

Label(window, text="Policy #", background="black", fg="white") .place(x=350, y=500)
policyNumberEntry = Entry(window, width=20, bg="white")
policyNumberEntry.place(x=400, y=500)

Label(window, text="Years W/ Policy", background="black", fg="white") .place(x=520, y=500)
yearsWithPolicyEntry = Entry(window, width=5, bg="white")
yearsWithPolicyEntry.place(x=610, y=500)

Label(window, text="Exp Date", background="black", fg="white") .place(x=640, y=500)
expDatePolicyEntry = Entry(window, width=10, bg="white")
expDatePolicyEntry.place(x=695, y=500)

#Liability Limits
BiLimit = IntVar()
Label(window, text="BI Limit:", background="black", fg="white") .place(x=15, y=530)
Label(window, text="10/20", background="black", fg="white") .place(x=80, y=530)
Bi1020 = Radiobutton(window, variable=BiLimit, bg="black").place(x=115, y=530)
Label(window, text="25/50", background="black", fg="white") .place(x=150, y=530)
Bi2550 = Radiobutton(window, variable=BiLimit, bg="black").place(x=185, y=530)
Label(window, text="100+", background="black", fg="white") .place(x=220, y=530)
Bi100Plus = Radiobutton(window, variable=BiLimit, bg="black").place(x=250, y=530)

PdLimit = IntVar()
Label(window, text="PD Limit:", background="black", fg="white") .place(x=320, y=530)
Label(window, text="10", background="black", fg="white") .place(x=380, y=530)
Pd10 = Radiobutton(window, variable=PdLimit, bg="black").place(x=400, y=530)
Label(window, text="25", background="black", fg="white") .place(x=430, y=530)
Pd25 = Radiobutton(window, variable=PdLimit, bg="black").place(x=450, y=530)
Label(window, text="50", background="black", fg="white") .place(x=480, y=530)
Pd50 = Radiobutton(window, variable=PdLimit, bg="black").place(x=500, y=530)
Label(window, text="100", background="black", fg="white") .place(x=530, y=530)
Pd100 = Radiobutton(window, variable=PdLimit, bg="black").place(x=555, y=530)

PipDeductible = IntVar()
Label(window, text="PIP Deductible", background="black", fg="white") .place(x=600, y=530)
Checkbutton(window, variable=PipDeductible, bg="black").place(x=680, y=530)

PdForYourVehicle = IntVar()
Label(window, text="PD For Your Vehicle", background="black", fg="white") .place(x=15, y=560)
Checkbutton(window, variable=PdForYourVehicle, bg="black").place(x=130, y=560)

PdDeductibleForYourVehicle = IntVar()
Label(window, text="If Yes, Deductible:", background="black", fg="white") .place(x=180, y=560)
Label(window, text="$500", background="black", fg="white") .place(x=300, y=560)
PdDeductible500 = Radiobutton(window, variable=PdDeductibleForYourVehicle, bg="black").place(x=330, y=560)
Label(window, text="$1000", background="black", fg="white") .place(x=360, y=560)
PdDeductible1000 = Radiobutton(window, variable=PdDeductibleForYourVehicle, bg="black").place(x=400, y=560)
#PdDeductibleOther = Entry(window, width=10, bg="white")
#PdDeductibleOther.place(x=295, y=560)

#Vehicles
Label(window, text="Vehicle 1: Year", background="black", fg="white") .place(x=15, y=610)
vehicle1Entry = Entry(window, width=10, bg="white")
vehicle1Entry.place(x=100, y=610)

Label(window, text="Make", background="black", fg="white") .place(x=170, y=610)
vehicle1MakeEntry = Entry(window, width=20, bg="white")
vehicle1MakeEntry.place(x=210, y=610)

Label(window, text="Model", background="black", fg="white") .place(x=340, y=610)
vehicle1ModelEntry = Entry(window, width=20, bg="white")
vehicle1ModelEntry.place(x=385, y=610)

Label(window, text="VIN", background="black", fg="white") .place(x=510, y=610)
vehicle1VINEntry = Entry(window, width=20, bg="white")
vehicle1VINEntry.place(x=535, y=610)

Financed1= IntVar()
Label(window, text="Financed", background="black", fg="white") .place(x=660, y=610)
Checkbutton(window, variable=Financed1, bg="black").place(x=710, y=610)

Leased1= IntVar()
Label(window, text="Leased", background="black", fg="white") .place(x=730, y=610)
Checkbutton(window, variable=Leased1, bg="black").place(x=770, y=610)

Label(window, text="Vehicle 2: Year", background="black", fg="white") .place(x=15, y=640)
vehicle2Entry = Entry(window, width=10, bg="white")
vehicle2Entry.place(x=100, y=640)

Label(window, text="Make", background="black", fg="white") .place(x=170, y=640)
vehicle2MakeEntry = Entry(window, width=20, bg="white")
vehicle2MakeEntry.place(x=210, y=640)

Label(window, text="Model", background="black", fg="white") .place(x=340, y=640)
vehicle2ModelEntry = Entry(window, width=20, bg="white")
vehicle2ModelEntry.place(x=385, y=640)

Label(window, text="VIN", background="black", fg="white") .place(x=510, y=640)
vehicle2VINEntry = Entry(window, width=20, bg="white")
vehicle2VINEntry.place(x=535, y=640)

Financed2= IntVar()
Label(window, text="Financed", background="black", fg="white") .place(x=660, y=640)
Checkbutton(window, variable=Financed2, bg="black").place(x=710, y=640)

Leased2= IntVar()
Label(window, text="Leased", background="black", fg="white") .place(x=730, y=640)
Checkbutton(window, variable=Leased2, bg="black").place(x=770, y=640)

Label(window, text="Vehicle 3: Year", background="black", fg="white") .place(x=15, y=670)
vehicle3Entry = Entry(window, width=10, bg="white")
vehicle3Entry.place(x=100, y=670)

Label(window, text="Make", background="black", fg="white") .place(x=170, y=670)
vehicle3MakeEntry = Entry(window, width=20, bg="white")
vehicle3MakeEntry.place(x=210, y=670)

Label(window, text="Model", background="black", fg="white") .place(x=340, y=670)
vehicle3ModelEntry = Entry(window, width=20, bg="white")
vehicle3ModelEntry.place(x=385, y=670)

Label(window, text="VIN", background="black", fg="white") .place(x=510, y=670)
vehicle3VINEntry = Entry(window, width=20, bg="white")
vehicle3VINEntry.place(x=535, y=670)

Financed3= IntVar()
Label(window, text="Financed", background="black", fg="white") .place(x=660, y=670)
Checkbutton(window, variable=Financed3, bg="black").place(x=710, y=670)

Leased3= IntVar()
Label(window, text="Leased", background="black", fg="white") .place(x=730, y=670)
Checkbutton(window, variable=Leased3, bg="black").place(x=770, y=670)

Label(window, text="Vehicle 4: Year", background="black", fg="white") .place(x=15, y=700)
vehicle4Entry = Entry(window, width=10, bg="white")
vehicle4Entry.place(x=100, y=700)

Label(window, text="Make", background="black", fg="white") .place(x=170, y=700)
vehicle4MakeEntry = Entry(window, width=20, bg="white")
vehicle4MakeEntry.place(x=210, y=700)

Label(window, text="Model", background="black", fg="white") .place(x=340, y=700)
vehicle4ModelEntry = Entry(window, width=20, bg="white")
vehicle4ModelEntry.place(x=385, y=700)

Label(window, text="VIN", background="black", fg="white") .place(x=510, y=700)
vehicle4VINEntry = Entry(window, width=20, bg="white")
vehicle4VINEntry.place(x=535, y=700)

Financed4= IntVar()
Label(window, text="Financed", background="black", fg="white") .place(x=660, y=700)
Checkbutton(window, variable=Financed4, bg="black").place(x=710, y=700)

Leased4= IntVar()
Label(window, text="Leased", background="black", fg="white") .place(x=730, y=700)
Checkbutton(window, variable=Leased4, bg="black").place(x=770, y=700)

Label(window, text="Vehicle 5: Year", background="black", fg="white") .place(x=15, y=730)
vehicle5Entry = Entry(window, width=10, bg="white")
vehicle5Entry.place(x=100, y=730)

Label(window, text="Make", background="black", fg="white") .place(x=170, y=730)
vehicle5MakeEntry = Entry(window, width=20, bg="white")
vehicle5MakeEntry.place(x=210, y=730)

Label(window, text="Model", background="black", fg="white") .place(x=340, y=730)
vehicle5ModelEntry = Entry(window, width=20, bg="white")
vehicle5ModelEntry.place(x=385, y=730)

Label(window, text="VIN", background="black", fg="white") .place(x=510, y=730)
vehicle5VINEntry = Entry(window, width=20, bg="white")
vehicle5VINEntry.place(x=535, y=730)

Financed5= IntVar()
Label(window, text="Financed", background="black", fg="white") .place(x=660, y=730)
Checkbutton(window, variable=Financed2, bg="black").place(x=710, y=730)

Leased5= IntVar()
Label(window, text="Leased", background="black", fg="white") .place(x=730, y=730)
Checkbutton(window, variable=Leased5, bg="black").place(x=770, y=730)

#Accidents
Label(window, text="Accident 1: Date", background="black", fg="white") .place(x=15, y=780)
accident1Entry = Entry(window, width=10, bg="white")
accident1Entry.place(x=110, y=780)

Label(window, text="Type Of Accident", background="black", fg="white") .place(x=175, y=780)
accident1TypeEntry = Entry(window, width=20, bg="white")
accident1TypeEntry.place(x=275, y=780)

Label(window, text="Driver", background="black", fg="white") .place(x=375, y=780)
accident1DriverEntry = Entry(window, width=20, bg="white")
accident1DriverEntry.place(x=415, y=780)

Label(window, text="PIP Claim", background="black", fg="white") .place(x=540, y=780)
accident1PIPEntry = Entry(window, width=20, bg="white")
accident1PIPEntry.place(x=595, y=780)

Label(window, text="Points DL", background="black", fg="white") .place(x=700, y=780)
accident1PointsOnLicenseEntry = Entry(window, width=5, bg="white")
accident1PointsOnLicenseEntry.place(x=760, y=780)

Label(window, text="Accident 2: Date", background="black", fg="white") .place(x=15, y=810)
accident2Entry = Entry(window, width=10, bg="white")
accident2Entry.place(x=110, y=810)

Label(window, text="Type Of Accident", background="black", fg="white") .place(x=175, y=810)
accident2TypeEntry = Entry(window, width=20, bg="white")
accident2TypeEntry.place(x=275, y=810)

Label(window, text="Driver", background="black", fg="white") .place(x=375, y=810)
accident2DriverEntry = Entry(window, width=20, bg="white")
accident2DriverEntry.place(x=415, y=810)

Label(window, text="PIP Claim", background="black", fg="white") .place(x=540, y=810)
accident2PIPEntry = Entry(window, width=20, bg="white")
accident2PIPEntry.place(x=595, y=810)

Label(window, text="Points DL", background="black", fg="white") .place(x=700, y=810)
accident2PointsOnLicenseEntry = Entry(window, width=5, bg="white")
accident2PointsOnLicenseEntry.place(x=760, y=810)

Label(window, text="Accident 3: Date", background="black", fg="white") .place(x=15, y=840)
accident3Entry = Entry(window, width=10, bg="white")
accident3Entry.place(x=110, y=840)

Label(window, text="Type Of Accident", background="black", fg="white") .place(x=175, y=840)
accident3TypeEntry = Entry(window, width=20, bg="white")
accident3TypeEntry.place(x=275, y=840)

Label(window, text="Driver", background="black", fg="white") .place(x=375, y=840)
accident3DriverEntry = Entry(window, width=20, bg="white")
accident3DriverEntry.place(x=415, y=840)

Label(window, text="PIP Claim", background="black", fg="white") .place(x=540, y=840)
accident3PIPEntry = Entry(window, width=20, bg="white")
accident3PIPEntry.place(x=595, y=840)

Label(window, text="Points DL", background="black", fg="white") .place(x=700, y=840)
accident3PointsOnLicenseEntry = Entry(window, width=5, bg="white")
accident3PointsOnLicenseEntry.place(x=760, y=840)

Label(window, text="Search: ", font=("Helvetica", 15), background="black", fg="white") .place(x=797, y=723)
clientSearchEntry = Entry(window,font=("Helvetica", 15), width=28, bg="white")
clientSearchEntry.place(x=872, y=725)

clientSearchEntry.bind("<KeyRelease>", Search)
#buttons
Button(window, text="QUOTE", padx=10, pady=5, fg="white", bg="#263D42", command=quote) .place(x=960, y=820)
SaveClient = tk.Button(window, text="Save Client", padx=10, pady=5, fg="white", bg="#263D42", command=Save).place(x=1000, y=770)
LoadClient = tk.Button(window, text="Load Client", padx=10, pady=5, fg="white", bg="#263D42", command=Load).place(x=900, y=770)

#connect.close()
#mainloop
window.mainloop()