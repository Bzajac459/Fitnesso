from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
import os
import json
from translation_manager import translation_manager


class PasswordResetScreen(MDScreen):
    """
    Ekran resetowania hasła dla aplikacji fitness.

    Attributes:
        email (MDTextField): Pole tekstowe do wprowadzenia adresu email.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran resetowania hasła.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(PasswordResetScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.email = MDTextField(hint_text='', size_hint=(1, None), height=dp(50))
        translation_manager.register_widget(self.email, 'email', 'hint_text')

        reset_button = MDRaisedButton(text='', size_hint=(1, None), height=dp(50))
        reset_button.bind(on_press=self.reset_password)
        translation_manager.register_widget(reset_button, 'reset_password')

        back_button = MDRaisedButton(text='', size_hint=(1, None), height=dp(50))
        back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(back_button, 'back')

        layout.add_widget(self.email)
        layout.add_widget(reset_button)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def reset_password(self, instance):
        """
        Obsługuje proces resetowania hasła.

        Args:
            instance: Instancja wywołująca metodę.
        """
        email = self.email.text
        if not email:
            self.show_error_dialog(translation_manager.get_translation("email_empty"))
            return

        if self.email_exists(email):
            self.show_message_dialog(translation_manager.get_translation("reset_instructions_sent"))
        else:
            self.show_error_dialog(translation_manager.get_translation("email_not_found"))

    def email_exists(self, email):
        """
        Sprawdza, czy podany email istnieje w bazie użytkowników.

        Args:
            email (str): Adres email użytkownika.

        Returns:
            bool: True jeśli email istnieje, False w przeciwnym razie.
        """
        if not os.path.exists('users.json'):
            return False
        with open('users.json', 'r') as f:
            users = json.load(f)
        return email in users

    def go_back(self, instance):
        """
        Przenosi użytkownika do ekranu logowania.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'login'

    def show_error_dialog(self, message):
        """
        Wyświetla dialog błędu z podaną wiadomością.

        Args:
            message (str): Treść wiadomości błędu.
        """
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text=translation_manager.get_translation("ok"),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def show_message_dialog(self, message):
        """
        Wyświetla dialog z podaną wiadomością.

        Args:
            message (str): Treść wiadomości.
        """
        dialog = MDDialog(
            text=message,
            buttons=[
                MDRaisedButton(
                    text=translation_manager.get_translation("ok"),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()
