from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from translation_manager import translation_manager


class MainMenuScreen(MDScreen):
    """
    Główne menu aplikacji fitness.

    Attributes:
        welcome_label (MDLabel): Etykieta powitalna.
        start_workout_button (MDRaisedButton): Przycisk do rozpoczęcia treningu.
        history_button (MDRaisedButton): Przycisk do przeglądania historii treningów.
        settings_button (MDRaisedButton): Przycisk do otwierania ustawień.
        exit_button (MDRaisedButton): Przycisk do wyjścia z aplikacji.
        layout (BoxLayout): Główny layout ekranu menu.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje główne menu aplikacji.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.welcome_label = MDLabel(text='', halign="center", size_hint=(1, None), height=50)
        translation_manager.register_widget(self.welcome_label, 'welcome')

        self.start_workout_button = MDRaisedButton(text='', size_hint=(1, None), height=50, on_press=self.go_to_workout)
        translation_manager.register_widget(self.start_workout_button, 'workout')

        self.history_button = MDRaisedButton(text='', size_hint=(1, None), height=50, on_press=self.go_to_history)
        translation_manager.register_widget(self.history_button, 'history')

        self.settings_button = MDRaisedButton(text='', size_hint=(1, None), height=50, on_press=self.go_to_settings)
        translation_manager.register_widget(self.settings_button, 'settings')

        self.exit_button = MDRaisedButton(text='', size_hint=(1, None), height=50, on_press=self.exit_app)
        translation_manager.register_widget(self.exit_button, 'exit')

        self.layout.add_widget(self.welcome_label)
        self.layout.add_widget(self.start_workout_button)
        self.layout.add_widget(self.history_button)
        self.layout.add_widget(self.settings_button)
        self.layout.add_widget(self.exit_button)
        self.add_widget(self.layout)

    def go_to_workout(self, instance):
        """
        Przenosi użytkownika do ekranu wyboru typu treningu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'workout_type'

    def go_to_history(self, instance):
        """
        Przenosi użytkownika do ekranu historii treningów.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'history'

    def go_to_settings(self, instance):
        """
        Przenosi użytkownika do ekranu ustawień.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'settings'

    def exit_app(self, instance):
        """
        Zamyka aplikację.

        Args:
            instance: Instancja wywołująca metodę.
        """
        MDApp.get_running_app().stop()
