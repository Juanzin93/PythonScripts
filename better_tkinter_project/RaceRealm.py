import tkinter
import tkinter.messagebox
import customtkinter
import ctypes
import mysql.connector as mysql
import asyncio
import socket
import datetime
import calendar
import ctypes
import time
import json
import hashlib

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
        
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("RaceRealm VR - Admin")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
            
        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_dashboard = customtkinter.CTkFrame(master=self)
        self.frame_dashboard.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
        self.create_users = customtkinter.CTkFrame(master=self)
        self.create_users.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.create_users.grid_forget()
        
        self.manage_users = customtkinter.CTkFrame(master=self)
        self.manage_users.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        self.manage_users.grid_forget()
        
        self.entry_username = customtkinter.CTkEntry(master=self.create_users,
                                            width=120,
                                            placeholder_text="Username")
        self.entry_username.grid(row=0, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        
        self.entry_password = customtkinter.CTkEntry(master=self.create_users,
                                            width=120,
                                            placeholder_text="Password")
        self.entry_password.grid(row=0, column=2, columnspan=2, pady=20, padx=20, sticky="we")
        
        self.entry_first_name = customtkinter.CTkEntry(master=self.create_users,
                                            width=120,
                                            placeholder_text="First Name")
        self.entry_first_name.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        
        self.entry_last_name = customtkinter.CTkEntry(master=self.create_users,
                                            width=120,
                                            placeholder_text="Last Name")
        self.entry_last_name.grid(row=1, column=2, columnspan=2, pady=20, padx=20, sticky="we")

        self.entry_phone = customtkinter.CTkEntry(master=self.create_users,
                                            width=120,
                                            placeholder_text="Phone")
        self.entry_phone.grid(row=2, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.entry_email = customtkinter.CTkEntry(master=self.create_users,
                                            width=120,
                                            placeholder_text="Email")
        self.entry_email.grid(row=2, column=2, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.create_users,
                                                text="Create",
                                                command=self.create_user_button)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")
        
        self.entry2 = customtkinter.CTkEntry(master=self.manage_users,
                                            width=120,
                                            placeholder_text="Search User")
        self.entry2.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_25 = customtkinter.CTkButton(master=self.manage_users,
                                                text="Search",
                                                command=self.search_user)
        self.button_25.grid(row=1, column=2, columnspan=1, pady=20, padx=20, sticky="we")
        
        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Menu",
                                            )  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="DASHBOARD",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_dashboard)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="CREATE USERS",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_create_users)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="MANAGE USERS",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_manage_users)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_dashboard ============

        # configure grid layout (3x7)
        self.frame_dashboard.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_dashboard.rowconfigure(7, weight=10)
        self.frame_dashboard.columnconfigure((0, 1, 2), weight=1)
        self.frame_dashboard.columnconfigure(3, weight=0)
        
        
        self.currently_playing = customtkinter.CTkScrollableFrame(self.frame_dashboard)
        self.currently_playing.grid(row=1, column=0, columnspan=3, rowspan=8, pady=20, padx=20, sticky="nwse")

        # configure grid layout (1x1)
        self.currently_playing.rowconfigure(0, weight=1)
        self.currently_playing.columnconfigure(0, weight=1)
        
        self.UsersPlayingLabel_1 = customtkinter.CTkLabel(master=self.currently_playing,
                                              text="INVENTORY",
                                              )  # font name and size in px
        self.UsersPlayingLabel_1.grid(row=0, column=0, pady=10, padx=10)
        
        self.melbourne_button = customtkinter.CTkButton(master=self.frame_dashboard,
                                                text="MELBOURNE",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_melbourne)
        self.melbourne_button.grid(row=0, column=2, pady=1, padx=5)
        
        self.melbourne_button = customtkinter.CTkButton(master=self.frame_dashboard,
                                                text="ORLANDO",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_orlando)
        
        self.melbourne_button.grid(row=0, column=1, pady=1, padx=5)
        
        self.melbourne_button = customtkinter.CTkButton(master=self.frame_dashboard,
                                                text="TAMPA",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                command=self.button_tampa)
        self.melbourne_button.grid(row=0, column=0, pady=1, padx=5)

        temp_material = "Hazel Hickory"
        temp_Sqft = "1000"
        temp_Boxes = "50"
        temp_Price = "$2.00"
        
        for i in range(20):
            seat = i+1
            self.label_user = customtkinter.CTkLabel(master=self.currently_playing,
                                                    text=f"Material: {temp_material} Sqft: {temp_Sqft}   Boxes: {temp_Boxes} Price: {temp_Price}",
                                                    height=20,
                                                    fg_color=("white", "gray38"),  # <- custom tuple-color
                                                    justify=tkinter.CENTER)
            self.label_user.grid(column=0, row=i+1, sticky="nesw", padx=15, pady=15)

        # set default values
        self.switch_2.select()

    def button_dashboard(self):
        self.create_users.grid_forget()
        self.manage_users.grid_forget()        
        self.frame_dashboard.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
    def button_melbourne(self):
        self.create_users.grid_forget()
        self.manage_users.grid_forget()        
        self.frame_dashboard.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
    def button_orlando(self):
        self.create_users.grid_forget()
        self.manage_users.grid_forget()        
        self.frame_dashboard.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    
    def button_tampa(self):
        self.create_users.grid_forget()
        self.manage_users.grid_forget()        
        self.frame_dashboard.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
    def button_create_users(self):
        self.frame_dashboard.grid_forget()
        self.manage_users.grid_forget()
        self.create_users.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
        
    def create_user_button(self):
        userData = {
            'username': self.entry_username.get(),
            'password': self.entry_password.get(),
            'firstName': self.entry_first_name.get(),
            'lastName': self.entry_last_name.get(),
            'phone': self.entry_phone.get(),
            'email': self.entry_email.get()
        }
        print(self.entry_username.get())
        print(self.entry_password.get())
        print(self.entry_first_name.get())
        print(self.entry_last_name.get())
        print(self.entry_phone.get())
        print(self.entry_email.get())
        #try:
        conn = socketConnection()
        message = json.dumps(userData)
        sendUserInfo = f'createUser,{message}'
        result = conn.requestResponse(sendUserInfo)
        conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        conn.close()
        print("result",result)
        #except:
        #    tkinter.messagebox.showerror("Error", "Unable to connect to database.")
        tkinter.messagebox.showinfo("Created!", f"User {self.entry_username.get()} has been created!")
        
    def button_manage_users(self):
        self.frame_dashboard.grid_forget()
        self.create_users.grid_forget()
        self.user_list = customtkinter.CTkScrollableFrame(self.manage_users)
        self.user_list.grid(row=2, column=0, columnspan=2, rowspan=8, pady=20, padx=20, sticky="nwse")
        
        conn = socketConnection()
        category = 'searchCategory, sexo'
        result = conn.requestResponse(category)
        users = json.loads(result[0])
        conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        conn.close()
        print("users: ",users)
        num=0
        for user in users:
            num=num+1
            self.label_user = customtkinter.CTkButton(master=self.user_list,
                                                    text=f"User: {user['username']} \n" +
                                                    f"{user['firstName']} {user['lastName']}",
                                                    fg_color=("white", "gray38"),  # <- custom tuple-color
                                                    #command=self.button_manage_users
                                                    )
            
            self.label_user.grid(column=0, row=num+1, sticky="nesw", padx=15, pady=15)

        self.manage_users.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)
    
    def search_user(self):
        print("search user")
        #lock pc
        #ctypes.windll.user32.LockWorkStation()
    
    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
