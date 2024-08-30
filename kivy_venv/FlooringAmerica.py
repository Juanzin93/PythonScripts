from kivy.app import App
from kivy.event import EventDispatcher
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image, AsyncImage
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.core.window import Window
from kivyauth.google_auth import initialize_google, login_google, logout_google
from kivy.clock import Clock as kivyClock
from kivy.factory import Factory
from kivy.storage.jsonstore import JsonStore
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.behaviors.backgroundcolor_behavior import BackgroundColorBehavior
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import ThreeLineAvatarListItem, OneLineAvatarListItem
from kivymd.uix.imagelist import SmartTileWithLabel
from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.button import MDFloatingActionButton, MDRaisedButton
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivymd.uix.menu import MDDropdownMenu

import asyncio
import socket
import datetime
import calendar
import ctypes
import time
import json
import hashlib
import sqlite3

# CORES APP
#593111 marrom
#e8ad37 amarelo
#263d5c azul escuro
#255d98 azul claro
# dividir por 255

HEADER = 1024
PORT = 9316
SERVER = "104.136.118.185"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!Disconnect"

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
#Window.size = screensize
Window.size = (400, 600)
year = int(time.strftime("%Y"))
month = int(time.strftime("%m"))
day = int(time.strftime("%d"))
print("screen sizes= "+str(screensize))
Builder.load_file('dates.kv')
Builder.load_file('select.kv')
Builder.load_file('days.kv')
Builder.load_file('status.kv')

#class AvatarListItem(TwoLineAvatarIconListItem):
#    pass

class SharedUserData:
    data = None

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

class Encryptions():
    def encryptPassword(self, password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha1()
        hash_object.update(password_bytes)
        hashed_password = hash_object.hexdigest()
        return hashed_password

class User:
    def __init__(self, userId, firstName, lastName, email, password, phone, address, city, state, zipcode, category, photo, cover, company_name):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.category = category
        self.photo = photo
        self.cover = cover
        self.company_name = company_name
        self.categories = {
            'admin': 'admin_login',
            'company': 'company_login',
            'contractor': 'contractor_login',
            'client': 'client_login'
        }

class CustomOneLineAvatarListItem(OneLineAvatarListItem):
    source = StringProperty()
 
class userCreated(Screen):
    def backToLogin(self):
        self.manager.current = 'LoginWindow'

class changePasswordScreen(Screen):
    def submit(self):
        password = self.manager.get_screen('changePasswordWindow').ids.password.text
        confirmPassword = self.manager.get_screen('changePasswordWindow').ids.confirmPassword.text
        email = self.manager.get_screen('forgotPasswordWindow').ids.email.text

        if password == confirmPassword:
            hashed_password = Encryptions().encryptPassword(password)
            conn = socketConnection()
            updatePassword = f'updatePassword,{hashed_password},{email}'
            result = conn.requestResponse(updatePassword)
            print("result",result[0])
            conn.requestResponse(DISCONNECT_MESSAGE)
            time.sleep(0.5)
            conn.close()
            dialog = errorDialogs()
            if result[0] == 'Password Updated Successfully.':
                dialog.show_error_message(result[0])
                self.manager.current = 'LoginWindow'
            else:
                dialog.show_error_message(result[0])
        else:
            dialog = errorDialogs()
            dialog.show_error_message('Password does not match.')
        
    def backToLogin(self):
        self.manager.current = 'LoginWindow'
                
class verifyToken(Screen):
    def matchToken(self):
        conn = socketConnection()
        token = self.manager.get_screen('verifyTokenWindow').ids.token.text
        email = self.manager.get_screen('forgotPasswordWindow').ids.email.text
        match = f'matchToken,{token},{email}'
        result = conn.requestResponse(match)
        print("result",result[0])
        conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        conn.close()
        if result[0] == 'True':
            self.manager.current = 'changePasswordWindow'
        else:
            dialog = errorDialogs()
            dialog.show_error_message(result[0])
        
    def backToLogin(self):
        self.manager.current = 'LoginWindow'

class passwordRecovery(Screen):
    def requestToken(self):
        print("send token to email to change password and switch to confirm token screen")
        conn = socketConnection()
        email = self.manager.get_screen('forgotPasswordWindow').ids.email.text
        requestToken = f'requestPasswordChange,{email}'
        result = conn.requestResponse(requestToken)
        print("result",result)
        conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        conn.close()
        if result[0] == 'Token Sent':
            self.manager.current = 'verifyTokenWindow'
        else:
            dialog = errorDialogs()
            dialog.show_error_message(result[0])
        
    def backToLogin(self):
        self.manager.current = 'LoginWindow'

class errorDialogs():
    dialog = None
            
    def show_error_message(self, message):
        if self.dialog:
            self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text=message,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
        self.dialog.open()
        
class signUpScreen(Screen):
    errorDialog = errorDialogs()  
    
    def create_user(self):
        try:
            field_ids = ['firstName', 'lastName', 'email', 'password', 'confirmPassword', 'phone', 'address', 'city', 'state', 'zipcode', 'category']
            userData = {}
            
            for field_id in field_ids:
                input_text = self.manager.get_screen('SignUpWindow').ids[field_id].text
                print(field_id)
                if field_id == 'password' or field_id == 'confirmPassword':
                    # why did i make it like this? using field_id? changing to input_text, if im wrong just uncommment
                    #password_bytes = field_id.encode('utf-8')
                    #hash_object = hashlib.sha1()
                    #hash_object.update(password_bytes)
                    #input_text = hash_object.hexdigest()
                    input_text = Encryptions().encryptPassword(input_text)
                userData[field_id] = str(input_text)
                
                # Check for missing input
                if input_text == "":
                    self.errorDialog.show_error_message(f"{field_id} can not be empty.")
                    return
                
            if not userData['password'] == userData['confirmPassword']:
                self.errorDialog.show_error_message("Password does not match.")
                return
                
            conn = socketConnection()
            message = json.dumps(userData)
            sendUserInfo = f'createUser,{message}'
            result = conn.requestResponse(sendUserInfo)
            conn.requestResponse(DISCONNECT_MESSAGE)
            time.sleep(0.5)
            conn.close()
            # parse the JSON-encoded list of users
            if result[0] == 'User Created':
                self.userCreated(userData['firstName'], userData['email'])
            elif result[0] == 'email already exists':
                self.errorDialog.show_error_message('Email already in use.')
            else:
                print("result",result)


        except json.JSONDecodeError as e:
            print("Invalid JSON:", e)
            LoginScreen().show_connection_error()

        except Exception as e:
            print("loginEXception", e)
            LoginScreen().show_connection_error()
    
    def userCreated(self, name, email):
        self.manager.transition.direction = "left"
        confirm = f"Congrats {name}! Your account has been created!"
        text = f"A email has been sent to {email}. Please check your email to verify your account to login."
        self.manager.get_screen('userCreated').ids.title.text = confirm
        self.manager.get_screen('userCreated').ids.emailText.text = text
        self.manager.current = 'userCreated'
        
    
    def back(self):
        self.manager.current = 'LoginWindow'

class LoginScreen(Screen):
    dialog = None
    keep_me_logged_in = BooleanProperty(False)
    store = JsonStore('myapp_settings.json')
    
    if store.exists('app_settings'):
        keep_logged_in = store.get('app_settings')['keep_logged_in']
    else:
        keep_logged_in = False
        
    def on_enter(self):
        print(self.keep_logged_in)
        if self.keep_logged_in:
            self.autoLogin()
            
    def show_connection_error(self):
        if self.dialog:
            self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text="Unable to connect to server. Contact support.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
        self.dialog.open()

    def show_invalid_credentials_error(self):
        if self.dialog:
            self.dialog = None
        if not self.dialog:
            self.dialog = MDDialog(
                text="Wrong email or password.",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        on_release=lambda _: self.dialog.dismiss()
                    )
                ],
            )
        self.dialog.open()
            
    def autoLogin(self, *args):
        self.manager.get_screen('LoginWindow').ids.user.text = self.store.get('app_settings')['email']
        self.manager.get_screen('LoginWindow').ids.password.text = self.store.get('app_settings')['password']
        self.manager.get_screen('LoginWindow').ids.keep_me_logged_in_checkbox.active = self.store.get('app_settings')['keep_logged_in']
        self.validate_login_credentials()
        
    def login(self, userData):
        if userData.categories[userData.category] == 'admin_login':
            selected_screen = AdminScreen(name='admin_login')
        elif userData.categories[userData.category] == 'company_login':
            selected_screen = CompanyScreen(name='company_login')
        elif userData.categories[userData.category] == 'contractor_login':
            selected_screen = ContractorScreen(name='contractor_login')
        elif userData.categories[userData.category] == 'client_login':
            selected_screen = ClientScreen(name='client_login')
            
        # Add the admin screen to the screen manager
        self.manager.add_widget(selected_screen)
        self.manager.current = userData.categories[userData.category]
        welcome = self.manager.get_screen(userData.categories[userData.category]).ids.welcomeLabel
        welcome.text = f"Welcome {userData.firstName}"
        welcome.theme_text_color = "Custom"
        welcome.text_color = (1, 1, 1, 1)
        year = int(time.strftime("%Y"))
        month = time.strftime("%B")
        screen = self.manager.get_screen(userData.categories[userData.category])
        screen.ids.toolbarCalendar.title = f"{month} {year}"
        screen.ids.cover_photo.source = userData.cover
        screen.ids.profile_picture.source = userData.photo
        screen.ids.nameLabel.text = f"{userData.firstName} {userData.lastName}"
        screen.ids.company_name.text = userData.company_name
        posts_tab = PostsTab()
        screen.ids.post_grid.add_widget(posts_tab)
        reviews_tab = ReviewsTab()
        screen.ids.review_grid.add_widget(reviews_tab)
        
        print("Login Successful")
    
    def validate_login_credentials(self):
        print("login")
        try:
            print("logged")
            conn = socketConnection()
            try:
                if self.keep_logged_in:
                    username = self.store.get('app_settings')['email']
                    hashed_password = self.store.get('app_settings')['password']
                else:
                    username = str(self.manager.get_screen('LoginWindow').ids.user.text)
                    password = str(self.manager.get_screen('LoginWindow').ids.password.text)
                    hashed_password = Encryptions().encryptPassword(password)
            except Exception as e:
                print(e)
                username = self.store.get('app_settings')['email']
                hashed_password = self.store.get('app_settings')['password']
                 
            
            getCredentials = f'getLoginCredentials,{username},{hashed_password}'
            result = conn.requestResponse(getCredentials)
            print("result",result)
            conn.requestResponse(DISCONNECT_MESSAGE)
            time.sleep(0.5)
            conn.close()
            # parse the JSON-encoded list of users
            if result[0] == 'denied':
                self.show_invalid_credentials_error()
            else:
                # parse the JSON-encoded list of users
                users = json.loads(result[0])

                if len(users) == 0:
                    self.show_invalid_credentials_error()
                else:
                    # create a User object from the first user in the list
                    user = User(**users[0])
                    SharedUserData.data = user
                    if self.keep_me_logged_in:
                        self.store.put('app_settings', email=username, password=hashed_password, keep_logged_in=self.keep_me_logged_in )
                    self.login(user)

        except json.JSONDecodeError as e:
            print("Invalid JSON:", e)
            self.show_connection_error()

        except Exception as e:
            print("loginEXception", e)
            self.show_connection_error()

    def signUp(self):
        self.manager.current = 'SignUpWindow'
    
    def forgotPassword(self):
        self.manager.current = 'forgotPasswordWindow'
    
    def build(self):
        initialize_google(self.after_login, self.error_listener)

    def loginWithGoogle(self):
        login_google()
        
class AdminScreen(Screen):
    rating = NumericProperty(4.5)
    cover_image = StringProperty('')
    profile_image = StringProperty('')
    company_name = StringProperty('')
    
    def Logout(self):
        screen = ScreenManagement()
        screen.Logout(self)
        
    def updateCalendar(self):
        monthstr = datetime.date(1900, month, 1).strftime('%B')
        self.manager.get_screen('admin_login').ids.toolbarCalendar.title = f"{monthstr} {year}"

    def goToNotifications(self):
        screen = ScreenManagement()
        print("admin notifications")
        screen.goToNotifications(self)
        
    def goToSearchApp(self):
        screen = ScreenManagement()
        print("admin searchapp")
        screen.goToSearchApp(self)

class PostsTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '8dp'
        self.spacing = '8dp'
        self.conn = socketConnection()
        self.load_posts()
        self.create_add_button()

    def load_posts(self):
        fetchPosts = f'load_posts,{SharedUserData.data.userId}'
        result = self.conn.requestResponse(fetchPosts)
        self.conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        self.conn.close()
        posts = json.loads(result[0])
        if len(posts) == 0:
            item = MDLabel(
                    text="No posts yet.",
                    halign="center",
                    theme_text_color = "Custom",
                    text_color = (0, 0, 0, 1)
                )
            self.add_widget(item)
        else:
            scrollview = ScrollView()
            layout = BoxLayout(orientation='vertical', spacing='8dp', size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))
            scrollview.add_widget(layout)
            self.add_widget(scrollview)
            for post in posts:
                # Create the TwoLineAvatarIconListItem
                poster = post['poster']
                post_text = post['post_text']
                post_date_in_seconds = datetime.datetime.fromtimestamp(post['date_time'])
                post_date = post_date_in_seconds.strftime("%m-%d-%Y %H:%M:%S")
               
                item = ThreeLineAvatarListItem(text=poster,
                                                secondary_text=post_date,
                                                tertiary_text=post_text)

                # Create the FitImage widget with a custom image
                sharedData = SharedUserData.data
                if sharedData:
                    photo = sharedData.photo
                else:
                    photo = ''
                image = Image(source=photo)
                fit_image = AsyncImage(source=photo)
                fit_image.add_widget(image)

                # Create the ImageLeftWidget with the FitImage as its child
                image_widget = ImageLeftWidget()
                image_widget.add_widget(fit_image)

                # Set the ImageLeftWidget as the IconLeftWidget of the TwoLineAvatarIconListItem
                item.add_widget(image_widget)

                # Add the item to the postsTab layout
                layout.add_widget(item)


    def create_add_button(self):
        print("created button on posts")
        add_button = MDFloatingActionButton(icon="plus")
        add_button.bind(on_release=self.open_add_post_popup)
        self.add_widget(add_button)

    def open_add_post_popup(self, instance):
        content = MDBoxLayout(orientation='vertical', padding='8dp', spacing='8dp')
        post_input = TextInput(hint_text="Enter your post", multiline=False, size_hint=(1, None), height='48dp')
        save_button = MDFloatingActionButton(icon="check", size_hint=(1, None), height='48dp')
        save_button.bind(on_release=lambda x: self.save_post(post_input.text))
        content.add_widget(post_input)
        content.add_widget(save_button)

        popup = Popup(title="Add post", content=content, size_hint=(None, None), size=('300dp', '200dp'))
        popup.open()

    def save_post(self, post_text):
        if post_text:
            savePosts = 'save_posts'
            self.conn.requestResponse(savePosts)
            self.conn.requestResponse(DISCONNECT_MESSAGE)
            time.sleep(0.5)
            self.conn.close()
            #self.database_cursor.execute("INSERT INTO posts (post_text) VALUES (?)", (post_text,))
            #self.database_connection.commit()
            post_item = OneLineListItem(text=post_text)
            self.add_widget(post_item)
            
 
class ReviewsTab(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = '8dp'
        self.spacing = '8dp'
        self.conn = socketConnection()

        self.load_reviews()
        #self.create_add_button()

    def load_reviews(self):
        fetchReviews = f'load_reviews,{SharedUserData.data.userId}'
        result = self.conn.requestResponse(fetchReviews)
        self.conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        self.conn.close()
        reviews = json.loads(result[0])
        if len(reviews) == 0:
            item = MDLabel(
                    text="No reviews yet.",
                    halign="center",
                    theme_text_color = "Custom",
                    text_color = (0, 0, 0, 1)
                )
            self.add_widget(item)
        else:
            scrollview = ScrollView()
            layout = BoxLayout(orientation='vertical', spacing='8dp', size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))
            scrollview.add_widget(layout)
            self.add_widget(scrollview)
            for review in reviews:
                # Create the TwoLineAvatarIconListItem
                reviewer = review['reviewer_name']
                review_text = review['review_text']
                review_date_in_seconds = datetime.datetime.fromtimestamp(review['date_time'])
                review_date = review_date_in_seconds.strftime("%m-%d-%Y %H:%M:%S")
                
                item = ThreeLineAvatarListItem(text=reviewer,
                                                secondary_text=review_date,
                                                tertiary_text=review_text)
#
                # Create the FitImage widget with a custom image
                sharedData = SharedUserData.data
                if sharedData:
                    photo = sharedData.photo
                else:
                    photo = 'http://192.168.1.138/JtelloTech/pedro.jpg'
                image = Image(source=photo)
                fit_image = AsyncImage(source=photo)
                fit_image.add_widget(image)
#
                # Create the ImageLeftWidget with the FitImage as its child
                image_widget = ImageLeftWidget()
                image_widget.add_widget(fit_image)
#
                # Set the ImageLeftWidget as the IconLeftWidget of the TwoLineAvatarIconListItem
                item.add_widget(image_widget)
#
                # Add the item to the postsTab layout
                layout.add_widget(item)

    def create_add_button(self):
        print("created button on reviewss")
        
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

        
class CompanyScreen(Screen):
    rating = NumericProperty(4.5)
    cover_image = StringProperty('')
    profile_image = StringProperty('')
    company_name = StringProperty('')
    def Logout(self):
        screen = ScreenManagement()
        screen.Logout(self)

    def goToNotifications(self):
        screen = ScreenManagement()
        print("CompanyScreen notifications")
        screen.goToNotifications(self)
        
    def goToSearchApp(self):
        screen = ScreenManagement()
        print("admin searchapp")
        screen.goToSearchApp(self)

class ContractorScreen(Screen):
    rating = NumericProperty(4.5)
    cover_image = StringProperty('')
    profile_image = StringProperty('')
    company_name = StringProperty('')
    def Logout(self):
        screen = ScreenManagement()
        screen.Logout(self)
        
    def updateCalendar(self):
        monthstr = datetime.date(1900, month, 1).strftime('%B')
        self.manager.get_screen('contractor_login').ids.toolbarCalendar.title = f"{monthstr} {year}"

    def goToNotifications(self):
        screen = ScreenManagement()
        print("ContractorScreen notifications")
        screen.goToNotifications(self)
        
    def goToSearchApp(self):
        screen = ScreenManagement()
        print("admin searchapp")
        screen.goToSearchApp(self)
        
class ClientScreen(Screen):
    rating = NumericProperty(4.5)
    cover_image = StringProperty('')
    profile_image = StringProperty('')
    company_name = StringProperty('')
    def Logout(self):
        screen = ScreenManagement()
        screen.Logout(self)

    def goToNotifications(self):
        screen = ScreenManagement()
        print("ClientScreen notifications")
        screen.goToNotifications(self)
        
    def goToSearchApp(self):
        screen = ScreenManagement()
        print("admin searchapp")
        screen.goToSearchApp(self)
      
class SearchedUser(Screen):
    rating = NumericProperty(4.5)
    cover_image = StringProperty('')
    profile_image = StringProperty('')
    company_name = StringProperty('')
        
class ScreenManagement():
    def Logout(self,screen):
        screen.manager.get_screen('LoginWindow').ids.user.text = ""
        screen.manager.get_screen('LoginWindow').ids.password.text = ""
        screen.manager.current = 'LoginWindow'
        screen.manager.transition.direction = "right"
        
    def goToNotifications(self, screen):
        screen.manager.current = 'NotificationsWindow'
        screen.manager.transition.direction = "left"
        
    def goToSearchApp(self, screen):
        screen.manager.current = 'SearchWindow'
        screen.manager.transition.direction = "left"

    def goToLoggedInScreen(self, screen):
        sharedData = SharedUserData.data
        window = sharedData.categories[sharedData.category]
        screen.manager.current = window
        screen.manager.transition.direction = "right"

class MessagesScreen(Screen):
    pass
    
class NotificationScreen(Screen):
    
    def goToLoggedInScreen(self):
        screen = ScreenManagement()
        screen.goToLoggedInScreen(self)
        
class SearchScreen(Screen):
    current_category = "Search By"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        kivyClock.schedule_once(self.create_dropdown_menu)
        self.search_task = None

    def create_dropdown_menu(self, dt):
        menu_categories = ["User", "Contractor", "Company"]
        menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": i,
                "on_release": lambda x=i: self.set_search_category(x),
            } for i in menu_categories]

        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="bottom",
            width_mult=4,
        )
        self.menu.bind()
    def set_search_category(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.menu.dismiss()
        self.current_category = text_item
        print("text item: ",text_item)
        print("current_category item: ",self.current_category)
    
    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''
         # Clear any existing scheduled search
        if self.search_task:
            self.search_task.cancel()
            
        self.ids.rv.data = []
        
        if search:
            if text == "":
                self.ids.rv.data.clear()
                self.add_searched_item("", "http://192.168.1.138/JtelloTech/interrogacao.png", "no user found", "")
            else:
                
                if self.current_category == "Search By":
                    dialog = errorDialogs()
                    dialog.show_error_message("Please select a category to search.")
                    return
                
                self.search_task = asyncio.create_task(self.search_icons(text))

                
                #conn = socketConnection()
                #categoria = self.current_category
                #if categoria == "User":
                #    categoria = "client"
                #category = f'searchCategory,{categoria}'
                #result = conn.requestResponse(category)
                #users = json.loads(result[0])
                #print("users result ",users)
                #conn.requestResponse(DISCONNECT_MESSAGE)
                #time.sleep(0.5)
                #conn.close()
                ##elif not text == " " and text.lower() in name['name'].lower():
                #for name in users:
                #    print("name: ", name)
                #    if text.lower() in name['name'].lower(): # for test only
                #        print("name: ",name['name'])
                #        add_searched_item(name['avatar'], name['name'], "User")
        else:
            self.ids.rv.data = []
            self.add_searched_item("", "", "search", "")
        
    async def search_icons(self, text):
        # Simulate network delay (replace this with your actual search request)
        await asyncio.sleep(0.5)

        # Perform the search and update the UI with the results
        users = self.perform_search(text)
        self.update_results(users, text)
        
    def perform_search(self, text):
        conn = socketConnection()
        categoria = self.current_category
        if categoria == "User":
            categoria = "client"
        category = 'searchCategory'
        result = conn.requestResponse(category)
        users = json.loads(result[0])
        conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        conn.close()
        print("users: ",users)
        return users
    
    def update_results(self, users, text):
        self.ids.rv.data.clear()
        for userdata in users:
            if self.search_task and self.search_task.cancelled():
                print("canceled")
                return  # Abort updating the results if the search was cancelled
            if text.lower() in userdata['name'].lower():
                print("text.lower")
                self.add_searched_item(userdata['id'], userdata['avatar'], userdata['name'], "User")
            print("name:", userdata)    
    
    def fetch_profile(self, text):
        conn = socketConnection()
        categoria = self.current_category
        if categoria == "User":
            categoria = "client"
        category = f'searchCategory,{categoria},%{text}%'
        result = conn.requestResponse(category)
        users = json.loads(result[0])
        conn.requestResponse(DISCONNECT_MESSAGE)
        time.sleep(0.5)
        conn.close()
        print("users: ",users)
        return users
    
    def add_searched_item(self, userId, avatar, name, category):
        self.ids.rv.data.append(
            {
                "viewclass": "CustomOneLineAvatarListItem",
                "source": avatar,
                "text": name,
                "category": category,
                "callback": lambda x=userId: self.fetch_profile(x),
            }
        )
    
    
    def goToLoggedInScreen(self):
        screen = ScreenManagement()
        screen.goToLoggedInScreen(self)

class CoverBoxLayout(MDBoxLayout):

    def callback(self):  
        print("change cover pop up")      
        #self.ids['profileImage'].source = '1.jpg'
    # or you could switch sources each click for instance
    pass

    def coverCallback(self):  
        print("change cover pop up")      
        #self.ids['profileImage'].source = '1.jpg'
    # or you could switch sources each click for instance
    pass

    def profileCallback(self):  
        print("change photo ddpop up")      
        #self.ids['profileImage'].source = '1.jpg'
    # or you could switch sources each click for instance
    pass

class ProfileBoxLayout(MDBoxLayout):

    def callback(self):  
        print("change photosss pop up")      
        #self.ids['profileImage'].source = '1.jpg'
    # or you could switch sources each click for instance
    pass

class ButtonWidget(Widget):

    def profilePhotocallback(self):  
        print("change photo pop up")      
        #self.ids['profileImage'].source = '1.jpg'
    # or you could switch sources each click for instance
    pass

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

class Notifications(MDList):
    def __init__(self,**kwargs):
        super(Notifications,self).__init__(**kwargs)
        for i in range(5):
            lists = OneLineListItem(text=f"Notification {i+1}")
            self.add_widget(lists)

class Messages(MDList):
    def __init__(self,**kwargs):
        super(Messages,self).__init__(**kwargs)
        for i in range(10):
            lists = OneLineListItem(text=f"Message {i+1}")
            lists.theme_text_color = "Custom"
            lists.text_color = (1,1,1,1)
            self.add_widget(lists)

class Initialize(Screen):
    
    store = JsonStore('myapp_settings.json')
    
    def loginWindow(self, *args):
        self.manager.current = "LoginWindow"
        
    def on_enter(self, *args):
        # called when this Screen is displayed
        
        if not self.store.exists('app_settings'):
            self.store.put('app_settings', email="", password="", keep_logged_in=False)
        
        kivyClock.schedule_once(self.loginWindow, 5)

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

class Tab(MDBoxLayout, MDTabsBase):
    pass

class StarRating(Widget):
    num_stars = NumericProperty(5)
    rating = NumericProperty(0)
    color = [1, 0, 0, 1] # default to red

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(num_stars=self.update_rating)
        self.bind(rating=self.update_rating)
        self.bind(color=self.update_rating)

    def update_rating(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=self.color)
            for i in range(self.num_stars):
                if i < self.rating:
                    Rectangle(pos=self.star_pos(i), size=self.star_size())
                elif i == int(self.rating) and self.rating % 1 != 0:
                    # draw a partially-filled star for non-integer ratings
                    pct = self.rating % 1
                    star_width = self.star_size()[0]
                    fill_width = pct * star_width
                    Rectangle(pos=self.star_pos(i), size=(fill_width, star_width))
                    Rectangle(pos=self.star_pos(i), size=self.star_size(), texture=None)
                else:
                    Rectangle(pos=self.star_pos(i), size=self.star_size(), texture=None)

    def star_size(self):
        return dp(30), dp(30)

    def star_pos(self, i):
        return self.pos[0] + (i * self.star_size()[0]), self.pos[1]
    
class StarRatings(MDBoxLayout):
    rating = NumericProperty(0)
    color = StringProperty('#ffffff')  # add default color property

class ContractorProfileScreen(Screen):
    rating = NumericProperty(4.5)
    cover_image = StringProperty('')
    profile_image = StringProperty('')
    company_name = StringProperty('')
    color = StringProperty('#ffffff')  # add default color property


class MobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_file('FlooringAmericaStyle.kv')


if __name__ == '__main__':
    asyncio.run(MobileApp().async_run())
    
    
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
