from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list.list import MDList
from kivymd.uix.pickers import MDDatePicker
from kivy.core.window import Window
from kivymd.uix.behaviors.backgroundcolor_behavior import BackgroundColorBehavior
from kivyauth.google_auth import initialize_google, login_google, logout_google
import time
from kivy.clock import Clock
import ctypes

import sqlite3
import datetime
import calendar
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.event import EventDispatcher
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivymd.uix.list import OneLineListItem

connect = sqlite3.connect('FlooringAmerica.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS Users(
                UserID INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT,
                LastName TEXT,
                Email TEXT,
                Password TEXT,
                PhoneNumber TEXT,
                Address TEXT,
                City TEXT,
                State TEXT,
                ZipCode TEXT,
                Category TEXT
                )""")

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#Window.size = screensize
Window.size = (400, 600)
year = int(time.strftime("%Y"))
month = int(time.strftime("%m"))
day = int(time.strftime("%d"))
print("screen sizes= "+str(screensize))
# CORES APP
#593111 marrom
#e8ad37 amarelo
#263d5c azul escuro
#255d98 azul claro
# dividir por 255
Builder.load_file('dates.kv')
Builder.load_file('select.kv')
Builder.load_file('days.kv')
Builder.load_file('status.kv')

class LoginScreen(Screen):
    def Login(self):
        cursor.execute("SELECT * from Users")
        userData = cursor.fetchall()

        for User in userData:
            if str(User[3]) == str(self.manager.get_screen('LoginWindow').ids.user.text) and str(self.manager.get_screen('LoginWindow').ids.password.text) == str(User[4]):
                self.manager.get_screen('LoginWindow').ids.wrongPassword.text = " "
                self.manager.current = 'LoggedInWindow'
                self.manager.get_screen('LoggedInWindow').ids.welcomeLabel.text = f"Welcome {User[1]}"
                year = int(time.strftime("%Y"))
                month = time.strftime("%B")
                self.manager.get_screen('LoggedInWindow').ids.toolbarCalendar.title = f"{month} {year}"
                print("Login Successful")
                return
            else:
                print("Login Failed")
                self.manager.get_screen('LoginWindow').ids.wrongPassword.text = "Wrong Password"

    def build(self):
        initialize_google(self.after_login, self.error_listener)

    def loginWithGoogle(self):
        login_google()
    
class LoggedInScreen(Screen):
    def Logout(self):
        self.manager.get_screen('LoginWindow').ids.user.text = ""
        self.manager.get_screen('LoginWindow').ids.password.text = ""
        self.manager.current = 'LoginWindow'
        self.manager.transition.direction = "right"

    def updateCalendar(self):
        monthstr = datetime.date(1900, month, 1).strftime('%B')
        self.manager.get_screen('LoggedInWindow').ids.toolbarCalendar.title = f"{monthstr} {year}"
        

class JobsList(MDList):
    def __init__(self,**kwargs):
        super(JobsList,self).__init__(**kwargs)
        for i in range(20):
            lists = OneLineListItem(text=f"Job {i+1}")
            lists.theme_text_color = "Custom"
            lists.text_color = (1,1,1,1)
            self.add_widget(lists)

class AppSetting(MDList):
    def __init__(self,**kwargs):
        super(AppSetting,self).__init__(**kwargs)
        haduki = OneLineListItem(text=f"Account Settings")
        self.add_widget(haduki)
        for i in range(10):
            lists = OneLineListItem(text=f"Settings {i+1}")
            self.add_widget(lists)

class Initialize(Screen):
    
    def switch(self, *args):
        self.manager.current = "LoginWindow"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 5)

class WindowManager(ScreenManager):
    pass

class ContentNavigationDrawer(MDBoxLayout):
    pass

# class for Reminder in Dates
class Reminder(BoxLayout):
    def __init__(self,**kwargs):
        super(Reminder,self).__init__(**kwargs)
        
        self.orientation = 'vertical'
        self.add_widget(TextInput())
        self.b = BoxLayout(orientation = 'horizontal' , size_hint = (1,.15))
        self.add_widget(self.b)
        self.b.add_widget(Button(on_release = self.on_release,text = "OK!"))
        
    def on_release(self,event):
        print("OK clicked!")

class Status(BoxLayout,EventDispatcher):
    
    def __init__(self,**kwargs):
        super(Status,self).__init__(**kwargs)
   
class Select(BoxLayout):
    
    n = ListProperty()
    year_1_ = ObjectProperty(None)
    year_2 = ObjectProperty(None)
    lbl_ = ObjectProperty(None)
    btn = ObjectProperty(None)
    global count
    
    def __init__(self,**kwargs):
        super(Select,self).__init__(**kwargs)
        self.count = 0 
    def get_years(self):
        if self.count == 0:
            for i in range(0,100):
                if i<10:
                    self.n.append('0'+str(i))
                else:
                    self.n.append(str(i))
        self.count = 1
        self.year_1_.values = self.n
        self.year_2.values = self.n

class Dates(GridLayout):
    now = datetime.datetime.now()
    
    def __init__(self,**kwargs):
        super(Dates,self).__init__(**kwargs)
        year = int(time.strftime("%Y"))
        month = int(time.strftime("%m"))
        day = int(time.strftime("%d"))
        self.cols = 7
        self.c  = calendar.monthcalendar(year,month)
        for i in self.c:
           for j in i:
               if j == 0:
                    self.emptyButton = Button(on_release = self.on_release, disabled = True, text = '{j}'.format(j=''))
                    self.ids[f'emptyButton{j}'] = self.emptyButton
                    self.add_widget(self.emptyButton)
               else:
                   if j == day:
                       self.selectedButton = Button(on_release = self.on_release, background_color = (1, .3, .4, .85),  text = '{j}'.format(j=j))
                       self.ids[f'selectedButton{j}'] = self.selectedButton
                       self.add_widget(self.selectedButton)
                   else:
                       self.otherDays = Button(on_release = self.on_release, background_color = (0.15, 0.24, 0.36, 0.2), text = '{j}'.format(j=j))
                       self.ids[f'otherDays{j}'] = self.otherDays
                       self.add_widget(self.otherDays)
    def nextMonth(self):
        global year
        global month
        global day
        self.clear_widgets()
        month = month + 1
        if month == 13:
            month = 1
            year = year + 1
        self.c  = calendar.monthcalendar(year,month)
        for i in self.c:
           for j in i:
               if j == 0:
                    self.emptyButton = Button(on_release = self.on_release, disabled = True, text = '{j}'.format(j=''))
                    self.ids[f'emptyButton{j}'] = self.emptyButton
                    self.add_widget(self.emptyButton)
                    
               else:
                    if j == day and month == int(time.strftime("%m")) and year == int(time.strftime("%Y")):
                        self.selectedButton = Button(on_release = self.on_release, background_color = (1, .3, .4, .85),  text = '{j}'.format(j=j))
                        self.ids[f'selectedButton{j}'] = self.selectedButton
                        self.add_widget(self.selectedButton)
                    else:
                        self.otherDays = Button(on_release = self.on_release, background_color = (0.15, 0.24, 0.36, 0.2), text = '{j}'.format(j=j))
                        self.ids[f'otherDays{j}'] = self.otherDays
                        self.add_widget(self.otherDays)

    def previousMonth(self):
        global year
        global month
        global day
        self.clear_widgets()
        month = month - 1
        if month == 0:
            month = 12
            year = year - 1
        
        self.c  = calendar.monthcalendar(year,month)
        for i in self.c:
           for j in i:
               if j == 0:
                    self.emptyButton = Button(on_release = self.on_release, disabled = True, text = '{j}'.format(j=''))
                    self.ids[f'emptyButton{j}'] = self.emptyButton
                    self.add_widget(self.emptyButton)
                    
               else:
                    if j == day and month == int(time.strftime("%m")) and year == int(time.strftime("%Y")):
                        self.selectedButton = Button(on_release = self.on_release, background_color = (1, .3, .4, .85),  text = '{j}'.format(j=j))
                        self.ids[f'selectedButton{j}'] = self.selectedButton
                        self.add_widget(self.selectedButton)
                    else:
                        self.otherDays = Button(on_release = self.on_release, background_color = (0.15, 0.24, 0.36, 0.2), text = '{j}'.format(j=j))
                        self.ids[f'otherDays{j}'] = self.otherDays
                        self.add_widget(self.otherDays)
    
    def on_dismiss(self, arg):
        # Do something on close of popup
        pass
    
    def on_release(self,event):
        print ("date clicked :" + event.text)
        #event.background_color = 1,0,0,1
        self.popup = Popup(title= "Set Reminder :",
        content = Reminder(),
        size_hint=(None, None), size=(self.width*3/4, self.height))
        self.popup.bind(on_dismiss = self.on_dismiss)
        self.popup.open() 

class Months(BoxLayout):
    def __init__(self,**kwargs):
        super(Months,self).__init__(**kwargs)

#class DrawerList(ThemableBehavior, MDList):
#    def set_color_item(self, instance_item):
#        '''Called when tap on a menu item.'''
#
#        # Set the color of the icon and text for the menu item.
#        for item in self.children:
#            if item.text_color == self.theme_cls.primary_color:
#                item.text_color = self.theme_cls.text_color
#                break
#        instance_item.text_color = self.theme_cls.primary_color
        
userId = ""

class MobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('FlooringAmericaStyle.kv')

    def forgotPassword(self):
        pass

if __name__ == '__main__':
    MobileApp().run()