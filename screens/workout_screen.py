from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from translation_manager import translation_manager


class WorkoutScreen(MDScreen):
    """
    Ekran treningu w aplikacji fitness.

    Attributes:
        layout (MDBoxLayout): Główny layout ekranu.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran treningu.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(WorkoutScreen, self).__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        workout_label = MDLabel(
            text="",
            halign='center',
            size_hint=(1, None),
            height=dp(50)
        )
        translation_manager.register_widget(workout_label, 'workout_screen')

        back_button = MDRaisedButton(
            text='',
            size_hint=(1, None),
            height=dp(50)
        )
        back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(back_button, 'back_to_menu')

        layout.add_widget(workout_label)
        layout.add_widget(back_button)
        self.add_widget(layout)

    def go_back(self, instance):
        """
        Przenosi użytkownika do głównego menu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'main_menu'
