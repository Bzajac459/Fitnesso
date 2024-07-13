from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from translation_manager import translation_manager

class LanguageSelectionScreen(MDScreen):
    """
    Ekran wyboru języka aplikacji.

    Attributes:
        label (MDLabel): Etykieta wyboru języka.
        menu (MDDropdownMenu): Menu wyboru języka.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran wyboru języka.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(LanguageSelectionScreen, self).__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.label = MDLabel(text='', halign="center", size_hint=(1, None), height=dp(50))
        translation_manager.register_widget(self.label, 'select_language')

        self.menu_items = [
            {"text": "English"},
            {"text": "Spanish"},
            {"text": "German"},
            {"text": "Polish"},
            {"text": "French"}
        ]

        self.menu = MDDropdownMenu(
            caller=self.label,
            items=[
                {
                    "viewclass": "OneLineListItem",
                    "text": i["text"],
                    "height": dp(56),
                    "on_release": lambda x=i["text"]: self.set_item(x),
                } for i in self.menu_items
            ],
            width_mult=4,
        )

        select_button = MDRaisedButton(text='', size_hint=(1, None), height=dp(50))
        select_button.bind(on_release=lambda x: self.menu.open())
        translation_manager.register_widget(select_button, 'select_language')

        back_button = MDRaisedButton(text='', size_hint=(1, None), height=dp(50))
        back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(back_button, 'back')

        layout.add_widget(self.label)
        layout.add_widget(select_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def set_item(self, text_item):
        """
        Ustawia wybrany język aplikacji.

        Args:
            text_item (str): Nazwa wybranego języka.
        """
        lang_code = 'en'
        if text_item == 'Spanish':
            lang_code = 'es'
        elif text_item == 'German':
            lang_code = 'de'
        elif text_item == 'Polish':
            lang_code = 'pl'
        elif text_item == 'French':
            lang_code = 'fr'

        translation_manager.set_language(lang_code)
        self.label.text = translation_manager.get_translation('selected_language').format(text_item)
        self.menu.dismiss()

    def go_back(self, instance):
        """
        Przenosi użytkownika do ekranu ustawień.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'settings'
