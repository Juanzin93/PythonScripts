from kivy.app import App
from kivy.core import text
from kivy.uix.label import Label

class Menu(App):
    def build(self):
        #self.window = GridLayout()
        #self.window.cols = 1
        return Label(text="Main Menu")
        #return self.window



if __name__ == "__main__":
    Menu().run()