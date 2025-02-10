from tkinter import ttk, messagebox, filedialog
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import os
import time
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
from io import BytesIO
import subprocess
import socket
import json
import mysql.connector as mysql
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


chrome_Options = Options()
chrome_Options.add_argument("--headless")
chrome_Options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
FILE_CHROME_PATH = r"chromedriver.exe"
CHROME_PATH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_Options.binary_location = CHROME_PATH

PATH = os.path.dirname(os.path.realpath(__file__))

CACHE = []

HEADER = 1024
PORT = 9316
SERVER = "104.136.118.185"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"


class socketConnection():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
    
    def requestResponse(self, msg):
        serverResponse = []
        if isinstance(msg, str):
            message = msg.encode(FORMAT)
        elif isinstance(msg, bytes):
            message = msg
        else:
            raise TypeError(f"Expected string or bytes, got {type(msg).__name__}")
        msgLength = len(message)
        sendLength = str(msgLength).encode(FORMAT)
        sendLength += b' ' * (HEADER - len(sendLength))
        self.client.sendall(sendLength)
        self.client.sendall(message)
        if msg != DISCONNECT_MESSAGE:
            from_server = self.client.recv(HEADER).decode(FORMAT)
            if from_server:
                
                serverResponse.append(from_server)
            return serverResponse
    
    def close(self):
        self.client.close()


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Cavalieri Management Tool - Beta")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.iconbitmap('property_manager_tool2.ico')
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.On_Closing)  # call .On_Closing() when app gets closed

        self.login_screen()


## screens
    def login_screen(self):
        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = customtkinter.CTkFrame(master=self)
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        

        # ============ main_frame ============

        # configure grid layout (3x7)
        self.main_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.main_frame.rowconfigure(7, weight=10)
        self.main_frame.columnconfigure((0, 1), weight=1)
        self.main_frame.columnconfigure(1, weight=0)

        
        # load image with PIL and convert to PhotoImage
        image = Image.open("logo.png").resize((int(self.WIDTH/2), int(self.HEIGHT/2)))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = customtkinter.CTkLabel(master=self.main_frame, text='', image=self.bg_image, bg_color="#292929")
        self.image_label.grid(column=1, row=0, sticky="nswe", padx=10, pady=20)

        # ============ main_frame ============

        self.user_entry = customtkinter.CTkEntry(master=self.main_frame,
                                            width=120,
                                            placeholder_text="Username")
        self.user_entry.grid(row=7, column=1, columnspan=1, pady=20, padx=20, sticky="we")

        
        self.password_entry = customtkinter.CTkEntry(master=self.main_frame,
                                            width=120,
                                            placeholder_text="Password",
                                            show="*")
        self.password_entry.grid(row=8, column=1, columnspan=1, pady=20, padx=20, sticky="we")

        self.login_button = customtkinter.CTkButton(master=self.main_frame,
                                                text="Login",
                                                command=self.Login)
        self.login_button.grid(row=7, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        
        self.forgotPassword_button = customtkinter.CTkButton(master=self.main_frame,
                                                text="forgot password?",
                                                command=self.ForgotPassword)
        self.forgotPassword_button.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        self.darkmode_switch = customtkinter.CTkSwitch(master=self.main_frame,
                                                text="Dark Mode",
                                                command=self.ChangeMode)
        self.darkmode_switch.grid(row=8, column=0, columnspan=1, pady=20, padx=20, sticky="we")
        
        if customtkinter.get_appearance_mode() == "Dark":
            self.darkmode_switch.select()

    def logged_screen(self):
        self.logged_frame = customtkinter.CTkFrame(master=self)
        self.logged_frame.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.addProductWindow = None
        self.productListWindow = None
        self.productSelected = None
        self.generateListWindow = None
        
        # configure grid layout (3x7)
        self.logged_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.logged_frame.rowconfigure(7, weight=10)
        self.logged_frame.columnconfigure((0, 1), weight=1)
        self.logged_frame.columnconfigure(1, weight=0)

        self.clientListFrame = customtkinter.CTkFrame(self.logged_frame)
        self.clientListFrame.place(relwidth=0.257, relheight=0.64, x=520,y=110)
        self.clientListScrollBar = Scrollbar(self.clientListFrame, orient=VERTICAL)

        self.clientList = Listbox(self.logged_frame, yscrollcommand=self.clientListScrollBar.set, bg="#3d3d3d", fg='silver', border=0)
        self.clientList.place(relwidth=0.247, relheight=0.64, x=510,y=110)
        self.clientListScrollBar.configure(command=self.clientList.yview)
        self.clientListScrollBar.pack(side=RIGHT, fill=Y)

        self.clientTable = [
           ["Juan"],
           ["Felipe"],
           ["Joao"],
           ["Pedro"],
           ["Bruno"],
           ["Ariel"],
           ["Caio"],
           ["Wesley"],
           ["Weslei"],
           ["Juan"],
           ["Juan"],
           ["Oracio"],
           ["Juan"],
           ["Ricardo"],
           ["Phelippe"],
           ["Juan"],
           ["Juan"],
           ["Ariel"],
           ["Wesley"],
           ["Bruno"],
           ["Ricardo"],
           ["Juan"],
           ["Juan"],
           ["Oracio"],
        ]

        for client in self.clientTable:
            self.clientList.insert(END, client)

        self.clientList.bind("<Double-Button-1>", self.load_selected_client)
        self.clientName_Label = customtkinter.CTkLabel(master=self.logged_frame, text="Client Name:", font=("Arial",12))
        self.clientName_Label.grid(row=2, column=0, pady=20, padx=5, sticky="w")

        
        self.clientName_result_Label = customtkinter.CTkLabel(master=self.logged_frame, text="", font=("Arial",12))
        self.clientName_result_Label.grid(row=2, column=0, pady=20, padx=120, sticky="w")

        self.clientSearch_entry = customtkinter.CTkEntry(master=self.logged_frame,
                                            width=100,
                                            placeholder_text="Search Client")
        self.clientSearch_entry.grid(row=8, column=1, columnspan=2, pady=20, padx=30, sticky="we")
        
        self.clientSearch_entry.bind("<KeyRelease>", self.Client_Search)

        self.darkmode_switch = customtkinter.CTkSwitch(master=self.logged_frame,
                                                text="Dark Mode",
                                                command=self.ChangeMode)
        self.darkmode_switch.grid(row=8, column=0, columnspan=1, pady=20, padx=20, sticky="w")

        if customtkinter.get_appearance_mode() == "Dark":
            self.darkmode_switch.select()
        else:
            self.clientList.configure(bg="white")

        self.clock_label = customtkinter.CTkLabel(master=self.logged_frame, font=("Helvetica", 15))
        self.clock_label.grid(column=2, row=0, sticky="ne", padx=10, pady=15)

        self.timeInAndOut_label = customtkinter.CTkLabel(master=self.logged_frame, font=("Helvetica", 15), text="")
        self.timeInAndOut_label.place(x=610,y=55)
        
        #TKbuttons
        self.clockIn_button = customtkinter.CTkButton(master=self.logged_frame,
                                                text="Clock In",
                                                command=self.ClockIn)
        self.clockIn_button.grid(column=1, row=0, pady=15, sticky="ne")
        
        self.clockOut_button = customtkinter.CTkButton(master=self.logged_frame,
                                                text="Clock Out",
                                                command=self.ClockOut)
        self.clockOut_button.grid(column=1, row=0, pady=15, sticky="ne")
        self.clockOut_button.grid_forget()
        
        self.Logout_button = customtkinter.CTkButton(master=self.logged_frame,
                                                text="Logout",
                                                command=self.Logout)
        self.Logout_button.grid(column=0, row=0, pady=15, padx=15, sticky="nw")
        
        self.AdminPanel_button = customtkinter.CTkButton(master=self.logged_frame,
                                                text="Admin Panel",
                                                command=self.AdminPanel)
        self.AdminPanel_button.grid(column=0, row=0, pady=15, padx=45, sticky="ne")
        
        self.Inventory_button = customtkinter.CTkButton(master=self.logged_frame,
                                                text="Inventory List",
                                                command=self.productList)
        self.Inventory_button.grid(column=0, row=0, pady=15, padx=30, sticky="n")
        #call Functions
        self.Clock()

# usefull functions
    def On_Closing(self, event=0):
        self.destroy()

    def ChangeMode(self):
        if self.darkmode_switch.get() == 1:
            customtkinter.set_appearance_mode("dark")
            try:
                self.image_label.configure(bg="#292929")
            except:
                self.clientList.configure(bg="#3d3d3d")
        else:
            customtkinter.set_appearance_mode("light")
            try:
                self.image_label.configure(bg="#e3e4e5")
            except:
                self.clientList.configure(bg="white")

    def Start(self):
        self.mainloop()

    def Clock(self):
        hour = time.strftime("%H")
        minute = time.strftime("%M")
        second = time.strftime("%S")

        self.clock_label.configure(text=f"{hour}:{minute}:{second}")
        self.clock_label.after(1000, self.Clock)

    def productUpdate(self, data):  
        for deleteproduct in self.product_tree.get_children():
            self.product_tree.delete(deleteproduct)
            
        print("data=",data)
        for product in data:
            print("product=",product)
            if product['Material'] == 'vinyl':
                self.product_tree.insert("", "end", values=(product['Product'], product['Size'], product['Thickness'], product['Wear Layer'], product['Brand'], product['SKU'], product['Sqft/Box'], product['Pc/Box'], product['Box/Pallet'], product['Lbs/Box'], product['Dealer Price'], product['Retail Price'], product['Box_In_Stock'], product['Material'], product['Color Group'], product['image_link']))
            elif product['Material'] == 'laminate':
                self.product_tree.insert("", "end", values=(product['Product'], product['Size'], product['Thickness'], product['Brand'], product['SKU'], product['Sqft/Box'], product['Pc/Box'], product['Box/Pallet'], product['Lbs/Box'], product['Dealer Price'], product['Retail Price'], product['Box_In_Stock'], product['Material'], product['Color Group'], product['image_link']))
            elif product['Material'] == 'tile':
                self.product_tree.insert("", "end", values=(product['Product'], product['Size'], product['Finish'], product['Brand'], product['SKU'], product['Sqft/Box'], product['Pc/Box'], product['Box/Pallet'], product['Lbs/Box'], product['Dealer Price'], product['Retail Price'], product['Box_In_Stock'], product['Material'], product['Color Group', product['image_link']]))
            elif product['Material'] == 'hardwood':
                self.product_tree.insert("", "end", values=(product['Product'], product['Size'], product['Thickness'], product['Finish'], product['Brand'], product['SKU'], product['Sqft/Box'], product['Pc/Box'], product['Box/Pallet'], product['Lbs/Box'], product['Dealer Price'], product['Retail Price'], product['Box_In_Stock'], product['Material'], product['Color Group', product['image_link']]))
            elif product['Material'] == 'carpet':
                self.product_tree.insert("", "end", values=(product['Product'], product['Size'], product['Thickness'], product['Wear Layer'], product['Finish'], product['Brand'], product['SKU'], product['Sqft/Box'], product['Pc/Box'], product['Box/Pallet'], product['Lbs/Box'], product['Dealer Price'], product['Retail Price'], product['Box_In_Stock'], product['Material'], product['Color Group', product['image_link']]))
            elif product['Material'] == 'mosaic':
                self.product_tree.insert("", "end", values=(product['Product'], product['Size'], product['Finish'], product['Brand'], product['SKU'], product['Sqft/Box'], product['Pc/Box'], product['Box/Pallet'], product['Lbs/Box'], product['Dealer Price'], product['Retail Price'], product['Box_In_Stock'], product['Material'], product['Color Group', product['image_link']]))
            else:
                self.product_tree.insert("", "end", values=(product['Product'], product['Size'], product['Thickness'], product['Wear Layer'], product['Finish'], product['Brand'], product['SKU'], product['Sqft/Box'], product['Pc/Box'], product['Box/Pallet'], product['Lbs/Box'], product['Dealer Price'], product['Retail Price'], product['Box_In_Stock'], product['Material'], product['Color Group'], product['image_link']))

    def fetchProductsFromDatabase(self,material):
        inventory_size = self.getSocketDataInventorySize(f"getSizeInventory,m,{material}")
        for i in range(int(inventory_size)):
            data = self.getSocketData(f"getInventory,{i+1},'all'")
            if not str(data) == 'denied':
                db_data = json.loads(data)
                CACHE.append(db_data)
                if db_data['Material'] == 'vinyl':
                    self.product_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['Thickness'], db_data['Wear Layer'], db_data['Brand'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock'], db_data['Material'], db_data['Color Group'], db_data['image_link']))
                elif db_data['Material'] == 'laminate':
                    self.product_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['Thickness'], db_data['Brand'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock'], db_data['Material'], db_data['Color Group'], db_data['image_link']))
                elif material == 'tile':
                    self.product_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['Finish'], db_data['Brand'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock'], db_data['Material'], db_data['Color Group'], db_data['image_link']))
                elif db_data['Material'] == 'hardwood':
                    self.product_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['Thickness'], db_data['Finish'], db_data['Brand'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock'], db_data['Material'], db_data['Color Group'], db_data['image_link']))
                elif db_data['Material'] == 'carpet':
                    self.product_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['Thickness'], db_data['Wear Layer'], db_data['Finish'], db_data['Brand'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock'], db_data['Material'], db_data['Color Group'], db_data['image_link']))
                elif db_data['Material'] == 'mosaic':
                    self.product_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['Thickness'], db_data['Wear Layer'], db_data['Finish'], db_data['Brand'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock'], db_data['Material'], db_data['Color Group'], db_data['image_link']))
                else:
                    self.product_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['Thickness'], db_data['Wear Layer'], db_data['Finish'], db_data['Brand'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock'], db_data['Material'], db_data['Color Group'], db_data['image_link']))
        
    def productSearch(self, search):
        searched = self.product_search_entry.get()
        material = self.searchMaterial.get().lower()
        self.packTreeBy(material)

        print("cache:", len(CACHE))
        if len(CACHE) == 0:
            Thread(target = self.fetchProductsFromDatabase, args = (material,)).start() 
        products = CACHE
        if searched == '':
            data = []
            for product in products:
                if product['Material'] == material:
                    data.append(product)
        else:
            data = []
            
            for product in products:
                if product['Material'] == 'vinyl':
                    if self.searchproductBy.get() == "Product":
                        productFound = product['Product']
                    elif self.searchproductBy.get() == "Size":
                        productFound = product['Size']
                    elif self.searchproductBy.get() == "Thickness":
                        productFound = product['Thickness']
                    elif self.searchproductBy.get() == "Wear Layer":
                        productFound = product['Wear Layer']
                    elif self.searchproductBy.get() == "Brand":
                        productFound = product['Brand']    
                    elif self.searchproductBy.get() == "SKU":
                        productFound = product['SKU']
                    elif self.searchproductBy.get() == "Sqft/Box":
                        productFound = product['Sqft/Box']
                    elif self.searchproductBy.get() == "Pc/Box":
                        productFound = product['Pc/Box']
                    elif self.searchproductBy.get() == "Box/Pallet":
                        productFound = product['Box/Pallet']
                    elif self.searchproductBy.get() == "Lbs/Box":
                        productFound = product['Lbs/Box']
                    elif self.searchproductBy.get() == "Dealer Price":
                        productFound = product['Dealer Price']
                    elif self.searchproductBy.get() == "Retail Price":
                        productFound = product['Retail Price']
                    elif self.searchproductBy.get() == "Box In Stock":
                        productFound = product['Box In Stock']    
                    elif self.searchproductBy.get() == "Material":
                        productFound = product['Material']    
                    elif self.searchproductBy.get() == "Color Group":
                        productFound = product['Color Group']    
                    elif self.searchproductBy.get() == "image_link":
                        productFound = product['image_link']    
                    if searched.lower() in productFound.lower():                    
                        data.append(product)
                elif product['Material'] == 'laminate':
                    if self.searchproductBy.get() == "Product":
                        productFound = product['Product']
                    elif self.searchproductBy.get() == "Size":
                        productFound = product['Size']
                    elif self.searchproductBy.get() == "Thickness":
                        productFound = product['Thickness']
                    elif self.searchproductBy.get() == "Brand":
                        productFound = product['Brand']    
                    elif self.searchproductBy.get() == "SKU":
                        productFound = product['SKU']
                    elif self.searchproductBy.get() == "Sqft/Box":
                        productFound = product['Sqft/Box']
                    elif self.searchproductBy.get() == "Pc/Box":
                        productFound = product['Pc/Box']
                    elif self.searchproductBy.get() == "Box/Pallet":
                        productFound = product['Box/Pallet']
                    elif self.searchproductBy.get() == "Lbs/Box":
                        productFound = product['Lbs/Box']
                    elif self.searchproductBy.get() == "Dealer Price":
                        productFound = product['Dealer Price']
                    elif self.searchproductBy.get() == "Retail Price":
                        productFound = product['Retail Price']
                    elif self.searchproductBy.get() == "Box In Stock":
                        productFound = product['Box In Stock']    
                    elif self.searchproductBy.get() == "Material":
                        productFound = product['Material']    
                    elif self.searchproductBy.get() == "Color Group":
                        productFound = product['Color Group']    
                    if searched.lower() in productFound.lower():                    
                        data.append(product)
                else:
                    if self.searchproductBy.get() == "Product":
                        productFound = product['Product']
                    elif self.searchproductBy.get() == "Size":
                        productFound = product['Size']
                    elif self.searchproductBy.get() == "Thickness":
                        productFound = product['Thickness']
                    elif self.searchproductBy.get() == "Wear Layer":
                        productFound = product['Wear Layer']    
                    elif self.searchproductBy.get() == "Finish":
                        productFound = product['Finish']    
                    elif self.searchproductBy.get() == "Brand":
                        productFound = product['Brand']    
                    elif self.searchproductBy.get() == "SKU":
                        productFound = product['SKU']
                    elif self.searchproductBy.get() == "Sqft/Box":
                        productFound = product['Sqft/Box']
                    elif self.searchproductBy.get() == "Pc/Box":
                        productFound = product['Pc/Box']
                    elif self.searchproductBy.get() == "Box/Pallet":
                        productFound = product['Box/Pallet']
                    elif self.searchproductBy.get() == "Lbs/Box":
                        productFound = product['Lbs/Box']
                    elif self.searchproductBy.get() == "Dealer Price":
                        productFound = product['Dealer Price']
                    elif self.searchproductBy.get() == "Retail Price":
                        productFound = product['Retail Price']
                    elif self.searchproductBy.get() == "Box In Stock":
                        productFound = product['Box In Stock']    
                    elif self.searchproductBy.get() == "Material":
                        productFound = product['Material']    
                    elif self.searchproductBy.get() == "Color Group":
                        productFound = product['Color Group']    
                    if searched.lower() in productFound.lower():                    
                        data.append(product)

        
        self.productUpdate(data)

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: \
            self.treeview_sort_column(tv, col, not reverse))

    def Client_Update(self, data):  
        self.clientList.delete(0, END)

        for client in data:
            self.clientList.insert(END, client)

    def Client_Search(self, search):
        searched = self.clientSearch_entry.get()

        if searched == '':
            data = []
            for client in self.clientTable:
                client_string = str(client).split("'")[1]
                data.append(client_string)
        else:
            data = []
            for client in self.clientTable:
                client_string = str(client).split("'")[1]
                if searched.lower() in client_string.lower():
                    data.append(client_string)

        self.Client_Update(sorted(data))


    def load_selected_client(self, event):
        loadedClient = self.clientList.get(self.clientList.curselection())
        try:
            client = str(loadedClient).split("'")[1]
        except:
            client = loadedClient
            
        self.clientName_result_Label.configure(text=str(client))
        
    def getSocketData(self, msg): 
        conn = socketConnection()
        response = conn.requestResponse(msg)[0]
        conn.requestResponse(DISCONNECT_MESSAGE)
        return response

    def getSocketDataInventorySize(self, msg): 
        conn = socketConnection()
        response = conn.requestResponse(msg)[0]
        conn.requestResponse(DISCONNECT_MESSAGE)
        return response

#buttons

    def ClockIn(self):
        self.clockIn_button.grid_forget()
        self.clockOut_button.grid(column=1, row=0, pady=15, sticky="ne")
        
        self.timeInAndOut_label.configure(text=time.strftime('%H:%M:%S'), bg_color="green")
        
    def ClockOut(self):
        self.clockOut_button.grid_forget()
        self.clockIn_button.grid(column=1, row=0, pady=15, sticky="ne")
        self.timeInAndOut_label.configure(text=time.strftime('%H:%M:%S'), bg_color="red")

    def Logout(self):
        self.logged_frame.destroy()
        self.login_screen()

    def Login(self):
        print(self.user_entry.get())
        print(self.password_entry.get())
        self.main_frame.destroy()
        self.logged_screen()
        
    def ForgotPassword(self):
        print("ForgotPassword Button pressed")

    def AdminPanel(self):
        self.AdminPanelWindow = customtkinter.CTkToplevel(self)
        self.AdminPanelWindow.title("Admin Panel")
        self.AdminPanelWindow.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.AdminPanelWindow.iconbitmap('property_manager_tool2.ico')
        self.AdminPanelWindow.minsize(App.WIDTH, App.HEIGHT)
        self.AdminPanelWindow.maxsize(App.WIDTH, App.HEIGHT)
        
        self.AdminPanel_frame = customtkinter.CTkFrame(master=self.AdminPanelWindow)
        self.AdminPanel_frame.pack(side="top", padx=20, pady=40, fill="both", expand=True)
        
        self.productName_entry = customtkinter.CTkEntry(master=self.AdminPanel_frame,
                                            width=150,
                                            placeholder_text="Todo")
        self.productName_entry.place(x=20,y=20)
        
        self.addProduct_button = customtkinter.CTkButton(master=self.AdminPanelWindow,
                                                text="Create User",
                                                command=self.addProduct)
        self.addProduct_button.place(x=50,y=5)
        
        self.addProduct_button = customtkinter.CTkButton(master=self.AdminPanelWindow,
                                                text="Manage Users",
                                                command=self.addProduct)
        self.addProduct_button.place(x=230,y=5)
        
        self.addProduct_button = customtkinter.CTkButton(master=self.AdminPanelWindow,
                                                text="Create Client",
                                                command=self.addProduct)
        self.addProduct_button.place(x=410,y=5)
        
        self.addProduct_button = customtkinter.CTkButton(master=self.AdminPanelWindow,
                                                text="Manage Clients",
                                                command=self.addProduct)
        self.addProduct_button.place(x=590,y=5)
            
    def AddToDatabase(self):
        image_links = f"{self.productSampleImg_entry.get()},{self.productRoomImg_entry.get()}"
        msg = [
            self.productName_entry.get(),
            self.productSize_entry.get(),
            self.productThickness_entry.get(),
            self.productWearLayer_entry.get(),
            self.productFinish_entry.get(),
            self.productBrand_entry.get(),
            self.productSku_entry.get(),
            self.productSqftbox_entry.get(),
            self.productPcbox_entry.get(),
            self.productBoxpallet_entry.get(),
            self.productLbsbox_entry.get(),
            self.productDealerprice_entry.get(),
            self.productRetailprice_entry.get(),
            self.productBoxInStock_entry.get(),
            self.productMaterial_entry.get(),
            self.productColorGroup_entry.get(),
            image_links
        ]
        conn = socketConnection()
        conn.requestResponse(f"addProduct,{msg}")
        conn.requestResponse(DISCONNECT_MESSAGE)
        CACHE.clear()
        self.productSearch('n')
        
    def addProduct(self):
        if self.addProductWindow is None or not self.addProductWindow.winfo_exists():
            self.addProductWindow = customtkinter.CTkToplevel(self)
            self.addProductWindow.title("Add Product")
            self.addProductWindow.geometry("400x500")
            self.addProductWindow.iconbitmap('property_manager_tool2.ico')
            self.addProductWindow.minsize(400, 500)
            self.addProductWindow.maxsize(400, 500)
            
            self.product_frame = customtkinter.CTkFrame(master=self.addProductWindow)
            self.product_frame.pack(side="top", padx=20, pady=40, fill="both", expand=True)
            
            self.productName_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Product")
            self.productName_entry.place(x=20,y=20)
            
            self.productSize_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Size")
            self.productSize_entry.place(x=20,y=60)
            
            self.productSku_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="SKU")
            self.productSku_entry.place(x=20,y=100)
            
            self.productSqftbox_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Sqft/Box")
            self.productSqftbox_entry.place(x=20,y=140)
            self.productPcbox_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Pc/Box")
            self.productPcbox_entry.place(x=20,y=180)
            
            self.productThickness_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Thickness")
            self.productThickness_entry.place(x=20,y=220)
            
            self.productFinish_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Finish")
            self.productFinish_entry.place(x=20,y=260)
            
            self.productBrand_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Brand")
            self.productBrand_entry.place(x=20,y=300)
            
            self.productSampleImg_entry = customtkinter.CTkEntry(master=self.product_frame,
                                      width=150,
                                      placeholder_text="Sample Image Link")
            self.productSampleImg_entry.place(x=20,y=340)
            
            self.productBoxpallet_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Box/Pallet")
            self.productBoxpallet_entry.place(x=200,y=20)
            
            self.productLbsbox_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Lbs/Box")
            self.productLbsbox_entry.place(x=200,y=60)
            
            self.productDealerprice_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Dealer Price")
            self.productDealerprice_entry.place(x=200,y=100)
            self.productRetailprice_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Retail Price")
            self.productRetailprice_entry.place(x=200,y=140)
            
            self.productBoxInStock_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Box In Stock")
            self.productBoxInStock_entry.place(x=200,y=180)
            
            self.productWearLayer_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Wear Layer")
            self.productWearLayer_entry.place(x=200,y=220)
            
            self.productMaterial_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Material")
            self.productMaterial_entry.place(x=200,y=260)
            
            self.productColorGroup_entry = customtkinter.CTkEntry(master=self.product_frame,
                                                width=150,
                                                placeholder_text="Color Group")
            self.productColorGroup_entry.place(x=200,y=300)

            self.productRoomImg_entry = customtkinter.CTkEntry(master=self.product_frame,
                                      width=150,
                                      placeholder_text="Room Image Link")
            self.productRoomImg_entry.place(x=200,y=340)
            
            
            self.add_button = customtkinter.CTkButton(master=self.product_frame,
                                                    text="Add",
                                                    command=self.AddToDatabase)
            self.add_button.place(x=115,y=380)
            self.addProductWindow.focus()
            # create window if its None or destroyed
        else:
            self.addProductWindow.focus()  # if window exists focus it

    def generateList(self):
        if self.generateListWindow is None or not self.generateListWindow.winfo_exists():
            self.generateListWindow = customtkinter.CTkToplevel(self)
            self.generateListWindow.title("Generated List")
            self.generateListWindow.geometry(f"{App.WIDTH}x{App.HEIGHT}")
            self.generateListWindow.iconbitmap('property_manager_tool2.ico')
            self.generateListWindow.minsize(App.WIDTH, App.HEIGHT)
            self.generateListWindow.maxsize(App.WIDTH+140, App.HEIGHT+260)

            # Create the canvas
            self.generateList_canvas = customtkinter.CTkCanvas(master=self.generateListWindow)
            self.generateList_canvas.grid(row=0, column=0, pady=20, padx=5, sticky="nsew")

            # Create a scrollbar
            self.generateListScrollBar = customtkinter.CTkScrollbar(master=self.generateListWindow, orientation="vertical")
            self.generateListScrollBar.grid(row=0, column=1, sticky="ns")
            self.generateListScrollBar.configure(command=self.generateList_canvas.yview)
            self.generateList_canvas.configure(yscrollcommand=self.generateListScrollBar.set)

            # Configure the row and column weights to ensure expansion
            self.generateListWindow.grid_rowconfigure(0, weight=1)
            self.generateListWindow.grid_columnconfigure(0, weight=1)

            # Create a frame inside the canvas
            self.generateList_frame = customtkinter.CTkFrame(master=self.generateList_canvas)
            
            # Add the frame to the canvas
            self.generateList_canvas.create_window((0, 0), window=self.generateList_frame, anchor="center")

            # Update the scrollregion to encompass the frame
            def update_scroll_region(event):
                self.generateList_canvas.config(scrollregion=self.generateList_canvas.bbox("all"))

            self.generateList_frame.bind("<Configure>", update_scroll_region)
            

            def load_images(none):
                def next_photo():
                    first_room_label.grid_forget()
                    second_room_label = customtkinter.CTkLabel(master=generate_frame, text='', image=second_image_load)
                    second_room_label.grid(column=0, row=0, sticky="nswe", padx=20, pady=20)
                    PreviousButton = customtkinter.CTkButton(master=generate_frame, text="Previous", width=60,command=previous_photo)
                    PreviousButton.grid(column=0, row=0, sticky="w", padx=20, pady=20)
                    NextButton.grid_forget()
                    
                def previous_photo():
                    second_room_label.grid_forget()
                    first_room_label = customtkinter.CTkLabel(master=generate_frame, text='', image=first_image_load)
                    first_room_label.grid(column=0, row=0, sticky="nswe", padx=20, pady=20)
                    NextButton = customtkinter.CTkButton(master=generate_frame, text="Next", width=60,command=next_photo)
                    NextButton.grid(column=0, row=0, sticky="e", padx=20, pady=20)
                    PreviousButton.grid_forget()
                    
                row = 0
                column = 0
                for selectedProduct in self.product_tree.get_children():
                    generate_frame = customtkinter.CTkFrame(master=self.generateList_frame)
                    generate_frame.grid(row=row, column=column, pady=20, padx=5, sticky="nsew")
                    
                    try:
                        split_link = self.product_tree.item(selectedProduct)["values"][15].split(',')
                        image_of_sample = requests.get(split_link[0])
                        image_of_room = requests.get(split_link[1])
                        first_image = Image.open(BytesIO(image_of_sample.content)).resize((int(App.WIDTH/2), int(App.HEIGHT)))
                        first_image_load = ImageTk.PhotoImage(first_image)
                        second_image = Image.open(BytesIO(image_of_room.content)).resize((int(App.WIDTH/2), int(App.HEIGHT)))
                        second_image_load = ImageTk.PhotoImage(second_image)

                    except:
                        split_link = self.product_tree.item(selectedProduct)["values"][14].split(',')
                        image_of_sample = requests.get(split_link[0])
                        image_of_room = requests.get(split_link[1])
                        first_image = Image.open(BytesIO(image_of_sample.content)).resize((int(App.WIDTH/2), int(App.HEIGHT)))
                        first_image_load = ImageTk.PhotoImage(first_image)
                        second_image = Image.open(BytesIO(image_of_room.content)).resize((int(App.WIDTH/2), int(App.HEIGHT)))
                        second_image_load = ImageTk.PhotoImage(second_image)

                    
                    first_room_label = customtkinter.CTkLabel(master=generate_frame, text='', image=first_image_load)
                    first_room_label.grid(column=0, row=0, columnspan=1, sticky="nswe", padx=20, pady=20)
                    
                    second_room_label = customtkinter.CTkLabel(master=generate_frame, text='', image=second_image_load)
                    second_room_label.grid_forget()
    
                    NextButton = customtkinter.CTkButton(master=generate_frame, text="Next", width=60,command=lambda i=row: next_photo)
                    #NextButton.grid(column=0, row=0, sticky="e", padx=20, pady=20)
                    NextButton.grid_forget()

                    PreviousButton = customtkinter.CTkButton(master=generate_frame, text="Previous", width=60,command=lambda i=row: previous_photo)
                    PreviousButton.grid_forget()

                    product_name = f'{self.product_tree.item(selectedProduct)["values"][0]} - {self.product_tree.item(selectedProduct)["values"][5]}'
                    product_size = self.product_tree.item(selectedProduct)["values"][1]
                    product_Thickness = f'{self.product_tree.item(selectedProduct)["values"][2]}mm'
                    product_Wear_Layer = f'{self.product_tree.item(selectedProduct)["values"][3]}mil'
                    product_price = self.product_tree.item(selectedProduct)["values"][11]
                    self.image_label = customtkinter.CTkLabel(master=generate_frame, text=product_name)
                    self.image_label.grid(column=0, row=1, columnspan=1, sticky="n", padx=0, pady=0)
                    self.image_label = customtkinter.CTkLabel(master=generate_frame, text=product_size)
                    self.image_label.grid(column=0, row=1, columnspan=1, sticky="n", padx=0, pady=20)
                    self.image_label = customtkinter.CTkLabel(master=generate_frame, text=product_Thickness)
                    self.image_label.grid(column=0, row=1, sticky="nw", padx=180, pady=40)
                    self.image_label = customtkinter.CTkLabel(master=generate_frame, text=product_Wear_Layer)
                    self.image_label.grid(column=0, row=1, sticky="ne", padx=180, pady=40)
                    self.image_label = customtkinter.CTkLabel(master=generate_frame, text=product_price)
                    self.image_label.grid(column=0, row=1, columnspan=1, sticky="n", padx=0, pady=60)
                    
                    if column == 0:
                        column = 1
                    else:
                        column = 0
                        row = row+1
                        
            Thread(target = load_images, args = ("none",)).start()
            
            self.generateListWindow.focus()
            # create window if its None or destroyed
        else:
            self.generateListWindow.focus()  # if window exists focus it

    def packTreeBy(self, material):
        if material == 'vinyl':
            choices = ['Product', 'Size', 'Thickness', 'Wear Layer', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group']
            self.searchproductBy.configure(value=choices)

            self.product_tree['columns'] = ('Product', 'Size', 'Thickness', 'Wear Layer', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group', 'image_link')
            #formate treeview columns
            self.product_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
            self.product_tree.column("Product", width=200, minwidth=100, anchor="n")
            self.product_tree.column("Size", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Thickness", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Wear Layer", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Brand", width=100, minwidth=100, anchor="n")
            self.product_tree.column("SKU", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Sqft/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Pc/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Box/Pallet", width=60, minwidth=60, anchor="n")
            self.product_tree.column("Lbs/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Dealer Price", width=0, minwidth=0, stretch=NO, anchor="n") #80
            self.product_tree.column("Retail Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Box In Stock", width=90, minwidth=90, anchor="n")
            self.product_tree.column("Material", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Color Group", width=50, minwidth=50, anchor="n")
            self.product_tree.column("image_link", width=0, minwidth=0, stretch=NO, anchor="n")
            
            self.product_tree.heading("#0", anchor="w")
            self.product_tree.heading("Product", text="Product", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Product", False))
            self.product_tree.heading("Size", text="Size", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Size", False))
            self.product_tree.heading("Thickness", text="Thickness", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Thickness", False))
            self.product_tree.heading("Wear Layer", text="Wear Layer", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Wear Layer", False))
            self.product_tree.heading("Brand", text="Brand", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Brand", False))
            self.product_tree.heading("SKU", text="SKU", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "SKU", False))
            self.product_tree.heading("Sqft/Box", text="Sqft/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Sqft/Box", False))
            self.product_tree.heading("Pc/Box", text="Pc/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Pc/Box", False))
            self.product_tree.heading("Box/Pallet", text="Box/Pallet", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box/Pallet", False))
            self.product_tree.heading("Lbs/Box", text="Lbs/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Lbs/Box", False))
            self.product_tree.heading("Dealer Price", text="Dealer Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Dealer Price", False))
            self.product_tree.heading("Retail Price", text="Retail Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Retail Price", False))
            self.product_tree.heading("Box In Stock", text="Box In Stock", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box In Stock", False))
            self.product_tree.heading("Material", text="Material", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Material", False))
            self.product_tree.heading("Color Group", text="Color Group", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Color Group", False))    
            self.product_tree.heading("image_link", text="image_link", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "image_link", False))    
        elif material == 'laminate':
            choices = ['Product', 'Size', 'Thickness', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group']
            self.searchproductBy.configure(value=choices)

            self.product_tree['columns'] = ('Product', 'Size', 'Thickness', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group', 'image_link')

            #formate treeview columns
            self.product_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
            self.product_tree.column("Product", width=200, minwidth=100, anchor="n")
            self.product_tree.column("Size", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Thickness", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Brand", width=100, minwidth=100, anchor="n")
            self.product_tree.column("SKU", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Sqft/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Pc/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Box/Pallet", width=60, minwidth=60, anchor="n")
            self.product_tree.column("Lbs/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Dealer Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Retail Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Box In Stock", width=90, minwidth=90, anchor="n")
            self.product_tree.column("Material", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Color Group", width=50, minwidth=50, anchor="n")
            self.product_tree.column("image_link", width=0, minwidth=0, stretch=NO, anchor="n")
            
            self.product_tree.heading("#0", anchor="w")
            self.product_tree.heading("Product", text="Product", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Product", False))
            self.product_tree.heading("Size", text="Size", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Size", False))
            self.product_tree.heading("Thickness", text="Thickness", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Thickness", False))
            self.product_tree.heading("Brand", text="Brand", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Brand", False))
            self.product_tree.heading("SKU", text="SKU", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "SKU", False))
            self.product_tree.heading("Sqft/Box", text="Sqft/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Sqft/Box", False))
            self.product_tree.heading("Pc/Box", text="Pc/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Pc/Box", False))
            self.product_tree.heading("Box/Pallet", text="Box/Pallet", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box/Pallet", False))
            self.product_tree.heading("Lbs/Box", text="Lbs/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Lbs/Box", False))
            self.product_tree.heading("Dealer Price", text="Dealer Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Dealer Price", False))
            self.product_tree.heading("Retail Price", text="Retail Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Retail Price", False))
            self.product_tree.heading("Box In Stock", text="Box In Stock", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box In Stock", False))
            self.product_tree.heading("Material", text="Material", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Material", False))
            self.product_tree.heading("Color Group", text="Color Group", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Color Group", False))
            self.product_tree.heading("image_link", text="image_link", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "image_link", False))   
        elif material == 'tile':
            choices = ['Product', 'Size', 'Finish', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group']
            self.searchproductBy.configure(value=choices)


            self.product_tree['columns'] = ('Product', 'Size', 'Finish', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group', 'image_link')

            #formate treeview columns
            self.product_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
            self.product_tree.column("Product", width=200, minwidth=100, anchor="n")
            self.product_tree.column("Size", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Finish", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Brand", width=100, minwidth=100, anchor="n")
            self.product_tree.column("SKU", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Sqft/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Pc/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Box/Pallet", width=60, minwidth=60, anchor="n")
            self.product_tree.column("Lbs/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Dealer Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Retail Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Box In Stock", width=90, minwidth=90, anchor="n")
            self.product_tree.column("Material", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Color Group", width=50, minwidth=50, anchor="n")
            self.product_tree.column("image_link", width=0, minwidth=0, stretch=NO, anchor="n")
            
            self.product_tree.heading("#0", anchor="w")
            self.product_tree.heading("Product", text="Product", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Product", False))
            self.product_tree.heading("Size", text="Size", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Size", False))
            self.product_tree.heading("Finish", text="Finish", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Finish", False))
            self.product_tree.heading("Brand", text="Brand", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Brand", False))
            self.product_tree.heading("SKU", text="SKU", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "SKU", False))
            self.product_tree.heading("Sqft/Box", text="Sqft/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Sqft/Box", False))
            self.product_tree.heading("Pc/Box", text="Pc/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Pc/Box", False))
            self.product_tree.heading("Box/Pallet", text="Box/Pallet", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box/Pallet", False))
            self.product_tree.heading("Lbs/Box", text="Lbs/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Lbs/Box", False))
            self.product_tree.heading("Dealer Price", text="Dealer Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Dealer Price", False))
            self.product_tree.heading("Retail Price", text="Retail Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Retail Price", False))
            self.product_tree.heading("Box In Stock", text="Box In Stock", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box In Stock", False))
            self.product_tree.heading("Material", text="Material", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Material", False))
            self.product_tree.heading("Color Group", text="Color Group", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Color Group", False))
            self.product_tree.heading("image_link", text="image_link", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "image_link", False))   
        elif material == 'hardwood':
            self.searchproductBy.configure(value=choices)


            self.product_tree['columns'] = ('Product', 'Size', 'Thickness', 'Finish', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group', 'image_link')

            #formate treeview columns
            self.product_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
            self.product_tree.column("Product", width=200, minwidth=100, anchor="n")
            self.product_tree.column("Size", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Thickness", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Finish", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Brand", width=100, minwidth=100, anchor="n")
            self.product_tree.column("SKU", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Sqft/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Pc/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Box/Pallet", width=60, minwidth=60, anchor="n")
            self.product_tree.column("Lbs/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Dealer Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Retail Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Box In Stock", width=90, minwidth=90, anchor="n")
            self.product_tree.column("Material", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Color Group", width=50, minwidth=50, anchor="n")
            self.product_tree.column("image_link", width=0, minwidth=0, stretch=NO, anchor="n")
            
            self.product_tree.heading("#0", anchor="w")
            self.product_tree.heading("Product", text="Product", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Product", False))
            self.product_tree.heading("Size", text="Size", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Size", False))
            self.product_tree.heading("Thickness", text="Thickness", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Thickness", False))
            self.product_tree.heading("Finish", text="Finish", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Finish", False))
            self.product_tree.heading("Brand", text="Brand", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Brand", False))
            self.product_tree.heading("SKU", text="SKU", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "SKU", False))
            self.product_tree.heading("Sqft/Box", text="Sqft/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Sqft/Box", False))
            self.product_tree.heading("Pc/Box", text="Pc/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Pc/Box", False))
            self.product_tree.heading("Box/Pallet", text="Box/Pallet", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box/Pallet", False))
            self.product_tree.heading("Lbs/Box", text="Lbs/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Lbs/Box", False))
            self.product_tree.heading("Dealer Price", text="Dealer Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Dealer Price", False))
            self.product_tree.heading("Retail Price", text="Retail Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Retail Price", False))
            self.product_tree.heading("Box In Stock", text="Box In Stock", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box In Stock", False))
            self.product_tree.heading("Material", text="Material", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Material", False))
            self.product_tree.heading("Color Group", text="Color Group", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Color Group", False))
            self.product_tree.heading("image_link", text="image_link", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "image_link", False))   
        elif material == 'carpet':
            choices = ['Product', 'Size', 'Thickness', 'Wear Layer', 'Finish', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group']
            self.searchproductBy.configure(value=choices)


            self.product_tree['columns'] = ('Product', 'Size', 'Thickness', 'Wear Layer', 'Finish', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group', 'image_link')

            #formate treeview columns
            self.product_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
            self.product_tree.column("Product", width=200, minwidth=100, anchor="n")
            self.product_tree.column("Size", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Thickness", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Wear Layer", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Finish", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Brand", width=100, minwidth=100, anchor="n")
            self.product_tree.column("SKU", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Sqft/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Pc/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Box/Pallet", width=60, minwidth=60, anchor="n")
            self.product_tree.column("Lbs/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Dealer Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Retail Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Box In Stock", width=90, minwidth=90, anchor="n")
            self.product_tree.column("Material", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Color Group", width=50, minwidth=50, anchor="n")
            self.product_tree.column("image_link", width=0, minwidth=0, stretch=NO, anchor="n")
            
            self.product_tree.heading("#0", anchor="w")
            self.product_tree.heading("Product", text="Product", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Product", False))
            self.product_tree.heading("Size", text="Size", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Size", False))
            self.product_tree.heading("Thickness", text="Thickness", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Thickness", False))
            self.product_tree.heading("Wear Layer", text="Wear Layer", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Wear Layer", False))
            self.product_tree.heading("Finish", text="Finish", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Finish", False))
            self.product_tree.heading("Brand", text="Brand", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Brand", False))
            self.product_tree.heading("SKU", text="SKU", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "SKU", False))
            self.product_tree.heading("Sqft/Box", text="Sqft/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Sqft/Box", False))
            self.product_tree.heading("Pc/Box", text="Pc/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Pc/Box", False))
            self.product_tree.heading("Box/Pallet", text="Box/Pallet", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box/Pallet", False))
            self.product_tree.heading("Lbs/Box", text="Lbs/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Lbs/Box", False))
            self.product_tree.heading("Dealer Price", text="Dealer Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Dealer Price", False))
            self.product_tree.heading("Retail Price", text="Retail Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Retail Price", False))
            self.product_tree.heading("Box In Stock", text="Box In Stock", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box In Stock", False))
            self.product_tree.heading("Material", text="Material", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Material", False))
            self.product_tree.heading("Color Group", text="Color Group", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Color Group", False))
            self.product_tree.heading("image_link", text="image_link", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "image_link", False))   
        elif material == 'mosaic':
            choices = ['Product', 'Size', 'Thickness', 'Wear Layer', 'Finish', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group']
            self.searchproductBy.configure(value=choices)

            self.product_tree['columns'] = ('Product', 'Size', 'Thickness', 'Wear Layer', 'Finish', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group', 'image_link')

            #formate treeview columns
            self.product_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
            self.product_tree.column("Product", width=200, minwidth=100, anchor="n")
            self.product_tree.column("Size", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Thickness", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Wear Layer", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Finish", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Brand", width=100, minwidth=100, anchor="n")
            self.product_tree.column("SKU", width=100, minwidth=100, anchor="n")
            self.product_tree.column("Sqft/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Pc/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Box/Pallet", width=60, minwidth=60, anchor="n")
            self.product_tree.column("Lbs/Box", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Dealer Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Retail Price", width=80, minwidth=80, anchor="n")
            self.product_tree.column("Box In Stock", width=90, minwidth=90, anchor="n")
            self.product_tree.column("Material", width=50, minwidth=50, anchor="n")
            self.product_tree.column("Color Group", width=50, minwidth=50, anchor="n")
            self.product_tree.column("image_link", width=0, minwidth=0, stretch=NO, anchor="n")
            
            self.product_tree.heading("#0", anchor="w")
            self.product_tree.heading("Product", text="Product", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Product", False))
            self.product_tree.heading("Size", text="Size", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Size", False))
            self.product_tree.heading("Thickness", text="Thickness", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Thickness", False))
            self.product_tree.heading("Wear Layer", text="Wear Layer", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Wear Layer", False))
            self.product_tree.heading("Finish", text="Finish", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Finish", False))
            self.product_tree.heading("Brand", text="Brand", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Brand", False))
            self.product_tree.heading("SKU", text="SKU", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "SKU", False))
            self.product_tree.heading("Sqft/Box", text="Sqft/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Sqft/Box", False))
            self.product_tree.heading("Pc/Box", text="Pc/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Pc/Box", False))
            self.product_tree.heading("Box/Pallet", text="Box/Pallet", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box/Pallet", False))
            self.product_tree.heading("Lbs/Box", text="Lbs/Box", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Lbs/Box", False))
            self.product_tree.heading("Dealer Price", text="Dealer Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Dealer Price", False))
            self.product_tree.heading("Retail Price", text="Retail Price", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Retail Price", False))
            self.product_tree.heading("Box In Stock", text="Box In Stock", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Box In Stock", False))
            self.product_tree.heading("Material", text="Material", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Material", False))
            self.product_tree.heading("Color Group", text="Color Group", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "Color Group", False))
            self.product_tree.heading("image_link", text="image_link", anchor="n",command=lambda: \
                                    self.treeview_sort_column(self.product_tree, "image_link", False))   
    
    def productList(self):
        if self.productListWindow is None or not self.productListWindow.winfo_exists():
            self.productListWindow = customtkinter.CTkToplevel(self)
            self.productListWindow.title("Inventory")
            self.productListWindow.geometry(f"{App.WIDTH+600}x{App.HEIGHT}")
            self.productListWindow.iconbitmap('property_manager_tool2.ico')
            self.productListWindow.minsize(App.WIDTH+600, App.HEIGHT)
            #self.productListWindow.maxsize(App.WIDTH+300, App.HEIGHT)

            self.product_frame = customtkinter.CTkFrame(master=self.productListWindow)
            self.product_frame.pack(side="top", padx=20, pady=40, fill="both", expand=True)
            self.product_tree = ttk.Treeview(self.product_frame)
            
            
            self.ProductListScrollBar = Scrollbar(self.product_frame, orient=VERTICAL)
            self.ProductListScrollBar.configure(command=self.product_tree.yview)
            self.ProductListScrollBar.pack(side=RIGHT, fill=Y)

                    
            self.product_search_entry = customtkinter.CTkEntry(master=self.productListWindow,
                                                width=150,
                                                placeholder_text="Search Product")
            self.product_search_entry.place(x=20,y=5)
            
            self.addProduct_button = customtkinter.CTkButton(master=self.productListWindow,
                                                    text="Add Product",
                                                    command=self.addProduct)
            self.addProduct_button.place(x=600,y=5)
            
            self.generateList_button = customtkinter.CTkButton(master=self.productListWindow,
                                                    text="Generate List",
                                                    command=self.generateList)
            self.generateList_button.place(x=1200,y=5)
            #treeview
            
            self.tree_style = ttk.Style(self.product_frame)
            # set ttk theme to "clam" which support the fieldbackground option
            self.tree_style.theme_use("clam")

            #Possible ideas #choices = ['Address', 'City', 'State', 'Zip', 'Bedrooms', 'Bathrooms', 'Square Feet', 'Lot Size', 'Year Built', 'Price', 'Status']
            choices2 = ['Vinyl', 'Tile', 'Laminate', 'Hardwood', 'Carpet', 'Mosaics']
            
            if customtkinter.get_appearance_mode() == "Dark":
                self.tree_style.configure("Treeview", background="#292929", 
                            fieldbackground="#292929", foreground="white")
            else:
                self.tree_style.configure("Treeview", background="white", 
                            fieldbackground="white", foreground="black")
            
            self.searchMaterial = ttk.Combobox(self.productListWindow, state="readonly", value = choices2)
            self.searchMaterial.set(choices2[0])
            self.searchMaterial.place(x=400,y=10)
            self.searchMaterial.bind("<<ComboboxSelected>>",lambda e: self.productListWindow.focus())

            choices = ['Product', 'Size', 'Thickness', 'Wear Layer', 'Brand', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock', 'Material', 'Color Group']
            self.searchproductBy = ttk.Combobox(self.productListWindow, state="readonly", value = choices)
            self.searchproductBy.set(choices[0])
            self.searchproductBy.place(x=200,y=10)
            self.searchproductBy.bind("<<ComboboxSelected>>",lambda e: self.productListWindow.focus())
                
            #define treeview columns
            self.packTreeBy(self.searchMaterial.get().lower())
            self.productSearch('n')
            
            self.product_tree.pack(side="top", fill="both", expand=True)

            
            self.product_search_entry.bind("<KeyRelease>", self.productSearch)
            self.product_tree.bind("<Double-1>", self.OpenSelectedproduct)
            self.productListWindow.focus()
        else:
            self.productListWindow.focus()  # if window exists focus it
    
    def next_photo(self):
            self.image_label.grid_forget()
            self.image_label = customtkinter.CTkLabel(master=self.productSelected_frame, text='', image=self.second_image)
            self.image_label.grid(column=1, row=0, sticky="nswe", padx=20, pady=20)
            self.PreviousButton = customtkinter.CTkButton(master=self.productSelected_frame, text="Previous", width=60,command=self.previous_photo)
            self.PreviousButton.grid(column=1, row=0, sticky="w", padx=20, pady=20)
            self.NextButton.grid_forget()
        
    def previous_photo(self):
            self.image_label.grid_forget()
            self.image_label = customtkinter.CTkLabel(master=self.productSelected_frame, text='', image=self.first_image)
            self.image_label.grid(column=1, row=0, sticky="nswe", padx=20, pady=20)
            self.NextButton = customtkinter.CTkButton(master=self.productSelected_frame, text="Next", width=60,command=self.next_photo)
            self.NextButton.grid(column=1, row=0, sticky="e", padx=20, pady=20)
            self.PreviousButton.grid_forget()
    
    def OpenSelectedproduct(self, product):
        if self.productSelected is None or not self.productSelected.winfo_exists():
            self.productSelected = customtkinter.CTkToplevel(self)
            self.productSelected.title(self.product_tree.item(self.product_tree.selection())["values"][0])
            self.productSelected.geometry(f"{App.WIDTH+220}x{App.HEIGHT+150}")
            self.productSelected.iconbitmap('property_manager_tool2.ico')
            self.productSelected.minsize(App.WIDTH+220, App.HEIGHT+150)
            self.productSelected.maxsize(App.WIDTH+220, App.HEIGHT+150)
            self.productSelected.columnconfigure(2, weight=1)
            self.productSelected.rowconfigure(1, weight=1)

            self.edit_button = customtkinter.CTkButton(master=self.productSelected, text="Edit", command=self.Login)
            self.edit_button.grid(row=0, column=2, pady=20, padx=50, sticky="e")
            
            self.save_button = customtkinter.CTkButton(master=self.productSelected, text="Save", command=self.Login)
            self.save_button.grid(row=0, column=2, pady=20, padx=200, sticky="e")

            self.productSelected_frame = customtkinter.CTkFrame(master=self.productSelected)
            self.productSelected_frame.grid(row=1, column=2, rowspan=2, columnspan=2, sticky="nswe", padx=20, pady=0)
            self.productSelected_frame.columnconfigure(2, weight=1)
            self.productSelected_frame.rowconfigure(1, weight=1)
            try:
                split_link = self.product_tree.item(self.product_tree.selection())["values"][15].split(',')
                self.image_of_sample = requests.get(split_link[0])
                self.image_of_room = requests.get(split_link[1])

            except:
                split_link = self.product_tree.item(self.product_tree.selection())["values"][14].split(',')
                self.image_of_sample = requests.get(split_link[0])
                self.image_of_room = requests.get(split_link[1])


            first_image = Image.open(BytesIO(self.image_of_sample.content)).resize((int(App.WIDTH/2), int(App.HEIGHT)))
            self.first_image = ImageTk.PhotoImage(first_image)
            
            second_image = Image.open(BytesIO(self.image_of_room.content)).resize((int(App.WIDTH/2), int(App.HEIGHT)))
            self.second_image = ImageTk.PhotoImage(second_image)

            self.image_label = customtkinter.CTkLabel(master=self.productSelected_frame, text='', image=self.first_image)
            self.image_label.grid(column=1, row=0, sticky="nswe", padx=20, pady=20)

            self.secondimage_label = customtkinter.CTkLabel(master=self.productSelected_frame, text='', image=self.second_image)
            self.secondimage_label.grid_forget()
            
            self.NextButton = customtkinter.CTkButton(master=self.productSelected_frame, text="Next", width=60,command=self.next_photo)
            self.NextButton.grid(column=1, row=0, sticky="e", padx=20, pady=20)
                        
            self.productSelected_Infoframe = customtkinter.CTkFrame(master=self.productSelected_frame)
            self.productSelected_Infoframe.grid(row=0, column=2, sticky="nsew", padx=20, pady=20)
            self.productSelected_Infoframe.columnconfigure(2, weight=1)
            self.productSelected_Infoframe.rowconfigure(6, weight=1)
            self.createFrameByMaterial(self.productSelected_Infoframe,self.searchMaterial.get().lower())
        else:
            self.productSelected.focus()  # if window exists focus it

    def createFrameByMaterial(self, frame, material):
        if material == 'vinyl':
            self.productName_label = customtkinter.CTkLabel(master=frame, text='Product Name:')
            self.productName_label.grid(column=0, row=0, sticky="w", padx=20, pady=20)
            product_name = customtkinter.StringVar()
            product_name.set(self.product_tree.item(self.product_tree.selection())["values"][0])
            self.productName_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Product Name", textvariable=product_name, state=DISABLED, text_color='gray')
            self.productName_entry.grid(row=0, column=0, pady=20, padx=115, sticky="w")

            self.productSize_label = customtkinter.CTkLabel(master=frame, text='Size:')
            self.productSize_label.grid(column=0, row=0, sticky="e", padx=10, pady=20)
            product_size = customtkinter.StringVar()
            product_size.set(self.product_tree.item(self.product_tree.selection())["values"][1])
            self.productSize_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Size", textvariable=product_size, state=DISABLED, text_color='gray')
            self.productSize_entry.grid(row=0, column=1, pady=20, padx=0, sticky="w")

            self.productThickness_label = customtkinter.CTkLabel(master=frame, text='Thickness:')
            self.productThickness_label.grid(column=0, row=1, sticky="w", padx=20, pady=20)
            product_thickness = customtkinter.StringVar()
            product_thickness.set(self.product_tree.item(self.product_tree.selection())["values"][2])
            self.productThickness_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Thickness", textvariable=product_thickness, state=DISABLED, text_color='gray')
            self.productThickness_entry.grid(row=1, column=0, pady=20, padx=115, sticky="w")
            
            self.productWearLayer_label = customtkinter.CTkLabel(master=frame, text='Wear Layer:')
            self.productWearLayer_label.grid(column=0, row=1, sticky="e", padx=10, pady=20)
            product_wearlayer = customtkinter.StringVar()
            product_wearlayer.set(self.product_tree.item(self.product_tree.selection())["values"][3])
            self.productWearLayer_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Wear Layer", textvariable=product_wearlayer, state=DISABLED, text_color='gray')
            self.productWearLayer_entry.grid(row=1, column=1, pady=20, padx=0, sticky="w")
            

            self.productBrand_label = customtkinter.CTkLabel(master=frame, text='Brand:')
            self.productBrand_label.grid(column=0, row=2, sticky="w", padx=20, pady=20)
            product_brand = customtkinter.StringVar()
            product_brand.set(self.product_tree.item(self.product_tree.selection())["values"][4])
            self.productBrand_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Brand", textvariable=product_brand, state=DISABLED, text_color='gray')
            self.productBrand_entry.grid(column=0, row=2, pady=20, padx=115, sticky="w")
            
            self.productSKU_label = customtkinter.CTkLabel(master=frame, text='SKU:')
            self.productSKU_label.grid(column=0, row=2, sticky="e", padx=10, pady=20)
            product_sku = customtkinter.StringVar()
            product_sku.set(self.product_tree.item(self.product_tree.selection())["values"][5])
            self.productSKU_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SKU", textvariable=product_sku, state=DISABLED, text_color='gray')
            self.productSKU_entry.grid(column=1, row=2, pady=20, padx=0, sticky="w")
            
            self.productSqftBox_label = customtkinter.CTkLabel(master=frame, text='SQFT/BOX:')
            self.productSqftBox_label.grid(column=0, row=3, sticky="w", padx=20, pady=20)
            product_sqftbox = customtkinter.StringVar()
            product_sqftbox.set(self.product_tree.item(self.product_tree.selection())["values"][6])
            self.productSqftBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SQFT/BOX", textvariable=product_sqftbox, state=DISABLED, text_color='gray')
            self.productSqftBox_entry.grid(row=3, column=0, pady=20, padx=115, sticky="w")
            
            self.productPcBox_label = customtkinter.CTkLabel(master=frame, text='PC/BOX:')
            self.productPcBox_label.grid(column=0, row=3, sticky="e", padx=10, pady=20)
            product_pcbox = customtkinter.StringVar()
            product_pcbox.set(self.product_tree.item(self.product_tree.selection())["values"][7])
            self.productPcBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="PC/BOX", textvariable=product_pcbox, state=DISABLED, text_color='gray')
            self.productPcBox_entry.grid(row=3, column=1, pady=20, padx=0, sticky="w")
            

            self.productBoxPallet_label = customtkinter.CTkLabel(master=frame, text='BOX/PALLET:')
            self.productBoxPallet_label.grid(column=0, row=4, sticky="w", padx=10, pady=20)
            product_boxpallet = customtkinter.StringVar()
            product_boxpallet.set(self.product_tree.item(self.product_tree.selection())["values"][8])
            self.productBoxPallet_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="BOX/PALLET", textvariable=product_boxpallet, state=DISABLED, text_color='gray')
            self.productBoxPallet_entry.grid(row=4, column=0, pady=20, padx=115, sticky="w")
            
            self.productLbsBox_label = customtkinter.CTkLabel(master=frame, text='Lbs/Box:')
            self.productLbsBox_label.grid(column=0, row=4, sticky="e", padx=10, pady=20)
            product_lbsbox = customtkinter.StringVar()
            product_lbsbox.set(self.product_tree.item(self.product_tree.selection())["values"][9])
            self.productLbsBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Lbs/Box", textvariable=product_lbsbox, state=DISABLED, text_color='gray')
            self.productLbsBox_entry.grid(row=4, column=1, pady=20, padx=0, sticky="w")
            
            self.productDealerPrice_label = customtkinter.CTkLabel(master=frame, text='Dealer Price:')
            self.productDealerPrice_label.grid(column=0, row=5, sticky="w", padx=10, pady=20)
            product_dealerprice = customtkinter.StringVar()
            product_dealerprice.set(self.product_tree.item(self.product_tree.selection())["values"][10])
            self.productDealerPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Dealer Price", textvariable=product_dealerprice, state=DISABLED, text_color='gray')
            self.productDealerPrice_entry.grid(row=5, column=0, pady=20, padx=115, sticky="w")
            
            self.productRetailPrice_label = customtkinter.CTkLabel(master=frame, text='Retail Price:')
            self.productRetailPrice_label.grid(column=0, row=5, sticky="e", padx=10, pady=20)
            product_retailprice = customtkinter.StringVar()
            product_retailprice.set(self.product_tree.item(self.product_tree.selection())["values"][11])
            self.productRetailPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Retail Price", textvariable=product_retailprice, state=DISABLED, text_color='gray')
            self.productRetailPrice_entry.grid(row=5, column=1, pady=20, padx=0, sticky="w")
        

            self.productBoxInStock_label = customtkinter.CTkLabel(master=frame, text='Box In Stock:')
            self.productBoxInStock_label.grid(column=0, row=6, sticky="w", padx=10, pady=20)
            product_boxinstock = customtkinter.StringVar()
            product_boxinstock.set(self.product_tree.item(self.product_tree.selection())["values"][12])
            self.productBoxInStock_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Box In Stock", textvariable=product_boxinstock, state=DISABLED, text_color='gray')
            self.productBoxInStock_entry.grid(row=6, column=0, pady=20, padx=115, sticky="w")
            
            self.productMaterial_label = customtkinter.CTkLabel(master=frame, text='Material:')
            self.productMaterial_label.grid(column=0, row=6, sticky="e", padx=10, pady=20)
            product_material = customtkinter.StringVar()
            product_material.set(self.product_tree.item(self.product_tree.selection())["values"][13])
            self.productMaterial_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Material", textvariable=product_material, state=DISABLED, text_color='gray')
            self.productMaterial_entry.grid(row=6, column=1, pady=20, padx=0, sticky="w")
        
            self.productColorGroup_label = customtkinter.CTkLabel(master=frame, text='Color Group:')
            self.productColorGroup_label.grid(column=0, row=7, sticky="w", padx=10, pady=20)
            product_colorgroup = customtkinter.StringVar()
            product_colorgroup.set(self.product_tree.item(self.product_tree.selection())["values"][14])
            self.productColorGroup_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Color Group", textvariable=product_colorgroup, state=DISABLED, text_color='gray')
            self.productColorGroup_entry.grid(row=7, column=0, pady=20, padx=115, sticky="w")

        elif material == 'laminate':
            self.productName_label = customtkinter.CTkLabel(master=frame, text='Product Name:')
            self.productName_label.grid(column=0, row=0, sticky="w", padx=20, pady=20)
            product_name = customtkinter.StringVar()
            product_name.set(self.product_tree.item(self.product_tree.selection())["values"][0])
            self.productName_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Product Name", textvariable=product_name, state=DISABLED, text_color='gray')
            self.productName_entry.grid(row=0, column=0, pady=20, padx=115, sticky="w")

            self.productSize_label = customtkinter.CTkLabel(master=frame, text='Size:')
            self.productSize_label.grid(column=0, row=0, sticky="e", padx=10, pady=20)
            product_size = customtkinter.StringVar()
            product_size.set(self.product_tree.item(self.product_tree.selection())["values"][1])
            self.productSize_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Size", textvariable=product_size, state=DISABLED, text_color='gray')
            self.productSize_entry.grid(row=0, column=1, pady=20, padx=0, sticky="w")

            self.productThickness_label = customtkinter.CTkLabel(master=frame, text='Thickness:')
            self.productThickness_label.grid(column=0, row=1, sticky="w", padx=20, pady=20)
            product_thickness = customtkinter.StringVar()
            product_thickness.set(self.product_tree.item(self.product_tree.selection())["values"][2])
            self.productThickness_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Thickness", textvariable=product_thickness, state=DISABLED, text_color='gray')
            self.productThickness_entry.grid(row=1, column=0, pady=20, padx=115, sticky="w")
            
            self.productWearLayer_label = customtkinter.CTkLabel(master=frame, text='Brand:')
            self.productWearLayer_label.grid(column=0, row=1, sticky="e", padx=10, pady=20)
            product_wearlayer = customtkinter.StringVar()
            product_wearlayer.set(self.product_tree.item(self.product_tree.selection())["values"][3])
            self.productWearLayer_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Brand", textvariable=product_wearlayer, state=DISABLED, text_color='gray')
            self.productWearLayer_entry.grid(row=1, column=1, pady=20, padx=0, sticky="w")
            

            self.productBrand_label = customtkinter.CTkLabel(master=frame, text='SKU:')
            self.productBrand_label.grid(column=0, row=2, sticky="w", padx=20, pady=20)
            product_brand = customtkinter.StringVar()
            product_brand.set(self.product_tree.item(self.product_tree.selection())["values"][4])
            self.productBrand_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SKU", textvariable=product_brand, state=DISABLED, text_color='gray')
            self.productBrand_entry.grid(column=0, row=2, pady=20, padx=115, sticky="w")
            
            self.productSKU_label = customtkinter.CTkLabel(master=frame, text='SQFT/BOX:')
            self.productSKU_label.grid(column=0, row=2, sticky="e", padx=10, pady=20)
            product_sku = customtkinter.StringVar()
            product_sku.set(self.product_tree.item(self.product_tree.selection())["values"][5])
            self.productSKU_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SQFT/BOX", textvariable=product_sku, state=DISABLED, text_color='gray')
            self.productSKU_entry.grid(column=1, row=2, pady=20, padx=0, sticky="w")
            
            self.productSqftBox_label = customtkinter.CTkLabel(master=frame, text='PC/BOX:')
            self.productSqftBox_label.grid(column=0, row=3, sticky="w", padx=20, pady=20)
            product_sqftbox = customtkinter.StringVar()
            product_sqftbox.set(self.product_tree.item(self.product_tree.selection())["values"][6])
            self.productSqftBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="PC/BOX", textvariable=product_sqftbox, state=DISABLED, text_color='gray')
            self.productSqftBox_entry.grid(row=3, column=0, pady=20, padx=115, sticky="w")
            
            self.productPcBox_label = customtkinter.CTkLabel(master=frame, text='BOX/PALLET:')
            self.productPcBox_label.grid(column=0, row=3, sticky="e", padx=10, pady=20)
            product_pcbox = customtkinter.StringVar()
            product_pcbox.set(self.product_tree.item(self.product_tree.selection())["values"][7])
            self.productPcBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="BOX/PALLET", textvariable=product_pcbox, state=DISABLED, text_color='gray')
            self.productPcBox_entry.grid(row=3, column=1, pady=20, padx=0, sticky="w")
            

            self.productBoxPallet_label = customtkinter.CTkLabel(master=frame, text='LBS/BOX:')
            self.productBoxPallet_label.grid(column=0, row=4, sticky="w", padx=10, pady=20)
            product_boxpallet = customtkinter.StringVar()
            product_boxpallet.set(self.product_tree.item(self.product_tree.selection())["values"][8])
            self.productBoxPallet_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="LBS/BOX", textvariable=product_boxpallet, state=DISABLED, text_color='gray')
            self.productBoxPallet_entry.grid(row=4, column=0, pady=20, padx=115, sticky="w")
            
            self.productLbsBox_label = customtkinter.CTkLabel(master=frame, text='Dealer Price:')
            self.productLbsBox_label.grid(column=0, row=4, sticky="e", padx=10, pady=20)
            product_lbsbox = customtkinter.StringVar()
            product_lbsbox.set(self.product_tree.item(self.product_tree.selection())["values"][9])
            self.productLbsBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Dealer Price", textvariable=product_lbsbox, state=DISABLED, text_color='gray')
            self.productLbsBox_entry.grid(row=4, column=1, pady=20, padx=0, sticky="w")
            
            self.productDealerPrice_label = customtkinter.CTkLabel(master=frame, text='Retail Price:')
            self.productDealerPrice_label.grid(column=0, row=5, sticky="w", padx=10, pady=20)
            product_dealerprice = customtkinter.StringVar()
            product_dealerprice.set(self.product_tree.item(self.product_tree.selection())["values"][10])
            self.productDealerPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Retail Price", textvariable=product_dealerprice, state=DISABLED, text_color='gray')
            self.productDealerPrice_entry.grid(row=5, column=0, pady=20, padx=115, sticky="w")
            
            self.productRetailPrice_label = customtkinter.CTkLabel(master=frame, text='Box In Stock:')
            self.productRetailPrice_label.grid(column=0, row=5, sticky="e", padx=10, pady=20)
            product_retailprice = customtkinter.StringVar()
            product_retailprice.set(self.product_tree.item(self.product_tree.selection())["values"][11])
            self.productRetailPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Box In Stock", textvariable=product_retailprice, state=DISABLED, text_color='gray')
            self.productRetailPrice_entry.grid(row=5, column=1, pady=20, padx=0, sticky="w")
        
            self.productBoxInStock_label = customtkinter.CTkLabel(master=frame, text='Material:')
            self.productBoxInStock_label.grid(column=0, row=6, sticky="w", padx=10, pady=20)
            product_boxinstock = customtkinter.StringVar()
            product_boxinstock.set(self.product_tree.item(self.product_tree.selection())["values"][12])
            self.productBoxInStock_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Material", textvariable=product_boxinstock, state=DISABLED, text_color='gray')
            self.productBoxInStock_entry.grid(row=6, column=0, pady=20, padx=115, sticky="w")
            
            self.productMaterial_label = customtkinter.CTkLabel(master=frame, text='Color Group:')
            self.productMaterial_label.grid(column=0, row=6, sticky="e", padx=10, pady=20)
            product_material = customtkinter.StringVar()
            product_material.set(self.product_tree.item(self.product_tree.selection())["values"][13])
            self.productMaterial_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Color Group", textvariable=product_material, state=DISABLED, text_color='gray')
            self.productMaterial_entry.grid(row=6, column=1, pady=20, padx=0, sticky="w")

        elif material == 'tile':
            self.productName_label = customtkinter.CTkLabel(master=frame, text='Product Name:')
            self.productName_label.grid(column=0, row=0, sticky="w", padx=20, pady=20)
            product_name = customtkinter.StringVar()
            product_name.set(self.product_tree.item(self.product_tree.selection())["values"][0])
            self.productName_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Product Name", textvariable=product_name, state=DISABLED, text_color='gray')
            self.productName_entry.grid(row=0, column=0, pady=20, padx=115, sticky="w")

            self.productSize_label = customtkinter.CTkLabel(master=frame, text='Size:')
            self.productSize_label.grid(column=0, row=0, sticky="e", padx=10, pady=20)
            product_size = customtkinter.StringVar()
            product_size.set(self.product_tree.item(self.product_tree.selection())["values"][1])
            self.productSize_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Size", textvariable=product_size, state=DISABLED, text_color='gray')
            self.productSize_entry.grid(row=0, column=1, pady=20, padx=0, sticky="w")

            self.productThickness_label = customtkinter.CTkLabel(master=frame, text='Thickness:')
            self.productThickness_label.grid(column=0, row=1, sticky="w", padx=20, pady=20)
            product_thickness = customtkinter.StringVar()
            product_thickness.set(self.product_tree.item(self.product_tree.selection())["values"][2])
            self.productThickness_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Thickness", textvariable=product_thickness, state=DISABLED, text_color='gray')
            self.productThickness_entry.grid(row=1, column=0, pady=20, padx=115, sticky="w")
            
            self.productWearLayer_label = customtkinter.CTkLabel(master=frame, text='Wear Layer:')
            self.productWearLayer_label.grid(column=0, row=1, sticky="e", padx=10, pady=20)
            product_wearlayer = customtkinter.StringVar()
            product_wearlayer.set(self.product_tree.item(self.product_tree.selection())["values"][3])
            self.productWearLayer_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Wear Layer", textvariable=product_wearlayer, state=DISABLED, text_color='gray')
            self.productWearLayer_entry.grid(row=1, column=1, pady=20, padx=0, sticky="w")
            

            self.productBrand_label = customtkinter.CTkLabel(master=frame, text='Brand:')
            self.productBrand_label.grid(column=0, row=2, sticky="w", padx=20, pady=20)
            product_brand = customtkinter.StringVar()
            product_brand.set(self.product_tree.item(self.product_tree.selection())["values"][4])
            self.productBrand_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Brand", textvariable=product_brand, state=DISABLED, text_color='gray')
            self.productBrand_entry.grid(column=0, row=2, pady=20, padx=115, sticky="w")
            
            self.productSKU_label = customtkinter.CTkLabel(master=frame, text='SKU:')
            self.productSKU_label.grid(column=0, row=2, sticky="e", padx=10, pady=20)
            product_sku = customtkinter.StringVar()
            product_sku.set(self.product_tree.item(self.product_tree.selection())["values"][5])
            self.productSKU_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SKU", textvariable=product_sku, state=DISABLED, text_color='gray')
            self.productSKU_entry.grid(column=1, row=2, pady=20, padx=0, sticky="w")
            
            self.productSqftBox_label = customtkinter.CTkLabel(master=frame, text='SQFT/BOX:')
            self.productSqftBox_label.grid(column=0, row=3, sticky="w", padx=20, pady=20)
            product_sqftbox = customtkinter.StringVar()
            product_sqftbox.set(self.product_tree.item(self.product_tree.selection())["values"][6])
            self.productSqftBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SQFT/BOX", textvariable=product_sqftbox, state=DISABLED, text_color='gray')
            self.productSqftBox_entry.grid(row=3, column=0, pady=20, padx=115, sticky="w")
            
            self.productPcBox_label = customtkinter.CTkLabel(master=frame, text='PC/BOX:')
            self.productPcBox_label.grid(column=0, row=3, sticky="e", padx=10, pady=20)
            product_pcbox = customtkinter.StringVar()
            product_pcbox.set(self.product_tree.item(self.product_tree.selection())["values"][7])
            self.productPcBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="PC/BOX", textvariable=product_pcbox, state=DISABLED, text_color='gray')
            self.productPcBox_entry.grid(row=3, column=1, pady=20, padx=0, sticky="w")
            

            self.productBoxPallet_label = customtkinter.CTkLabel(master=frame, text='BOX/PALLET:')
            self.productBoxPallet_label.grid(column=0, row=4, sticky="w", padx=10, pady=20)
            product_boxpallet = customtkinter.StringVar()
            product_boxpallet.set(self.product_tree.item(self.product_tree.selection())["values"][8])
            self.productBoxPallet_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="BOX/PALLET", textvariable=product_boxpallet, state=DISABLED, text_color='gray')
            self.productBoxPallet_entry.grid(row=4, column=0, pady=20, padx=115, sticky="w")
            
            self.productLbsBox_label = customtkinter.CTkLabel(master=frame, text='Lbs/Box:')
            self.productLbsBox_label.grid(column=0, row=4, sticky="e", padx=10, pady=20)
            product_lbsbox = customtkinter.StringVar()
            product_lbsbox.set(self.product_tree.item(self.product_tree.selection())["values"][9])
            self.productLbsBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Lbs/Box", textvariable=product_lbsbox, state=DISABLED, text_color='gray')
            self.productLbsBox_entry.grid(row=4, column=1, pady=20, padx=0, sticky="w")
            
            self.productDealerPrice_label = customtkinter.CTkLabel(master=frame, text='Dealer Price:')
            self.productDealerPrice_label.grid(column=0, row=5, sticky="w", padx=10, pady=20)
            product_dealerprice = customtkinter.StringVar()
            product_dealerprice.set(self.product_tree.item(self.product_tree.selection())["values"][10])
            self.productDealerPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Dealer Price", textvariable=product_dealerprice, state=DISABLED, text_color='gray')
            self.productDealerPrice_entry.grid(row=5, column=0, pady=20, padx=115, sticky="w")
            
            self.productRetailPrice_label = customtkinter.CTkLabel(master=frame, text='Retail Price:')
            self.productRetailPrice_label.grid(column=0, row=5, sticky="e", padx=10, pady=20)
            product_retailprice = customtkinter.StringVar()
            product_retailprice.set(self.product_tree.item(self.product_tree.selection())["values"][11])
            self.productRetailPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Retail Price", textvariable=product_retailprice, state=DISABLED, text_color='gray')
            self.productRetailPrice_entry.grid(row=5, column=1, pady=20, padx=0, sticky="w")
        

            self.productBoxInStock_label = customtkinter.CTkLabel(master=frame, text='Box In Stock:')
            self.productBoxInStock_label.grid(column=0, row=6, sticky="w", padx=10, pady=20)
            product_boxinstock = customtkinter.StringVar()
            product_boxinstock.set(self.product_tree.item(self.product_tree.selection())["values"][12])
            self.productBoxInStock_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Box In Stock", textvariable=product_boxinstock, state=DISABLED, text_color='gray')
            self.productBoxInStock_entry.grid(row=6, column=0, pady=20, padx=115, sticky="w")
            
            self.productMaterial_label = customtkinter.CTkLabel(master=frame, text='Material:')
            self.productMaterial_label.grid(column=0, row=6, sticky="e", padx=10, pady=20)
            product_material = customtkinter.StringVar()
            product_material.set(self.product_tree.item(self.product_tree.selection())["values"][13])
            self.productMaterial_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Material", textvariable=product_material, state=DISABLED, text_color='gray')
            self.productMaterial_entry.grid(row=6, column=1, pady=20, padx=0, sticky="w")
        
            self.productColorGroup_label = customtkinter.CTkLabel(master=frame, text='Color Group:')
            self.productColorGroup_label.grid(column=0, row=7, sticky="w", padx=10, pady=20)
            product_colorgroup = customtkinter.StringVar()
            product_colorgroup.set(self.product_tree.item(self.product_tree.selection())["values"][14])
            self.productColorGroup_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Color Group", textvariable=product_colorgroup, state=DISABLED, text_color='gray')
            self.productColorGroup_entry.grid(row=7, column=0, pady=20, padx=115, sticky="w")

        elif material == 'hardwood':
            self.productName_label = customtkinter.CTkLabel(master=frame, text='Product Name:')
            self.productName_label.grid(column=0, row=0, sticky="w", padx=20, pady=20)
            product_name = customtkinter.StringVar()
            product_name.set(self.product_tree.item(self.product_tree.selection())["values"][0])
            self.productName_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Product Name", textvariable=product_name, state=DISABLED, text_color='gray')
            self.productName_entry.grid(row=0, column=0, pady=20, padx=115, sticky="w")

            self.productSize_label = customtkinter.CTkLabel(master=frame, text='Size:')
            self.productSize_label.grid(column=0, row=0, sticky="e", padx=10, pady=20)
            product_size = customtkinter.StringVar()
            product_size.set(self.product_tree.item(self.product_tree.selection())["values"][1])
            self.productSize_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Size", textvariable=product_size, state=DISABLED, text_color='gray')
            self.productSize_entry.grid(row=0, column=1, pady=20, padx=0, sticky="w")

            self.productThickness_label = customtkinter.CTkLabel(master=frame, text='Thickness:')
            self.productThickness_label.grid(column=0, row=1, sticky="w", padx=20, pady=20)
            product_thickness = customtkinter.StringVar()
            product_thickness.set(self.product_tree.item(self.product_tree.selection())["values"][2])
            self.productThickness_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Thickness", textvariable=product_thickness, state=DISABLED, text_color='gray')
            self.productThickness_entry.grid(row=1, column=0, pady=20, padx=115, sticky="w")
            
            self.productWearLayer_label = customtkinter.CTkLabel(master=frame, text='Wear Layer:')
            self.productWearLayer_label.grid(column=0, row=1, sticky="e", padx=10, pady=20)
            product_wearlayer = customtkinter.StringVar()
            product_wearlayer.set(self.product_tree.item(self.product_tree.selection())["values"][3])
            self.productWearLayer_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Wear Layer", textvariable=product_wearlayer, state=DISABLED, text_color='gray')
            self.productWearLayer_entry.grid(row=1, column=1, pady=20, padx=0, sticky="w")
            

            self.productBrand_label = customtkinter.CTkLabel(master=frame, text='Brand:')
            self.productBrand_label.grid(column=0, row=2, sticky="w", padx=20, pady=20)
            product_brand = customtkinter.StringVar()
            product_brand.set(self.product_tree.item(self.product_tree.selection())["values"][4])
            self.productBrand_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Brand", textvariable=product_brand, state=DISABLED, text_color='gray')
            self.productBrand_entry.grid(column=0, row=2, pady=20, padx=115, sticky="w")
            
            self.productSKU_label = customtkinter.CTkLabel(master=frame, text='SKU:')
            self.productSKU_label.grid(column=0, row=2, sticky="e", padx=10, pady=20)
            product_sku = customtkinter.StringVar()
            product_sku.set(self.product_tree.item(self.product_tree.selection())["values"][5])
            self.productSKU_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SKU", textvariable=product_sku, state=DISABLED, text_color='gray')
            self.productSKU_entry.grid(column=1, row=2, pady=20, padx=0, sticky="w")
            
            self.productSqftBox_label = customtkinter.CTkLabel(master=frame, text='SQFT/BOX:')
            self.productSqftBox_label.grid(column=0, row=3, sticky="w", padx=20, pady=20)
            product_sqftbox = customtkinter.StringVar()
            product_sqftbox.set(self.product_tree.item(self.product_tree.selection())["values"][6])
            self.productSqftBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SQFT/BOX", textvariable=product_sqftbox, state=DISABLED, text_color='gray')
            self.productSqftBox_entry.grid(row=3, column=0, pady=20, padx=115, sticky="w")
            
            self.productPcBox_label = customtkinter.CTkLabel(master=frame, text='PC/BOX:')
            self.productPcBox_label.grid(column=0, row=3, sticky="e", padx=10, pady=20)
            product_pcbox = customtkinter.StringVar()
            product_pcbox.set(self.product_tree.item(self.product_tree.selection())["values"][7])
            self.productPcBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="PC/BOX", textvariable=product_pcbox, state=DISABLED, text_color='gray')
            self.productPcBox_entry.grid(row=3, column=1, pady=20, padx=0, sticky="w")
            

            self.productBoxPallet_label = customtkinter.CTkLabel(master=frame, text='BOX/PALLET:')
            self.productBoxPallet_label.grid(column=0, row=4, sticky="w", padx=10, pady=20)
            product_boxpallet = customtkinter.StringVar()
            product_boxpallet.set(self.product_tree.item(self.product_tree.selection())["values"][8])
            self.productBoxPallet_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="BOX/PALLET", textvariable=product_boxpallet, state=DISABLED, text_color='gray')
            self.productBoxPallet_entry.grid(row=4, column=0, pady=20, padx=115, sticky="w")
            
            self.productLbsBox_label = customtkinter.CTkLabel(master=frame, text='Lbs/Box:')
            self.productLbsBox_label.grid(column=0, row=4, sticky="e", padx=10, pady=20)
            product_lbsbox = customtkinter.StringVar()
            product_lbsbox.set(self.product_tree.item(self.product_tree.selection())["values"][9])
            self.productLbsBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Lbs/Box", textvariable=product_lbsbox, state=DISABLED, text_color='gray')
            self.productLbsBox_entry.grid(row=4, column=1, pady=20, padx=0, sticky="w")
            
            self.productDealerPrice_label = customtkinter.CTkLabel(master=frame, text='Dealer Price:')
            self.productDealerPrice_label.grid(column=0, row=5, sticky="w", padx=10, pady=20)
            product_dealerprice = customtkinter.StringVar()
            product_dealerprice.set(self.product_tree.item(self.product_tree.selection())["values"][10])
            self.productDealerPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Dealer Price", textvariable=product_dealerprice, state=DISABLED, text_color='gray')
            self.productDealerPrice_entry.grid(row=5, column=0, pady=20, padx=115, sticky="w")
            
            self.productRetailPrice_label = customtkinter.CTkLabel(master=frame, text='Retail Price:')
            self.productRetailPrice_label.grid(column=0, row=5, sticky="e", padx=10, pady=20)
            product_retailprice = customtkinter.StringVar()
            product_retailprice.set(self.product_tree.item(self.product_tree.selection())["values"][11])
            self.productRetailPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Retail Price", textvariable=product_retailprice, state=DISABLED, text_color='gray')
            self.productRetailPrice_entry.grid(row=5, column=1, pady=20, padx=0, sticky="w")
        

            self.productBoxInStock_label = customtkinter.CTkLabel(master=frame, text='Box In Stock:')
            self.productBoxInStock_label.grid(column=0, row=6, sticky="w", padx=10, pady=20)
            product_boxinstock = customtkinter.StringVar()
            product_boxinstock.set(self.product_tree.item(self.product_tree.selection())["values"][12])
            self.productBoxInStock_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Box In Stock", textvariable=product_boxinstock, state=DISABLED, text_color='gray')
            self.productBoxInStock_entry.grid(row=6, column=0, pady=20, padx=115, sticky="w")
            
            self.productMaterial_label = customtkinter.CTkLabel(master=frame, text='Material:')
            self.productMaterial_label.grid(column=0, row=6, sticky="e", padx=10, pady=20)
            product_material = customtkinter.StringVar()
            product_material.set(self.product_tree.item(self.product_tree.selection())["values"][13])
            self.productMaterial_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Material", textvariable=product_material, state=DISABLED, text_color='gray')
            self.productMaterial_entry.grid(row=6, column=1, pady=20, padx=0, sticky="w")
        
            self.productColorGroup_label = customtkinter.CTkLabel(master=frame, text='Color Group:')
            self.productColorGroup_label.grid(column=0, row=7, sticky="w", padx=10, pady=20)
            product_colorgroup = customtkinter.StringVar()
            product_colorgroup.set(self.product_tree.item(self.product_tree.selection())["values"][14])
            self.productColorGroup_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Color Group", textvariable=product_colorgroup, state=DISABLED, text_color='gray')
            self.productColorGroup_entry.grid(row=7, column=0, pady=20, padx=115, sticky="w")

        elif material == 'carpet':
            self.productName_label = customtkinter.CTkLabel(master=frame, text='Product Name:')
            self.productName_label.grid(column=0, row=0, sticky="w", padx=20, pady=20)
            product_name = customtkinter.StringVar()
            product_name.set(self.product_tree.item(self.product_tree.selection())["values"][0])
            self.productName_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Product Name", textvariable=product_name, state=DISABLED, text_color='gray')
            self.productName_entry.grid(row=0, column=0, pady=20, padx=115, sticky="w")

            self.productSize_label = customtkinter.CTkLabel(master=frame, text='Size:')
            self.productSize_label.grid(column=0, row=0, sticky="e", padx=10, pady=20)
            product_size = customtkinter.StringVar()
            product_size.set(self.product_tree.item(self.product_tree.selection())["values"][1])
            self.productSize_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Size", textvariable=product_size, state=DISABLED, text_color='gray')
            self.productSize_entry.grid(row=0, column=1, pady=20, padx=0, sticky="w")

            self.productThickness_label = customtkinter.CTkLabel(master=frame, text='Thickness:')
            self.productThickness_label.grid(column=0, row=1, sticky="w", padx=20, pady=20)
            product_thickness = customtkinter.StringVar()
            product_thickness.set(self.product_tree.item(self.product_tree.selection())["values"][2])
            self.productThickness_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Thickness", textvariable=product_thickness, state=DISABLED, text_color='gray')
            self.productThickness_entry.grid(row=1, column=0, pady=20, padx=115, sticky="w")
            
            self.productWearLayer_label = customtkinter.CTkLabel(master=frame, text='Wear Layer:')
            self.productWearLayer_label.grid(column=0, row=1, sticky="e", padx=10, pady=20)
            product_wearlayer = customtkinter.StringVar()
            product_wearlayer.set(self.product_tree.item(self.product_tree.selection())["values"][3])
            self.productWearLayer_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Wear Layer", textvariable=product_wearlayer, state=DISABLED, text_color='gray')
            self.productWearLayer_entry.grid(row=1, column=1, pady=20, padx=0, sticky="w")
            

            self.productBrand_label = customtkinter.CTkLabel(master=frame, text='Brand:')
            self.productBrand_label.grid(column=0, row=2, sticky="w", padx=20, pady=20)
            product_brand = customtkinter.StringVar()
            product_brand.set(self.product_tree.item(self.product_tree.selection())["values"][4])
            self.productBrand_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Brand", textvariable=product_brand, state=DISABLED, text_color='gray')
            self.productBrand_entry.grid(column=0, row=2, pady=20, padx=115, sticky="w")
            
            self.productSKU_label = customtkinter.CTkLabel(master=frame, text='SKU:')
            self.productSKU_label.grid(column=0, row=2, sticky="e", padx=10, pady=20)
            product_sku = customtkinter.StringVar()
            product_sku.set(self.product_tree.item(self.product_tree.selection())["values"][5])
            self.productSKU_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SKU", textvariable=product_sku, state=DISABLED, text_color='gray')
            self.productSKU_entry.grid(column=1, row=2, pady=20, padx=0, sticky="w")
            
            self.productSqftBox_label = customtkinter.CTkLabel(master=frame, text='SQFT/BOX:')
            self.productSqftBox_label.grid(column=0, row=3, sticky="w", padx=20, pady=20)
            product_sqftbox = customtkinter.StringVar()
            product_sqftbox.set(self.product_tree.item(self.product_tree.selection())["values"][6])
            self.productSqftBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SQFT/BOX", textvariable=product_sqftbox, state=DISABLED, text_color='gray')
            self.productSqftBox_entry.grid(row=3, column=0, pady=20, padx=115, sticky="w")
            
            self.productPcBox_label = customtkinter.CTkLabel(master=frame, text='PC/BOX:')
            self.productPcBox_label.grid(column=0, row=3, sticky="e", padx=10, pady=20)
            product_pcbox = customtkinter.StringVar()
            product_pcbox.set(self.product_tree.item(self.product_tree.selection())["values"][7])
            self.productPcBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="PC/BOX", textvariable=product_pcbox, state=DISABLED, text_color='gray')
            self.productPcBox_entry.grid(row=3, column=1, pady=20, padx=0, sticky="w")
            

            self.productBoxPallet_label = customtkinter.CTkLabel(master=frame, text='BOX/PALLET:')
            self.productBoxPallet_label.grid(column=0, row=4, sticky="w", padx=10, pady=20)
            product_boxpallet = customtkinter.StringVar()
            product_boxpallet.set(self.product_tree.item(self.product_tree.selection())["values"][8])
            self.productBoxPallet_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="BOX/PALLET", textvariable=product_boxpallet, state=DISABLED, text_color='gray')
            self.productBoxPallet_entry.grid(row=4, column=0, pady=20, padx=115, sticky="w")
            
            self.productLbsBox_label = customtkinter.CTkLabel(master=frame, text='Lbs/Box:')
            self.productLbsBox_label.grid(column=0, row=4, sticky="e", padx=10, pady=20)
            product_lbsbox = customtkinter.StringVar()
            product_lbsbox.set(self.product_tree.item(self.product_tree.selection())["values"][9])
            self.productLbsBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Lbs/Box", textvariable=product_lbsbox, state=DISABLED, text_color='gray')
            self.productLbsBox_entry.grid(row=4, column=1, pady=20, padx=0, sticky="w")
            
            self.productDealerPrice_label = customtkinter.CTkLabel(master=frame, text='Dealer Price:')
            self.productDealerPrice_label.grid(column=0, row=5, sticky="w", padx=10, pady=20)
            product_dealerprice = customtkinter.StringVar()
            product_dealerprice.set(self.product_tree.item(self.product_tree.selection())["values"][10])
            self.productDealerPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Dealer Price", textvariable=product_dealerprice, state=DISABLED, text_color='gray')
            self.productDealerPrice_entry.grid(row=5, column=0, pady=20, padx=115, sticky="w")
            
            self.productRetailPrice_label = customtkinter.CTkLabel(master=frame, text='Retail Price:')
            self.productRetailPrice_label.grid(column=0, row=5, sticky="e", padx=10, pady=20)
            product_retailprice = customtkinter.StringVar()
            product_retailprice.set(self.product_tree.item(self.product_tree.selection())["values"][11])
            self.productRetailPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Retail Price", textvariable=product_retailprice, state=DISABLED, text_color='gray')
            self.productRetailPrice_entry.grid(row=5, column=1, pady=20, padx=0, sticky="w")
        

            self.productBoxInStock_label = customtkinter.CTkLabel(master=frame, text='Box In Stock:')
            self.productBoxInStock_label.grid(column=0, row=6, sticky="w", padx=10, pady=20)
            product_boxinstock = customtkinter.StringVar()
            product_boxinstock.set(self.product_tree.item(self.product_tree.selection())["values"][12])
            self.productBoxInStock_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Box In Stock", textvariable=product_boxinstock, state=DISABLED, text_color='gray')
            self.productBoxInStock_entry.grid(row=6, column=0, pady=20, padx=115, sticky="w")
            
            self.productMaterial_label = customtkinter.CTkLabel(master=frame, text='Material:')
            self.productMaterial_label.grid(column=0, row=6, sticky="e", padx=10, pady=20)
            product_material = customtkinter.StringVar()
            product_material.set(self.product_tree.item(self.product_tree.selection())["values"][13])
            self.productMaterial_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Material", textvariable=product_material, state=DISABLED, text_color='gray')
            self.productMaterial_entry.grid(row=6, column=1, pady=20, padx=0, sticky="w")
        
            self.productColorGroup_label = customtkinter.CTkLabel(master=frame, text='Color Group:')
            self.productColorGroup_label.grid(column=0, row=7, sticky="w", padx=10, pady=20)
            product_colorgroup = customtkinter.StringVar()
            product_colorgroup.set(self.product_tree.item(self.product_tree.selection())["values"][14])
            self.productColorGroup_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Color Group", textvariable=product_colorgroup, state=DISABLED, text_color='gray')
            self.productColorGroup_entry.grid(row=7, column=0, pady=20, padx=115, sticky="w")

        elif material == 'mosaic':
            self.productName_label = customtkinter.CTkLabel(master=frame, text='Product Name:')
            self.productName_label.grid(column=0, row=0, sticky="w", padx=20, pady=20)
            product_name = customtkinter.StringVar()
            product_name.set(self.product_tree.item(self.product_tree.selection())["values"][0])
            self.productName_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Product Name", textvariable=product_name, state=DISABLED, text_color='gray')
            self.productName_entry.grid(row=0, column=0, pady=20, padx=115, sticky="w")

            self.productSize_label = customtkinter.CTkLabel(master=frame, text='Size:')
            self.productSize_label.grid(column=0, row=0, sticky="e", padx=10, pady=20)
            product_size = customtkinter.StringVar()
            product_size.set(self.product_tree.item(self.product_tree.selection())["values"][1])
            self.productSize_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Size", textvariable=product_size, state=DISABLED, text_color='gray')
            self.productSize_entry.grid(row=0, column=1, pady=20, padx=0, sticky="w")

            self.productThickness_label = customtkinter.CTkLabel(master=frame, text='Thickness:')
            self.productThickness_label.grid(column=0, row=1, sticky="w", padx=20, pady=20)
            product_thickness = customtkinter.StringVar()
            product_thickness.set(self.product_tree.item(self.product_tree.selection())["values"][2])
            self.productThickness_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Thickness", textvariable=product_thickness, state=DISABLED, text_color='gray')
            self.productThickness_entry.grid(row=1, column=0, pady=20, padx=115, sticky="w")
            
            self.productWearLayer_label = customtkinter.CTkLabel(master=frame, text='Wear Layer:')
            self.productWearLayer_label.grid(column=0, row=1, sticky="e", padx=10, pady=20)
            product_wearlayer = customtkinter.StringVar()
            product_wearlayer.set(self.product_tree.item(self.product_tree.selection())["values"][3])
            self.productWearLayer_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Wear Layer", textvariable=product_wearlayer, state=DISABLED, text_color='gray')
            self.productWearLayer_entry.grid(row=1, column=1, pady=20, padx=0, sticky="w")
            

            self.productBrand_label = customtkinter.CTkLabel(master=frame, text='Brand:')
            self.productBrand_label.grid(column=0, row=2, sticky="w", padx=20, pady=20)
            product_brand = customtkinter.StringVar()
            product_brand.set(self.product_tree.item(self.product_tree.selection())["values"][4])
            self.productBrand_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Brand", textvariable=product_brand, state=DISABLED, text_color='gray')
            self.productBrand_entry.grid(column=0, row=2, pady=20, padx=115, sticky="w")
            
            self.productSKU_label = customtkinter.CTkLabel(master=frame, text='SKU:')
            self.productSKU_label.grid(column=0, row=2, sticky="e", padx=10, pady=20)
            product_sku = customtkinter.StringVar()
            product_sku.set(self.product_tree.item(self.product_tree.selection())["values"][5])
            self.productSKU_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SKU", textvariable=product_sku, state=DISABLED, text_color='gray')
            self.productSKU_entry.grid(column=1, row=2, pady=20, padx=0, sticky="w")
            
            self.productSqftBox_label = customtkinter.CTkLabel(master=frame, text='SQFT/BOX:')
            self.productSqftBox_label.grid(column=0, row=3, sticky="w", padx=20, pady=20)
            product_sqftbox = customtkinter.StringVar()
            product_sqftbox.set(self.product_tree.item(self.product_tree.selection())["values"][6])
            self.productSqftBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="SQFT/BOX", textvariable=product_sqftbox, state=DISABLED, text_color='gray')
            self.productSqftBox_entry.grid(row=3, column=0, pady=20, padx=115, sticky="w")
            
            self.productPcBox_label = customtkinter.CTkLabel(master=frame, text='PC/BOX:')
            self.productPcBox_label.grid(column=0, row=3, sticky="e", padx=10, pady=20)
            product_pcbox = customtkinter.StringVar()
            product_pcbox.set(self.product_tree.item(self.product_tree.selection())["values"][7])
            self.productPcBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="PC/BOX", textvariable=product_pcbox, state=DISABLED, text_color='gray')
            self.productPcBox_entry.grid(row=3, column=1, pady=20, padx=0, sticky="w")
            

            self.productBoxPallet_label = customtkinter.CTkLabel(master=frame, text='BOX/PALLET:')
            self.productBoxPallet_label.grid(column=0, row=4, sticky="w", padx=10, pady=20)
            product_boxpallet = customtkinter.StringVar()
            product_boxpallet.set(self.product_tree.item(self.product_tree.selection())["values"][8])
            self.productBoxPallet_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="BOX/PALLET", textvariable=product_boxpallet, state=DISABLED, text_color='gray')
            self.productBoxPallet_entry.grid(row=4, column=0, pady=20, padx=115, sticky="w")
            
            self.productLbsBox_label = customtkinter.CTkLabel(master=frame, text='Lbs/Box:')
            self.productLbsBox_label.grid(column=0, row=4, sticky="e", padx=10, pady=20)
            product_lbsbox = customtkinter.StringVar()
            product_lbsbox.set(self.product_tree.item(self.product_tree.selection())["values"][9])
            self.productLbsBox_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Lbs/Box", textvariable=product_lbsbox, state=DISABLED, text_color='gray')
            self.productLbsBox_entry.grid(row=4, column=1, pady=20, padx=0, sticky="w")
            
            self.productDealerPrice_label = customtkinter.CTkLabel(master=frame, text='Dealer Price:')
            self.productDealerPrice_label.grid(column=0, row=5, sticky="w", padx=10, pady=20)
            product_dealerprice = customtkinter.StringVar()
            product_dealerprice.set(self.product_tree.item(self.product_tree.selection())["values"][10])
            self.productDealerPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Dealer Price", textvariable=product_dealerprice, state=DISABLED, text_color='gray')
            self.productDealerPrice_entry.grid(row=5, column=0, pady=20, padx=115, sticky="w")
            
            self.productRetailPrice_label = customtkinter.CTkLabel(master=frame, text='Retail Price:')
            self.productRetailPrice_label.grid(column=0, row=5, sticky="e", padx=10, pady=20)
            product_retailprice = customtkinter.StringVar()
            product_retailprice.set(self.product_tree.item(self.product_tree.selection())["values"][11])
            self.productRetailPrice_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Retail Price", textvariable=product_retailprice, state=DISABLED, text_color='gray')
            self.productRetailPrice_entry.grid(row=5, column=1, pady=20, padx=0, sticky="w")
        

            self.productBoxInStock_label = customtkinter.CTkLabel(master=frame, text='Box In Stock:')
            self.productBoxInStock_label.grid(column=0, row=6, sticky="w", padx=10, pady=20)
            product_boxinstock = customtkinter.StringVar()
            product_boxinstock.set(self.product_tree.item(self.product_tree.selection())["values"][12])
            self.productBoxInStock_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Box In Stock", textvariable=product_boxinstock, state=DISABLED, text_color='gray')
            self.productBoxInStock_entry.grid(row=6, column=0, pady=20, padx=115, sticky="w")
            
            self.productMaterial_label = customtkinter.CTkLabel(master=frame, text='Material:')
            self.productMaterial_label.grid(column=0, row=6, sticky="e", padx=10, pady=20)
            product_material = customtkinter.StringVar()
            product_material.set(self.product_tree.item(self.product_tree.selection())["values"][13])
            self.productMaterial_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Material", textvariable=product_material, state=DISABLED, text_color='gray')
            self.productMaterial_entry.grid(row=6, column=1, pady=20, padx=0, sticky="w")
        
            self.productColorGroup_label = customtkinter.CTkLabel(master=frame, text='Color Group:')
            self.productColorGroup_label.grid(column=0, row=7, sticky="w", padx=10, pady=20)
            product_colorgroup = customtkinter.StringVar()
            product_colorgroup.set(self.product_tree.item(self.product_tree.selection())["values"][14])
            self.productColorGroup_entry = customtkinter.CTkEntry(master=frame, width=120, placeholder_text="Color Group", textvariable=product_colorgroup, state=DISABLED, text_color='gray')
            self.productColorGroup_entry.grid(row=7, column=0, pady=20, padx=115, sticky="w")

        else:
            self.productName_label = customtkinter.CTkLabel(master=frame, text='ERROR')
            self.productName_label.grid(column=0, row=0, sticky="w", padx=20, pady=20)

            
            self.save_button = customtkinter.CTkButton(master=frame, text="BACK", command=self.Login)
            self.save_button.grid(row=7, column=1, pady=20, padx=0, sticky="e")


        #self.fetchproductInfo(self.product_tree.item(self.product_tree.selection())["values"][1])
       
    def fetchproductInfo(self, PropAddress):
        webdriveStartup =  webdriver.Chrome(executable_path=FILE_CHROME_PATH, options=chrome_Options)          
        countyWebsite = f"https://ocpaweb.ocpafl.org/parcelsearch"
        webdriveStartup.get(countyWebsite)
        insertproductAddress = webdriveStartup.find_element(By.ID,"productAddress")
        insertproductAddress.send_keys(PropAddress)
        insertproductAddress.send_keys(Keys.ENTER)
        time.sleep(1)
        gotoproductFeatures = webdriveStartup.find_element(By.ID,"ngb-nav-6")
        gotoproductFeatures.click()
        time.sleep(1)

        self.product_image_url = webdriveStartup.find_elements_by_xpath(("//img[@class='img-fluid pr-2']"))[0].get_attribute("src")
        self.response = requests.get(self.product_image_url)
        
        self.productImage = Image.open(BytesIO(self.response.content)).resize((int(self.WIDTH/2), int(self.HEIGHT/2)))
        self.productPhotoImage = ImageTk.PhotoImage(self.productImage)

        self.selectedproductPicture = customtkinter.CTkLabel(master=self.productSelected, image=self.productPhotoImage)
        self.selectedproductPicture.grid(row=1, column=0, sticky="nswe", padx=20, pady=175)

        ################################################################################
        self.fetchedModelCode = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[0]
        print(self.fetchedModelCode.text)
        self.fetchedModelCode_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedModelCode.text, font=("Arial", 15))
        self.fetchedModelCode_label.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        
        self.ffetchedModelCode_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[0]
        print(self.ffetchedModelCode_result.text)
        self.ffetchedModelCode_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.ffetchedModelCode_result.text, font=("Arial", 15))
        self.ffetchedModelCode_result_label.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedActualYearBuilt = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[1]
        print(self.fetchedActualYearBuilt.text)
        self.fetchedActualYearBuilt_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedActualYearBuilt.text, font=("Arial", 15))
        self.fetchedActualYearBuilt_label.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedActualYearBuilt_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[0]
        print(self.fetchedActualYearBuilt_result.text)
        self.fetchedActualYearBuilt_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedActualYearBuilt_result.text, font=("Arial", 15))
        self.fetchedActualYearBuilt_result_label.grid(row=1, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedGrossArea = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[2]
        print(self.fetchedGrossArea.text)
        self.fetchedGrossArea_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedGrossArea.text, font=("Arial", 15))
        self.fetchedGrossArea_label.grid(row=2, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedGrossArea_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[3]
        print(self.fetchedGrossArea_result.text)
        self.fetchedGrossArea_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedGrossArea_result.text, font=("Arial", 15))
        self.fetchedGrossArea_result_label.grid(row=2, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedTypeCode = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[4]
        print(self.fetchedTypeCode.text)
        self.fetchedTypeCode_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedTypeCode.text, font=("Arial", 15))
        self.fetchedTypeCode_label.grid(row=3, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedTypeCode_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[1]
        print(self.fetchedTypeCode_result.text)
        self.fetchedTypeCode_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedTypeCode_result.text, font=("Arial", 15))
        self.fetchedTypeCode_result_label.grid(row=3, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBeds = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[5]
        print(self.fetchedBeds.text)
        self.fetchedBeds_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedBeds.text, font=("Arial", 15))
        self.fetchedBeds_label.grid(row=4, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBeds_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[1]
        print(self.fetchedBeds_result.text)
        self.fetchedBeds_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedBeds_result.text, font=("Arial", 15))
        self.fetchedBeds_result_label.grid(row=4, column=1, sticky="nswe", padx=10, pady=10)

        self.fetchedLivingArea = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[6]
        print(self.fetchedLivingArea.text)
        self.fetchedLivingArea_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedLivingArea.text, font=("Arial", 15))
        self.fetchedLivingArea_label.grid(row=5, column=0, sticky="nswe", padx=10, pady=10)

        self.fetchedLivingArea_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[7]
        print(self.fetchedLivingArea_result.text)
        self.fetchedLivingArea_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedLivingArea_result.text, font=("Arial", 15))
        self.fetchedLivingArea_result_label.grid(row=5, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBuildingValue = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[8]
        print(self.fetchedBuildingValue.text)
        self.fetchedBuildingValue_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedBuildingValue.text, font=("Arial", 15))
        self.fetchedBuildingValue_label.grid(row=6, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBuildingValue_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[2]
        print(self.fetchedBuildingValue_result.text)
        self.fetchedBuildingValue_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedBuildingValue_result.text, font=("Arial", 15))
        self.fetchedBuildingValue_result_label.grid(row=6, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBaths = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[9]
        print(self.fetchedBaths.text)
        self.fetchedBaths_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedBaths.text, font=("Arial", 15))
        self.fetchedBaths_label.grid(row=7, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBaths_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[2]
        print(self.fetchedBaths_result.text)
        self.fetchedBaths_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedBaths_result.text, font=("Arial", 15))
        self.fetchedBaths_result_label.grid(row=7, column=1, sticky="nswe", padx=10, pady=10)

        self.fetchedExteriorWall = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[10]
        print(self.fetchedExteriorWall.text)
        self.fetchedExteriorWall_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedExteriorWall.text, font=("Arial", 15))
        self.fetchedExteriorWall_label.grid(row=8, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedExteriorWall_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[11]
        print(self.fetchedExteriorWall_result.text)
        self.fetchedExteriorWall_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedExteriorWall_result.text, font=("Arial", 15))
        self.fetchedExteriorWall_result_label.grid(row=8, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedEstimatedNewCost = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[12]
        print(self.fetchedEstimatedNewCost.text)
        self.fetchedEstimatedNewCost_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedEstimatedNewCost.text, font=("Arial", 15))
        self.fetchedEstimatedNewCost_label.grid(row=9, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedEstimatedNewCost_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[3]
        print(self.fetchedEstimatedNewCost_result.text)
        self.fetchedEstimatedNewCost_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedEstimatedNewCost_result.text, font=("Arial", 15))
        self.fetchedEstimatedNewCost_result_label.grid(row=9, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedFloors = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[13]
        print(self.fetchedFloors.text)
        self.fetchedFloors_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedFloors.text, font=("Arial", 15))
        self.fetchedFloors_label.grid(row=10, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedFloors_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[3]
        print(self.fetchedFloors_result.text)
        self.fetchedFloors_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedFloors_result.text, font=("Arial", 15))
        self.fetchedFloors_result_label.grid(row=10, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedInteriorWall = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[14]
        print(self.fetchedInteriorWall.text)
        self.fetchedInteriorWall_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedInteriorWall.text, font=("Arial", 15))
        self.fetchedInteriorWall_label.grid(row=11, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedInteriorWall_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[15]
        print(self.fetchedInteriorWall_result.text)
        self.fetchedInteriorWall_result_label = customtkinter.CTkLabel(master=self.productSelected_frame, text=self.fetchedInteriorWall_result.text, font=("Arial", 15))
        self.fetchedInteriorWall_result_label.grid(row=11, column=1, sticky="nswe", padx=10, pady=10)

        webdriveStartup.close()

if __name__ == "__main__":
    app = App()
    app.Start()