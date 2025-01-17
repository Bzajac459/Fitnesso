from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp
from translation_manager import translation_manager


class WorkoutTypeScreen(MDScreen):
    """
    Ekran wyboru typu treningu w aplikacji fitness.

    Attributes:
        workout_buttons (list): Lista przycisków wyboru typu treningu.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran wyboru typu treningu.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(WorkoutTypeScreen, self).__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        workout_types = ['Walk', 'Run', 'Bike', 'Roller Skate', 'Hiking', 'Scooter']

        self.workout_buttons = []
        for workout_type in workout_types:
            button = MDRaisedButton(
                text='',
                size_hint=(1, None),
                height=dp(50)
            )
            button.bind(on_press=lambda x, workout_type=workout_type: self.start_workout(workout_type))
            translation_manager.register_widget(button, workout_type.lower())
            layout.add_widget(button)
            self.workout_buttons.append(button)

        back_button = MDRaisedButton(
            text='',
            size_hint=(1, None),
            height=dp(50)
        )
        back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(back_button, 'back')
        layout.add_widget(back_button)

        self.add_widget(layout)

    def start_workout(self, workout_type):
        """
        Rozpoczyna trening o podanym typie.

        Args:
            workout_type (str): Typ treningu.
        """
        self.manager.get_screen('workout_details').start_workout(workout_type)
        self.manager.current = 'workout_details'

    def go_back(self, instance):
        """
        Przenosi użytkownika do głównego menu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'main_menu'
