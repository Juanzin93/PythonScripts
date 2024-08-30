from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import OneLineListItem
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
import sqlite3

class ReviewTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '8dp'
        self.spacing = '8dp'
        self.database_connection = sqlite3.connect('reviews.db')
        self.database_cursor = self.database_connection.cursor()

        self.load_reviews()
        self.create_add_button()

    def load_reviews(self):
        self.database_cursor.execute("SELECT * FROM reviews")
        reviews = self.database_cursor.fetchall()
        for review in reviews:
            review_item = OneLineListItem(text=review[1])
            self.add_widget(review_item)

    def create_add_button(self):
        add_button = MDFloatingActionButton(icon="plus")
        add_button.bind(on_release=self.open_add_review_popup)
        self.add_widget(add_button)

    def open_add_review_popup(self, instance):
        content = MDBoxLayout(orientation='vertical', padding='8dp', spacing='8dp')
        review_input = TextInput(hint_text="Enter your review", multiline=False, size_hint=(1, None), height='48dp')
        save_button = MDFloatingActionButton(icon="check", size_hint=(1, None), height='48dp')
        save_button.bind(on_release=lambda x: self.save_review(review_input.text))
        content.add_widget(review_input)
        content.add_widget(save_button)

        popup = Popup(title="Add Review", content=content, size_hint=(None, None), size=('300dp', '200dp'))
        popup.open()

    def save_review(self, review_text):
        if review_text:
            self.database_cursor.execute("INSERT INTO reviews (review_text) VALUES (?)", (review_text,))
            self.database_connection.commit()
            review_item = OneLineListItem(text=review_text)
            self.add_widget(review_item)

class ReviewApp(MDApp):
    def build(self):
        self.database_connection = sqlite3.connect('reviews.db')
        self.database_cursor = self.database_connection.cursor()
        self.database_cursor.execute("CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, review_text TEXT)")
        self.database_connection.commit()

        return ReviewTab()

if __name__ == '__main__':
    ReviewApp().run()