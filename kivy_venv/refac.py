
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.button import Button
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.gridlayout import GridLayout
import datetime
import calendar
import time
KV = '''
WindowManager:
    LoggedInScreen:
<LoggedInScreen>
    name: "LoggedInWindow"
    MDBottomNavigation:
        id: bottomnav

        MDBottomNavigationItem:
            name: "screen 1"
            text: 'Home'
            icon: 'home'
            
            MDToolbar:
                id: toolbarCalendar
                title: ""
                anchor_title: "center"
                elevation: 10
                pos_hint: {"top": 1}


                MDFloatingActionButton:
                    icon: "arrow-left"
                    elevation: 0
                    on_release:
                        grid.previousMonth()
                        root.updateCalendar()

                MDFloatingActionButton:
                    icon: "arrow-right"
                    elevation: 0
                    on_release:
                        grid.nextMonth()
                        root.updateCalendar()
    
        Dates:
            id: grid
            canvas.before:
                Color:
                    rgba: 0.15, 0.24, 0.36, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
'''


year = int(time.strftime("%Y"))
month = int(time.strftime("%m"))
day = int(time.strftime("%d"))

class LoggedInScreen(Screen):
    def updateCalendar(self):
        monthstr = datetime.date(1900, month, 1).strftime('%B')
        self.manager.get_screen('LoggedInWindow').ids.toolbarCalendar.title = f"{monthstr} {year}"

class WindowManager(ScreenManager):
    pass

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
                    self.emptyButton = Button(disabled = True, text = '{j}'.format(j=''))
                    self.ids[f'emptyButton{j}'] = self.emptyButton
                    self.add_widget(self.emptyButton)
               else:
                   if j == day:
                       self.selectedButton = Button(background_color = (1, .3, .4, .85),  text = '{j}'.format(j=j))
                       self.ids[f'selectedButton{j}'] = self.selectedButton
                       self.add_widget(self.selectedButton)
                   else:
                       self.otherDays = Button(background_color = (0.15, 0.24, 0.36, 0.2), text = '{j}'.format(j=j))
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
                    self.emptyButton = Button(disabled = True, text = '{j}'.format(j=''))
                    self.ids[f'emptyButton{j}'] = self.emptyButton
                    self.add_widget(self.emptyButton)
                    
               else:
                    if j == day and month == int(time.strftime("%m")) and year == int(time.strftime("%Y")):
                        self.selectedButton = Button(background_color = (1, .3, .4, .85),  text = '{j}'.format(j=j))
                        self.ids[f'selectedButton{j}'] = self.selectedButton
                        self.add_widget(self.selectedButton)
                    else:
                        self.otherDays = Button(background_color = (0.15, 0.24, 0.36, 0.2), text = '{j}'.format(j=j))
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
                    self.emptyButton = Button(disabled = True, text = '{j}'.format(j=''))
                    self.ids[f'emptyButton{j}'] = self.emptyButton
                    self.add_widget(self.emptyButton)
                    
               else:
                    if j == day and month == int(time.strftime("%m")) and year == int(time.strftime("%Y")):
                        self.selectedButton = Button(background_color = (1, .3, .4, .85),  text = '{j}'.format(j=j))
                        self.ids[f'selectedButton{j}'] = self.selectedButton
                        self.add_widget(self.selectedButton)
                    else:
                        self.otherDays = Button(background_color = (0.15, 0.24, 0.36, 0.2), text = '{j}'.format(j=j))
                        self.ids[f'otherDays{j}'] = self.otherDays
                        self.add_widget(self.otherDays)
        
class MobileApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    MobileApp().run()