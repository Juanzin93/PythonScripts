from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

KV = '''
Screen:

    MDToolbar:
        right_action_items: [["calendar-search", lambda x: grid.set_button_text()]]
        pos_hint: {"top": 1}

    Dates:
        id: grid
'''


class Dates(GridLayout):
    def __init__(self, **kwargs):
        super(Dates, self).__init__(**kwargs)
        self.add_widget(Button(text="1"))

    def set_button_text(self):
        for button in self.children:
            button.text = "CHANGE"


class MobileApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


MobileApp().run()