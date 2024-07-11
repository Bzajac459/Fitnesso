from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from translation_manager import translation_manager

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

        # Tworzenie głównego layoutu
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20, size_hint=(1, None))

        # Tworzenie przycisków
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

        # Dodanie przycisków do layoutu
        layout.add_widget(self.unit_button)
        layout.add_widget(self.sliders_button)
        layout.add_widget(self.language_button)
        layout.add_widget(self.back_button)

        # Dodanie layoutu do ekranu
        self.add_widget(layout)

    def go_to_unit_selection(self, instance):
        self.manager.current = 'unit_selection'

    def go_to_language_selection(self, instance):
        self.manager.current = 'language_selection'

    def go_to_sliders(self, instance):
        self.manager.current = 'sliders'

    def go_back(self, instance):
        self.manager.current = 'main_menu'
