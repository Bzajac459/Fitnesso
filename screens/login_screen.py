import os
import json
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from translation_manager import translation_manager


class LoginScreen(MDScreen):
    """
    Ekran logowania dla aplikacji fitness.

    Attributes:
        username (MDTextField): Pole tekstowe do wprowadzenia nazwy użytkownika.
        password (MDTextField): Pole tekstowe do wprowadzenia hasła.
        layout (MDBoxLayout): Główny layout ekranu logowania.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran logowania.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
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
        """
        Obsługuje proces logowania użytkownika.

        Args:
            instance: Instancja wywołująca metodę.
        """
        username = self.username.text
        password = self.password.text

        if not username or not password:
            self.show_dialog("Error", "Username and Password are required!")
            return

        file_path = os.path.join(os.path.dirname(__file__), '..', 'users.json')

        if not os.path.exists(file_path):
            self.show_dialog("Error", "Invalid username or password")
            return

        with open(file_path, 'r') as f:
            users = json.load(f)

        for user in users.values():
            if user['username'] == username and user['password'] == password:
                self.manager.current = 'main_menu'
                return

        self.show_dialog("Error", "Invalid username or password")

    def go_to_register(self, instance):
        """
        Przekierowuje użytkownika do ekranu rejestracji.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'register'

    def go_to_password_reset(self, instance):
        """
        Przekierowuje użytkownika do ekranu resetowania hasła.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'password_reset'

    def skip_login(self, instance):
        """
        Pozwala użytkownikowi pominąć logowanie i przejść do głównego menu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'main_menu'

    def show_dialog(self, title, message):
        """
        Wyświetla dialog z podanym tytułem i wiadomością.

        Args:
            title (str): Tytuł dialogu.
            message (str): Treść wiadomości w dialogu.
        """
        dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDRaisedButton(text="Ok", on_press=lambda x: dialog.dismiss())]
        )
        dialog.open()
