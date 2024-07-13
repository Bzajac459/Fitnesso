from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from translation_manager import translation_manager


class SettingsScreen(MDScreen):
    """
    Ekran ustawień dla aplikacji fitness.

    Attributes:
        unit_button (MDRaisedButton): Przycisk do wyboru jednostek.
        sliders_button (MDRaisedButton): Przycisk do dostosowania suwaków.
        language_button (MDRaisedButton): Przycisk do wyboru języka.
        back_button (MDRaisedButton): Przycisk powrotu do głównego menu.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran ustawień.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(SettingsScreen, self).__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(1, None))

        self.unit_button = MDRaisedButton(text="", size_hint=(1, None), height=dp(50))
        self.unit_button.bind(on_press=self.go_to_unit_selection)
        translation_manager.register_widget(self.unit_button, 'unit_selection')

        self.sliders_button = MDRaisedButton(text="", size_hint=(1, None), height=dp(50))
        self.sliders_button.bind(on_press=self.go_to_sliders)
        translation_manager.register_widget(self.sliders_button, 'adjust_sliders')

        self.language_button = MDRaisedButton(text="", size_hint=(1, None), height=dp(50))
        self.language_button.bind(on_press=self.go_to_language_selection)
        translation_manager.register_widget(self.language_button, 'language_selection')

        self.back_button = MDRaisedButton(text="", size_hint=(1, None), height=dp(50))
        self.back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(self.back_button, 'back')

        layout.add_widget(self.unit_button)
        layout.add_widget(self.sliders_button)
        layout.add_widget(self.language_button)
        layout.add_widget(self.back_button)

        self.add_widget(layout)

    def go_to_unit_selection(self, instance):
        """
        Przenosi użytkownika do ekranu wyboru jednostek.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'unit_selection'

    def go_to_language_selection(self, instance):
        """
        Przenosi użytkownika do ekranu wyboru języka.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'language_selection'

    def go_to_sliders(self, instance):
        """
        Przenosi użytkownika do ekranu dostosowania suwaków.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'sliders'

    def go_back(self, instance):
        """
        Przenosi użytkownika do głównego menu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'main_menu'
