from tkinter import ttk, messagebox, filedialog
from tkinter import *
import customtkinter
from PIL import Image, ImageTk
import os
import time
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


HEADER = 1024
PORT = 9316
SERVER = "104.136.118.185"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

DATABASE_INFO = []

class Database:
    def __init__(self, config):
        self.config = config

    def execute_query(self, query, params=None):
        with mysql.connect(**self.config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                data = cursor.fetchall()
                print("query", query)
                if "UPDATE" in query or "INSERT" in query:
                    print("commit to db")
                    connection.commit()
                return data

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
                
                DATABASE_INFO.append(from_server)
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

        # configure grid layout (3x7)
        self.logged_frame.rowconfigure((0, 1, 2, 3), weight=1)
        self.logged_frame.rowconfigure(7, weight=10)
        self.logged_frame.columnconfigure((0, 1), weight=1)
        self.logged_frame.columnconfigure(1, weight=0)

        self.clientListFrame = customtkinter.CTkFrame(self.logged_frame)
        self.clientListFrame.place(relwidth=0.257, relheight=0.64, x=520,y=110)
        #self.clientListFrame.grid(row=2, column=1, columnspan=2, pady=20, padx=50, sticky="e")
        self.clientListScrollBar = Scrollbar(self.clientListFrame, orient=VERTICAL)

        self.clientList = Listbox(self.logged_frame, yscrollcommand=self.clientListScrollBar.set, bg="#3d3d3d", fg="silver", border=0)
        self.clientList.place(relwidth=0.247, relheight=0.64, x=510,y=110)
        #self.clientList.grid(row=2, column=1, columnspan=2, pady=20, padx=65, sticky="e")
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
                                                command=self.PropertyList)
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

    def propertyUpdate(self, data):  
        for deleteProperty in self.property_tree.get_children():
            self.property_tree.delete(deleteProperty)

        for property in data:
            self.property_tree.insert("", "end", values=(property[0], property[1], property[2], property[3], property[4], property[5], property[6], property[7], property[8], property[9]))

    def propertySearch(self, search):
        searched = self.property_search_entry.get()
        words_searched = []
        inventory_size = self.getSocketDataInventorySize(f"getSizeInventory,m")
        for i in range(int(inventory_size)):
            data = self.getSocketData(f"getInventory,{i}") #[
            db_data = json.loads(data)
            print(db_data)
            words_searched.append(db_data)
            self.property_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock']))

        properties = self.words_searched
        if searched == '':
            data = []
            for property in properties:
                data.append(property)
        else:
            data = []
            for property in properties:
                if self.searchPropertyBy.get() == "Product":
                    propertyFound = property[0]
                elif self.searchPropertyBy.get() == "Size":
                    propertyFound = property[1]
                elif self.searchPropertyBy.get() == "SKU":
                    propertyFound = property[2]
                elif self.searchPropertyBy.get() == "Sqft/Box":
                    propertyFound = property[3]
                elif self.searchPropertyBy.get() == "Pc/Box":
                    propertyFound = property[4]
                elif self.searchPropertyBy.get() == "Box/Pallet":
                    propertyFound = property[5]
                elif self.searchPropertyBy.get() == "Lbs/Box":
                    propertyFound = property[6]
                elif self.searchPropertyBy.get() == "Dealer Price":
                    propertyFound = property[7]
                elif self.searchPropertyBy.get() == "Retail Price":
                    propertyFound = property[8]
                elif self.searchPropertyBy.get() == "Box In Stock":
                    propertyFound = property[9]    
                if searched.lower() in propertyFound.lower():                    
                    data.append(property)

        
        self.propertyUpdate(sorted(data))


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
        print("AdminPanel Button pressed")
        
    def AddToDatabase(self):
        msg = [
            self.productName_entry.get(),
            self.productSize_entry.get(),
            self.productSku_entry.get(),
            self.productSqftbox_entry.get(),
            self.productPcbox_entry.get(),
            self.productBoxpallet_entry.get(),
            self.productLbsbox_entry.get(),
            self.productDealerprice_entry.get(),
            self.productRetailprice_entry.get(),
            self.productBoxInStock_entry.get()
            
        ]
        print(json.dumps(msg))
        conn = socketConnection()
        conn.requestResponse(f"addProduct,{msg}")
        conn.requestResponse(DISCONNECT_MESSAGE)
        self.PropertyListWindow.destroy()
        self.PropertyList()
        
    def addProduct(self):
        self.addProductWindow = customtkinter.CTkToplevel(self)
        self.addProductWindow.title("Add Product")
        self.addProductWindow.geometry("400x350")
        self.addProductWindow.iconbitmap('property_manager_tool2.ico')
        self.addProductWindow.minsize(400, 350)
        self.addProductWindow.maxsize(400, 350)
        
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
                                            placeholder_text="Box_In_Stock")
        self.productBoxInStock_entry.place(x=200,y=180)
        
        self.add_button = customtkinter.CTkButton(master=self.product_frame,
                                                text="Add",
                                                command=self.AddToDatabase)
        self.add_button.place(x=115,y=220)
        
    
    def PropertyList(self):
        self.PropertyListWindow = customtkinter.CTkToplevel(self)
        self.PropertyListWindow.title("Inventory")
        self.PropertyListWindow.geometry(f"{App.WIDTH+400}x{App.HEIGHT}")
        self.PropertyListWindow.iconbitmap('property_manager_tool2.ico')
        self.PropertyListWindow.minsize(App.WIDTH+400, App.HEIGHT)
        #self.PropertyListWindow.maxsize(App.WIDTH+300, App.HEIGHT)
        
        self.property_frame = customtkinter.CTkFrame(master=self.PropertyListWindow)
        self.property_frame.pack(side="top", padx=20, pady=40, fill="both", expand=True)
                
        self.property_search_entry = customtkinter.CTkEntry(master=self.PropertyListWindow,
                                            width=150,
                                            placeholder_text="Search Product")
        self.property_search_entry.place(x=20,y=5)
        
        self.addProduct_button = customtkinter.CTkButton(master=self.PropertyListWindow,
                                                text="Add Product",
                                                command=self.addProduct)
        self.addProduct_button.place(x=400,y=5)
        #treeview
        
        self.tree_style = ttk.Style(self.property_frame)
        # set ttk theme to "clam" which support the fieldbackground option
        self.tree_style.theme_use("clam")

        #Possible ideas #choices = ['Address', 'City', 'State', 'Zip', 'Bedrooms', 'Bathrooms', 'Square Feet', 'Lot Size', 'Year Built', 'Price', 'Status']
        choices = ['Product','Size', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock']

        self.searchPropertyBy = ttk.Combobox(self.PropertyListWindow, state="readonly", value = choices)
        self.searchPropertyBy.set(choices[0])
        self.searchPropertyBy.place(x=200,y=10)
        self.searchPropertyBy.bind("<<ComboboxSelected>>",lambda e: self.PropertyListWindow.focus())
        self.property_tree = ttk.Treeview(self.property_frame)
        if customtkinter.get_appearance_mode() == "Dark":
            self.tree_style.configure("Treeview", background="#292929", 
                        fieldbackground="#292929", foreground="white")
        else:
            self.tree_style.configure("Treeview", background="white", 
                        fieldbackground="white", foreground="black")
        #define treeview columns
        self.property_tree['columns'] = ('Product','Size', 'SKU', 'Sqft/Box', 'Pc/Box', 'Box/Pallet', 'Lbs/Box', 'Dealer Price', 'Retail Price', 'Box In Stock')

        #formate treeview columns
        self.property_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
        self.property_tree.column("Product", width=200, minwidth=100, anchor="n")
        self.property_tree.column("Size", width=100, minwidth=120, anchor="n")
        self.property_tree.column("SKU", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Sqft/Box", width=50, minwidth=50, anchor="n")
        self.property_tree.column("Pc/Box", width=80, minwidth=80, anchor="n")
        self.property_tree.column("Box/Pallet", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Lbs/Box", width=80, minwidth=80, anchor="n")
        self.property_tree.column("Dealer Price", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Retail Price", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Box In Stock", width=50, minwidth=50, anchor="n")
        
        self.property_tree.heading("#0", anchor="w")
        self.property_tree.heading("Product", text="Product", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Product", False))
        self.property_tree.heading("Size", text="Size", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Size", False))
        self.property_tree.heading("SKU", text="SKU", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "SKU", False))
        self.property_tree.heading("Sqft/Box", text="Sqft/Box", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Sqft/Box", False))
        self.property_tree.heading("Pc/Box", text="Pc/Box", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Pc/Box", False))
        self.property_tree.heading("Box/Pallet", text="Box/Pallet", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Box/Pallet", False))
        self.property_tree.heading("Lbs/Box", text="Lbs/Box", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Lbs/Box", False))
        self.property_tree.heading("Dealer Price", text="Dealer Price", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Dealer Price", False))
        self.property_tree.heading("Retail Price", text="Retail Price", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Retail Price", False))
        self.property_tree.heading("Box In Stock", text="Box In Stock", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Box In Stock", False))

        inventory_size = self.getSocketDataInventorySize(f"getSizeInventory,m")
        print(inventory_size)
        loaded_data = []
        for i in range(int(inventory_size)):
            data = self.getSocketData(f"getInventory,{i}") #[
            db_data = json.loads(data)
            print(db_data)
            loaded_data = db_data
            self.property_tree.insert("", "end", values=(db_data['Product'], db_data['Size'], db_data['SKU'], db_data['Sqft/Box'], db_data['Pc/Box'], db_data['Box/Pallet'], db_data['Lbs/Box'], db_data['Dealer Price'], db_data['Retail Price'], db_data['Box_In_Stock']))

        self.property_tree.pack(side="top", fill="both", expand=True)

        
        self.property_search_entry.bind("<KeyRelease>", self.propertySearch)
        self.property_tree.bind("<Double-1>", self.OpenSelectedProperty)

    def OpenSelectedProperty(self, property):
        self.PropertySelected = customtkinter.CTkToplevel(self)
        self.PropertySelected.title(self.property_tree.item(self.property_tree.selection())["values"][1])
        self.PropertySelected.geometry(f"{App.WIDTH+400}x{App.HEIGHT+150}")
        self.PropertySelected.iconbitmap('property_manager_tool2.ico')
        self.PropertySelected.minsize(App.WIDTH+400, App.HEIGHT+150)
        self.PropertySelected.columnconfigure(2, weight=1)
        self.PropertySelected.rowconfigure(2, weight=1)
        self.PropertySelected_frame = customtkinter.CTkFrame(master=self.PropertySelected)
        self.PropertySelected_frame.grid(row=1, column=1, rowspan=2, columnspan=2, sticky="nswe", padx=20, pady=50)
        
        self.PropertySelected_frame.columnconfigure(1, weight=1)
        self.PropertySelected_frame.rowconfigure(12, weight=1)
        
        self.fetchPropertyInfo(self.property_tree.item(self.property_tree.selection())["values"][1])
       
    def fetchPropertyInfo(self, PropAddress):
        webdriveStartup =  webdriver.Chrome(executable_path=FILE_CHROME_PATH, options=chrome_Options)          
        countyWebsite = f"https://ocpaweb.ocpafl.org/parcelsearch"
        webdriveStartup.get(countyWebsite)
        insertPropertyAddress = webdriveStartup.find_element(By.ID,"PropertyAddress")
        insertPropertyAddress.send_keys(PropAddress)
        insertPropertyAddress.send_keys(Keys.ENTER)
        time.sleep(1)
        gotoPropertyFeatures = webdriveStartup.find_element(By.ID,"ngb-nav-6")
        gotoPropertyFeatures.click()
        time.sleep(1)

        self.property_image_url = webdriveStartup.find_elements_by_xpath(("//img[@class='img-fluid pr-2']"))[0].get_attribute("src")
        self.response = requests.get(self.property_image_url)
        
        self.propertyImage = Image.open(BytesIO(self.response.content)).resize((int(self.WIDTH/2), int(self.HEIGHT/2)))
        self.propertyPhotoImage = ImageTk.PhotoImage(self.propertyImage)

        self.selectedPropertyPicture = customtkinter.CTkLabel(master=self.PropertySelected, image=self.propertyPhotoImage)
        self.selectedPropertyPicture.grid(row=1, column=0, sticky="nswe", padx=20, pady=175)

        ################################################################################
        self.fetchedModelCode = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[0]
        print(self.fetchedModelCode.text)
        self.fetchedModelCode_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedModelCode.text, font=("Arial", 15))
        self.fetchedModelCode_label.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)
        
        self.ffetchedModelCode_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[0]
        print(self.ffetchedModelCode_result.text)
        self.ffetchedModelCode_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.ffetchedModelCode_result.text, font=("Arial", 15))
        self.ffetchedModelCode_result_label.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedActualYearBuilt = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[1]
        print(self.fetchedActualYearBuilt.text)
        self.fetchedActualYearBuilt_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedActualYearBuilt.text, font=("Arial", 15))
        self.fetchedActualYearBuilt_label.grid(row=1, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedActualYearBuilt_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[0]
        print(self.fetchedActualYearBuilt_result.text)
        self.fetchedActualYearBuilt_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedActualYearBuilt_result.text, font=("Arial", 15))
        self.fetchedActualYearBuilt_result_label.grid(row=1, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedGrossArea = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[2]
        print(self.fetchedGrossArea.text)
        self.fetchedGrossArea_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedGrossArea.text, font=("Arial", 15))
        self.fetchedGrossArea_label.grid(row=2, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedGrossArea_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[3]
        print(self.fetchedGrossArea_result.text)
        self.fetchedGrossArea_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedGrossArea_result.text, font=("Arial", 15))
        self.fetchedGrossArea_result_label.grid(row=2, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedTypeCode = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[4]
        print(self.fetchedTypeCode.text)
        self.fetchedTypeCode_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedTypeCode.text, font=("Arial", 15))
        self.fetchedTypeCode_label.grid(row=3, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedTypeCode_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[1]
        print(self.fetchedTypeCode_result.text)
        self.fetchedTypeCode_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedTypeCode_result.text, font=("Arial", 15))
        self.fetchedTypeCode_result_label.grid(row=3, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBeds = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[5]
        print(self.fetchedBeds.text)
        self.fetchedBeds_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedBeds.text, font=("Arial", 15))
        self.fetchedBeds_label.grid(row=4, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBeds_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[1]
        print(self.fetchedBeds_result.text)
        self.fetchedBeds_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedBeds_result.text, font=("Arial", 15))
        self.fetchedBeds_result_label.grid(row=4, column=1, sticky="nswe", padx=10, pady=10)

        self.fetchedLivingArea = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[6]
        print(self.fetchedLivingArea.text)
        self.fetchedLivingArea_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedLivingArea.text, font=("Arial", 15))
        self.fetchedLivingArea_label.grid(row=5, column=0, sticky="nswe", padx=10, pady=10)

        self.fetchedLivingArea_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[7]
        print(self.fetchedLivingArea_result.text)
        self.fetchedLivingArea_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedLivingArea_result.text, font=("Arial", 15))
        self.fetchedLivingArea_result_label.grid(row=5, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBuildingValue = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[8]
        print(self.fetchedBuildingValue.text)
        self.fetchedBuildingValue_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedBuildingValue.text, font=("Arial", 15))
        self.fetchedBuildingValue_label.grid(row=6, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBuildingValue_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[2]
        print(self.fetchedBuildingValue_result.text)
        self.fetchedBuildingValue_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedBuildingValue_result.text, font=("Arial", 15))
        self.fetchedBuildingValue_result_label.grid(row=6, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBaths = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[9]
        print(self.fetchedBaths.text)
        self.fetchedBaths_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedBaths.text, font=("Arial", 15))
        self.fetchedBaths_label.grid(row=7, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedBaths_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[2]
        print(self.fetchedBaths_result.text)
        self.fetchedBaths_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedBaths_result.text, font=("Arial", 15))
        self.fetchedBaths_result_label.grid(row=7, column=1, sticky="nswe", padx=10, pady=10)

        self.fetchedExteriorWall = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[10]
        print(self.fetchedExteriorWall.text)
        self.fetchedExteriorWall_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedExteriorWall.text, font=("Arial", 15))
        self.fetchedExteriorWall_label.grid(row=8, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedExteriorWall_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[11]
        print(self.fetchedExteriorWall_result.text)
        self.fetchedExteriorWall_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedExteriorWall_result.text, font=("Arial", 15))
        self.fetchedExteriorWall_result_label.grid(row=8, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedEstimatedNewCost = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[12]
        print(self.fetchedEstimatedNewCost.text)
        self.fetchedEstimatedNewCost_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedEstimatedNewCost.text, font=("Arial", 15))
        self.fetchedEstimatedNewCost_label.grid(row=9, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedEstimatedNewCost_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-3']"))[3]
        print(self.fetchedEstimatedNewCost_result.text)
        self.fetchedEstimatedNewCost_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedEstimatedNewCost_result.text, font=("Arial", 15))
        self.fetchedEstimatedNewCost_result_label.grid(row=9, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedFloors = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[13]
        print(self.fetchedFloors.text)
        self.fetchedFloors_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedFloors.text, font=("Arial", 15))
        self.fetchedFloors_label.grid(row=10, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedFloors_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-1']"))[3]
        print(self.fetchedFloors_result.text)
        self.fetchedFloors_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedFloors_result.text, font=("Arial", 15))
        self.fetchedFloors_result_label.grid(row=10, column=1, sticky="nswe", padx=10, pady=10)
        
        self.fetchedInteriorWall = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[14]
        print(self.fetchedInteriorWall.text)
        self.fetchedInteriorWall_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedInteriorWall.text, font=("Arial", 15))
        self.fetchedInteriorWall_label.grid(row=11, column=0, sticky="nswe", padx=10, pady=10)
        
        self.fetchedInteriorWall_result = webdriveStartup.find_elements_by_xpath(("//div[@class='col-md-2']"))[15]
        print(self.fetchedInteriorWall_result.text)
        self.fetchedInteriorWall_result_label = customtkinter.CTkLabel(master=self.PropertySelected_frame, text=self.fetchedInteriorWall_result.text, font=("Arial", 15))
        self.fetchedInteriorWall_result_label.grid(row=11, column=1, sticky="nswe", padx=10, pady=10)

        webdriveStartup.close()

if __name__ == "__main__":
    app = App()
    app.Start()