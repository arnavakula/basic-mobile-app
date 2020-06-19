import glob
import json
import random
from datetime import datetime
from pathlib import Path

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

Builder.load_file('design.kv')
 
class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'sign_up_screen'

    def login(self, name, pword):
        with open('users.json', 'r') as f:
            users = json.load(f)
        if name in users.keys() and users[name]['password'] == pword:
            self.manager.current = 'login_success_screen'
        else:
            self.ids.login_error.text = "The username you entered does not match the password."


class LoginSuccessScreen(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'

    def display_quote(self, feeling):
        feeling = feeling.lower()
        valid_feelings = [Path(filename).stem for filename in glob.glob('quotes/*txt')]
        if feeling in valid_feelings:
            with open(f'quotes/{feeling}.txt') as f:
                quotes = f.readlines()
            self.ids.quote.text = random.choice(quotes)
        else: 
            self.ids.quote.text = 'Sorry, that is not a valid feeling in this release.'

class SignUpScreen(Screen):
    def to_login_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'
    def add_user(self, name, pword):
        with open('users.json') as f:
            users = json.load(f)   
        
        if name in users:
            self.ids.sign_up_error.text = "Sorry, that username already exists. Please enter another one."
        else:
            users[name] = {'username': name, 'password': pword, 'created': datetime.now().strftime('%m-%d-%Y')}  
            with open('users.json', 'w') as f:
                json.dump(users, f)
            self.manager.current = 'sign_up_success_screen'

class SignUpSuccessScreen(Screen):
    def to_login_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'login_screen'
    pass
        
class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
 
if __name__== '__main__':
    MainApp().run()
