from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
import os
import json
from translation_manager import translation_manager


class RegisterScreen(MDScreen):
    """
    Ekran rejestracji dla aplikacji fitness.

    Attributes:
        username (MDTextField): Pole tekstowe do wprowadzenia nazwy użytkownika.
        email (MDTextField): Pole tekstowe do wprowadzenia adresu email.
        password (MDTextField): Pole tekstowe do wprowadzenia hasła.
        confirm_password (MDTextField): Pole tekstowe do potwierdzenia hasła.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran rejestracji.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(RegisterScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.username = MDTextField(hint_text='', size_hint=(1, None), height=50)
        translation_manager.register_widget(self.username, 'username', 'hint_text')

        self.email = MDTextField(hint_text='', size_hint=(1, None), height=50)
        translation_manager.register_widget(self.email, 'email', 'hint_text')

        self.password = MDTextField(hint_text='', size_hint=(1, None), height=50, password=True)
        translation_manager.register_widget(self.password, 'password', 'hint_text')

        self.confirm_password = MDTextField(hint_text='', size_hint=(1, None), height=50, password=True)
        translation_manager.register_widget(self.confirm_password, 'confirm_password', 'hint_text')

        register_button = MDRaisedButton(text='', size_hint=(1, None), height=50)
        register_button.bind(on_press=self.register)
        translation_manager.register_widget(register_button, 'register')

        back_button = MDRaisedButton(text='', size_hint=(1, None), height=50)
        back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(back_button, 'back')

        layout.add_widget(self.username)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(self.confirm_password)
        layout.add_widget(register_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def register(self, instance):
        """
        Obsługuje proces rejestracji nowego użytkownika.

        Args:
            instance: Instancja wywołująca metodę.
        """
        username = self.username.text
        email = self.email.text
        password = self.password.text
        confirm_password = self.confirm_password.text

        if not username or not email or not password or not confirm_password:
            self.show_dialog(translation_manager.get_translation("error"),
                             translation_manager.get_translation("all_fields_required"))
            return

        if password != confirm_password:
            self.show_dialog(translation_manager.get_translation("error"),
                             translation_manager.get_translation("passwords_do_not_match"))
            return

        if not os.path.exists('users.json'):
            users = {}
        else:
            with open('users.json', 'r') as f:
                users = json.load(f)

        if email in users:
            self.show_dialog(translation_manager.get_translation("error"),
                             translation_manager.get_translation("email_already_exists"))
            return

        users[email] = {'password': password, 'username': username}

        with open('users.json', 'w') as f:
            json.dump(users, f)

        self.show_dialog(translation_manager.get_translation("success"),
                         translation_manager.get_translation("registration_successful"))
        self.manager.current = 'login'

    def go_back(self, instance):
        """
        Przenosi użytkownika do ekranu logowania.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'login'

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
            buttons=[
                MDRaisedButton(
                    text=translation_manager.get_translation("ok"),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
