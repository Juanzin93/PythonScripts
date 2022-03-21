from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.behaviors.backgroundcolor_behavior import BackgroundColorBehavior
from kivyauth.google_auth import initialize_google, login_google, logout_google
import time
from kivy.clock import Clock

Window.size = (400, 600)


class LoginScreen(Screen):
    def welcomeUser(self):    
        self.manager.get_screen('LoggedInWindow').ids.welcomeLabel.text = f"Welcome {self.manager.get_screen('LoginWindow').ids.user.text}"
   
    def build(self):
        initialize_google(self.after_login, self.error_listener)

    def loginWithGoogle(self):
        login_google()
    
class LoggedInScreen(Screen):
    def returnLogin(self):
        self.manager.get_screen('LoginWindow').ids.user.text = ""
        self.manager.get_screen('LoginWindow').ids.password.text = ""

    pass

class Initialize(Screen):
    
    def switch(self, *args):
        self.manager.current = "LoginWindow"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 3)

class WindowManager(ScreenManager):
    pass


userId = ""
lista = ["1", "Juan", "Tello"]

class MobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('DatingAppStyle.kv')

    def getNameFromList(self):
        return lista[1]

    def getPasswordFromList(self):
        return lista[2]

    def forgotPassword(self):
        pass

if __name__ == '__main__':
    MobileApp().run()