from tkinter import ttk
from tkinter import *
import tkinter.messagebox
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

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


chrome_Options = Options()
chrome_Options.add_argument("--headless")
chrome_Options.add_argument('user-agent="MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"')
FILE_CHROME_PATH = r"chromedriver.exe"
CHROME_PATH = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
chrome_Options.binary_location = CHROME_PATH

PATH = os.path.dirname(os.path.realpath(__file__))

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Property Management Tool - Beta")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.iconbitmap('property_management_tool/property_manager_tool2.ico')
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
        image = Image.open(PATH + "\PMS-Logo.jpg").resize((int(self.WIDTH/2), int(self.HEIGHT/2)))
        self.bg_image = ImageTk.PhotoImage(image)

        self.image_label = customtkinter.CTkLabel(master=self.main_frame, image=self.bg_image, bg_color="#292929")
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
        
        self.AdminPanel_button = customtkinter.CTkButton(master=self.logged_frame,
                                                text="Property List",
                                                command=self.PropertyList)
        self.AdminPanel_button.grid(column=0, row=0, pady=15, padx=30, sticky="n")
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
            self.property_tree.insert("", "end", values=(property[0], property[1], property[2], property[3], property[4], property[5], property[6], property[7], property[8], property[9], property[10], property[11]))

    def propertySearch(self, search):
        searched = self.property_search_entry.get()

        properties = self.propertyData
        if searched == '':
            data = []
            for property in properties:
                data.append(property)
        else:
            data = []
            for property in properties:
                if self.searchPropertyBy.get() == "Owner":
                    propertyFound = property[0]
                elif self.searchPropertyBy.get() == "Address":
                    propertyFound = property[1]
                elif self.searchPropertyBy.get() == "City":
                    propertyFound = property[2]
                elif self.searchPropertyBy.get() == "State":
                    propertyFound = property[3]
                elif self.searchPropertyBy.get() == "Zip":
                    propertyFound = property[4]
                elif self.searchPropertyBy.get() == "Vacant Time":
                    propertyFound = property[5]
                elif self.searchPropertyBy.get() == "Rent":
                    propertyFound = property[6]
                elif self.searchPropertyBy.get() == "Rent Due":
                    propertyFound = property[7]
                elif self.searchPropertyBy.get() == "Property Type":
                    propertyFound = property[8]
                elif self.searchPropertyBy.get() == "Bedrooms":
                    propertyFound = property[9]
                elif self.searchPropertyBy.get() == "Bathrooms":
                    propertyFound = property[10]
                elif self.searchPropertyBy.get() == "Garage":
                    propertyFound = property[11]
                    
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

    def PropertyList(self):
        self.PropertyListWindow = customtkinter.CTkToplevel(self)
        self.PropertyListWindow.title("Properties")
        self.PropertyListWindow.geometry(f"{App.WIDTH+400}x{App.HEIGHT}")
        self.PropertyListWindow.iconbitmap('property_management_tool/property_manager_tool2.ico')
        self.PropertyListWindow.minsize(App.WIDTH+400, App.HEIGHT)
        #self.PropertyListWindow.maxsize(App.WIDTH+300, App.HEIGHT)
        
        self.property_frame = customtkinter.CTkFrame(master=self.PropertyListWindow)
        self.property_frame.pack(side="top", padx=20, pady=40, fill="both", expand=True)
                
        self.property_search_entry = customtkinter.CTkEntry(master=self.PropertyListWindow,
                                            width=150,
                                            placeholder_text="Search Property")
        self.property_search_entry.place(x=20,y=5)

        #treeview
        
        self.tree_style = ttk.Style(self.property_frame)
        # set ttk theme to "clam" which support the fieldbackground option
        self.tree_style.theme_use("clam")

        #Possible ideas #choices = ['Address', 'City', 'State', 'Zip', 'Bedrooms', 'Bathrooms', 'Square Feet', 'Lot Size', 'Year Built', 'Price', 'Status']
        choices = ['Owner','Address', 'City', 'State', 'Zip', 'Vacant Time', 'Rent', 'Rent Due', 'Property Type', 'Bedrooms', 'Bathrooms', 'Garage']

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
        self.property_tree['columns'] = ('Property Owner', 'Property Address', 'Property City', 'Property State', 'Property Zip', 'Vacant Time', 'Property Rent', 'Property Rent Due', 'Property Type', 'Property Bedrooms', 'Property Bathrooms', 'Property Garage')

        #formate treeview columns
        self.property_tree.column("#0", width=0, minwidth=0, stretch=NO, anchor="w")
        self.property_tree.column("Property Owner", width=100, minwidth=100, anchor="w")
        self.property_tree.column("Property Address", width=220, minwidth=120, anchor="w")
        self.property_tree.column("Property City", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Property State", width=50, minwidth=50, anchor="n")
        self.property_tree.column("Property Zip", width=80, minwidth=80, anchor="n")
        self.property_tree.column("Vacant Time", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Property Rent", width=80, minwidth=80, anchor="n")
        self.property_tree.column("Property Rent Due", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Property Type", width=100, minwidth=100, anchor="n")
        self.property_tree.column("Property Bedrooms", width=50, minwidth=50, anchor="n")
        self.property_tree.column("Property Bathrooms", width=50, minwidth=50, anchor="n")
        self.property_tree.column("Property Garage", width=80, minwidth=80, anchor="n")
        
        self.property_tree.heading("#0", anchor="w")
        self.property_tree.heading("Property Owner", text="Owner", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Owner", False))
        self.property_tree.heading("Property Address", text="Address", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Address", False))
        self.property_tree.heading("Property City", text="City", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property City", False))
        self.property_tree.heading("Property State", text="State", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property State", False))
        self.property_tree.heading("Property Zip", text="Zip", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Zip", False))
        self.property_tree.heading("Vacant Time", text="Vacant Time", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Vacant Time", False))
        self.property_tree.heading("Property Rent", text="Rent", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Rent", False))
        self.property_tree.heading("Property Rent Due", text="Rent Due", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Rent Due", False))
        self.property_tree.heading("Property Type", text="Property Type", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Type", False))
        self.property_tree.heading("Property Bedrooms", text="Beds", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Bedrooms", False))
        self.property_tree.heading("Property Bathrooms", text="Baths", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Bathrooms", False))
        self.property_tree.heading("Property Garage", text="Garage", anchor="n",command=lambda: \
                                self.treeview_sort_column(self.property_tree, "Property Garage", False))

        self.propertyData = [
           ["Juan","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"],
           ["Felipe","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Joao","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Pedro","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Bruno","923 Main St", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Ariel","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"],
           ["Caio","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Wesley","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Weslei","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Juan","923 Main St", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Juan","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"],
           ["Oracio","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Juan","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Ricardo","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Phelippe","1792 N Hiawassee Rd", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Juan","1796 hiawassee rd", "Orlando", "FL", "32818", "23 days", "$2100", "05/03/2022", "Apartment", "3", "2", "#213"],
           ["Juan","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Ariel","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Wesley","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Bruno","923 Main St", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Ricardo","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"],
           ["Juan","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Juan","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Oracio","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Juan","923 Main St", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Juan","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"],
           ["Ricardo","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Bruno","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Juan","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Juan","923 Main St", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Bruno","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"],
           ["Juan","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Ricardo","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Juan","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Juan","923 Main St", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Bruno","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"],
           ["Juan","423 Main St", "New York", "NY", "20001", "43 days", "$3000", "06/03/2022", "Single Family", "4", "3", "2 cars"],
           ["Ricardo","623 Main St", "New York", "NY", "30001", "33 days", "$4000", "06/03/2022", "Condo", "5", "4", "2 cars"],
           ["Juan","823 Main St", "New York", "NY", "40001", "23 days", "$5000", "06/03/2022", "Townhouse", "6", "5", "2 cars"],
           ["Ricardo","923 Main St", "New York", "NY", "50001", "13 days", "$6000", "06/03/2022", "Apartment", "7", "6", "2 cars"],
           ["Juan","123 Main St", "New York", "NY", "10001", "53 days", "$2000", "06/03/2022", "Apartment", "3", "2", "#213"]
       ]
        for property in self.propertyData:
           self.property_tree.insert("", "end", values=(property[0], property[1], property[2], property[3], property[4], property[5], property[6], property[7], property[8], property[9], property[10], property[11]))

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