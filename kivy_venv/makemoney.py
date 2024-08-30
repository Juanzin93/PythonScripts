import socket
import asyncio
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp

# Change these values to match your server's IP address and port number
SERVER_IP = '68.205.37.3'
SERVER_PORT = 9316

# Load the KV file
Builder.load_file('makemoney.kv')

class LoginScreen(Screen):
    async def login(self):
        # Get the username and password from the text inputs
        username = self.ids.username.text
        password = self.ids.password.text
        
        # Create a socket and connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        await asyncio.sleep(0)  # Allow event loop to switch tasks
        sock.connect((SERVER_IP, SERVER_PORT))
        
        # Send the username and password to the server
        data = f'{username},{password}'.encode()
        sock.send(data)
        
        # Receive the response from the server
        response = sock.recv(1024).decode()
        
        # Close the socket
        sock.close()
        
        # Check the response from the server
        if response == 'authorized':
            # Switch to the home screen
            self.manager.current = 'home'
        else:
            # Display an error message
            self.ids.error.text = 'Invalid username or password'
            
class HomeScreen(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class MyApp(MDApp):
    def build(self):
        # Create the screen manager
        sm = WindowManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HomeScreen(name='home'))
        
        return sm

if __name__ == '__main__':
    asyncio.run(MyApp().async_run())