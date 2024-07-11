from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.boxlayout import BoxLayout
from translation_manager import translation_manager


class MainMenuScreen(MDScreen):
    def __init__(self, **kwargs):
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

    def update_texts(self, translations):
        self.welcome_label.text = translations['welcome']
        self.start_workout_button.text = translations['workout']
        self.history_button.text = translations['history']
        self.settings_button.text = translations['settings']
        self.exit_button.text = translations['exit']

    def go_to_workout(self, instance):
        self.manager.current = 'workout_type'

    def go_to_history(self, instance):
        self.manager.current = 'history'

    def go_to_settings(self, instance):
        self.manager.current = 'settings'

    def exit_app(self, instance):
        MDApp.get_running_app().stop()
