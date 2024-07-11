from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
import os
import json
from translation_manager import translation_manager

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.username = MDTextField(hint_text='', size_hint=(1, None), height=50)
        translation_manager.register_widget(self.username, 'username', 'hint_text')

        self.password = MDTextField(hint_text='', size_hint=(1, None), height=50, password=True)
        translation_manager.register_widget(self.password, 'password', 'hint_text')

        login_button = MDRaisedButton(text='', size_hint=(1, None), height=50)
        login_button.bind(on_press=self.login)
        translation_manager.register_widget(login_button, 'login')

        register_button = MDRaisedButton(text='', size_hint=(1, None), height=50)
        register_button.bind(on_press=self.go_to_register)
        translation_manager.register_widget(register_button, 'register')

        forgot_password_button = MDRaisedButton(text='', size_hint=(1, None), height=50)
        forgot_password_button.bind(on_press=self.go_to_password_reset)
        translation_manager.register_widget(forgot_password_button, 'forgot_password')

        skip_login_button = MDRaisedButton(text='', size_hint=(1, None), height=50)
        skip_login_button.bind(on_press=self.skip_login)
        translation_manager.register_widget(skip_login_button, 'skip_login')

        self.layout.add_widget(self.username)
        self.layout.add_widget(self.password)
        self.layout.add_widget(login_button)
        self.layout.add_widget(register_button)
        self.layout.add_widget(forgot_password_button)
        self.layout.add_widget(skip_login_button)
        self.add_widget(self.layout)

    def login(self, instance):
        username = self.username.text
        password = self.password.text

        if not username or not password:
            self.show_dialog("Error", "Username and Password are required!")
            return

        if not os.path.exists('users.json'):
            self.show_dialog("Error", "Invalid username or password")
            return

        with open('users.json', 'r') as f:
            users = json.load(f)

        for user in users.values():
            if user['username'] == username and user['password'] == password:
                self.manager.current = 'main_menu'
                return

        self.show_dialog("Error", "Invalid username or password")

    def go_to_register(self, instance):
        self.manager.current = 'register'

    def go_to_password_reset(self, instance):
        self.manager.current = 'password_reset'

    def skip_login(self, instance):
        self.manager.current = 'main_menu'

    def show_dialog(self, title, message):
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDRaisedButton(text="Ok", on_press=lambda x: dialog.dismiss())]
        )
        dialog.open()

    def update_texts(self, translations):
        self.username.hint_text = translations['username']
        self.password.hint_text = translations['password']
        self.layout.children[5].text = translations['login']
        self.layout.children[4].text = translations['register']
        self.layout.children[3].text = translations['forgot_password']
        self.layout.children[2].text = translations['skip_login']
