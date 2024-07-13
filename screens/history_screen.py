import json
import os
from datetime import datetime, timedelta

from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, ThreeLineAvatarIconListItem, ILeftBody
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivymd.uix.selectioncontrol import MDCheckbox
from translation_manager import translation_manager

class HistoryScreen(MDScreen):
    """
    Ekran historii treningów aplikacji.

    Attributes:
        back_button (MDRaisedButton): Przycisk powrotu do głównego menu.
        filter_buttons (list): Lista przycisków do filtrowania historii.
        list_view (MDList): Widok listy historii treningów.
        selected_workouts (list): Lista wybranych treningów.
        history (list): Lista wszystkich treningów.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran historii treningów.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(HistoryScreen, self).__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical')

        self.back_button = MDRaisedButton(text='', size_hint=(1, None), height=dp(50))
        self.back_button.bind(on_press=self.go_back)
        layout.add_widget(self.back_button)
        translation_manager.register_widget(self.back_button, 'back')

        filter_layout = MDBoxLayout(size_hint=(1, None), height=dp(50))
        self.filter_buttons = [
            MDRaisedButton(text=translation_manager.get_translation('last_week'), on_press=lambda x: self.filter_history('week')),
            MDRaisedButton(text=translation_manager.get_translation('last_month'), on_press=lambda x: self.filter_history('month')),
            MDRaisedButton(text=translation_manager.get_translation('last_year'), on_press=lambda x: self.filter_history('year')),
            MDRaisedButton(text=translation_manager.get_translation('all'), on_press=lambda x: self.filter_history('all'))
        ]
        for button in self.filter_buttons:
            filter_layout.add_widget(button)
        layout.add_widget(filter_layout)

        scroll_view = MDScrollView()
        self.list_view = MDList()
        scroll_view.add_widget(self.list_view)
        layout.add_widget(scroll_view)

        delete_button = MDRaisedButton(text=translation_manager.get_translation('delete_selected'), size_hint=(1, None), height=dp(50))
        delete_button.bind(on_press=self.delete_selected_workouts)
        layout.add_widget(delete_button)

        self.add_widget(layout)

        self.selected_workouts = []
        self.history = []
        self.load_history()

    def on_pre_enter(self):
        """
        Ładuje historię treningów przed wejściem na ekran.
        """
        super().on_pre_enter()
        self.load_history()

    def go_back(self, instance):
        """
        Przenosi użytkownika do głównego menu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'main_menu'

    def load_history(self):
        """
        Ładuje historię treningów z pliku.
        """
        self.list_view.clear_widgets()
        if not os.path.exists('workout_history.json'):
            return

        with open('workout_history.json', 'r') as f:
            self.history = json.load(f)

        for workout in self.history:
            self.add_workout_to_list(workout)

    def add_workout_to_list(self, workout):
        """
        Dodaje trening do widoku listy.

        Args:
            workout (dict): Dane treningu.
        """
        item = WorkoutListItem(workout=workout, screen=self)
        self.list_view.add_widget(item)

    def show_workout_details(self, workout):
        """
        Wyświetla szczegóły wybranego treningu.

        Args:
            workout (dict): Dane treningu.
        """
        workout_details = (
            f"{translation_manager.get_translation('type')}: {workout['type']}\n"
            f"{translation_manager.get_translation('time')}: {workout['time']} s\n"
            f"{translation_manager.get_translation('distance')}: {workout['distance']} km\n"
            f"{translation_manager.get_translation('calories_burned')}: {workout['calories_burned']} kcal\n"
            f"{translation_manager.get_translation('avg_speed')}: {workout['avg_speed']} km/h\n"
            f"{translation_manager.get_translation('max_speed')}: {workout['max_speed']} km/h\n"
            f"{translation_manager.get_translation('elevation_gain')}: {workout['elevation_gain']} m\n"
            f"{translation_manager.get_translation('hydration_needed')}: {workout['hydration_needed']} L"
        )

        dialog = MDDialog(
            title=translation_manager.get_translation("workout_details"),
            text=workout_details,
            size_hint=(0.8, 0.4),
            buttons=[
                MDRaisedButton(
                    text=translation_manager.get_translation("close"),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def filter_history(self, period):
        """
        Filtruje historię treningów według podanego okresu.

        Args:
            period (str): Okres filtrowania ('week', 'month', 'year', 'all').
        """
        filtered_history = []
        now = datetime.now()

        if period == 'week':
            filtered_history = [w for w in self.history if now - datetime.strptime(w['date'], '%Y-%m-%d') <= timedelta(weeks=1)]
        elif period == 'month':
            filtered_history = [w for w in self.history if now - datetime.strptime(w['date'], '%Y-%m-%d') <= timedelta(days=30)]
        elif period == 'year':
            filtered_history = [w for w in self.history if now - datetime.strptime(w['date'], '%Y-%m-%d') <= timedelta(days=365)]
        else:
            filtered_history = self.history

        self.list_view.clear_widgets()
        for workout in filtered_history:
            self.add_workout_to_list(workout)

    def delete_selected_workouts(self, instance):
        """
        Usuwa wybrane treningi z historii.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.history = [w for w in self.history if w not in self.selected_workouts]
        with open('workout_history.json', 'w') as f:
            json.dump(self.history, f, indent=4)
        self.load_history()

    def toggle_select_workout(self, workout):
        """
        Zaznacza lub odznacza trening w historii.

        Args:
            workout (dict): Dane treningu.
        """
        if workout in self.selected_workouts:
            self.selected_workouts.remove(workout)
        else:
            self.selected_workouts.append(workout)

class WorkoutListItem(ThreeLineAvatarIconListItem):
    """
    Element listy treningów w historii.

    Attributes:
        workout (dict): Dane treningu.
        screen (HistoryScreen): Instancja ekranu historii.
        checkbox (WorkoutCheckbox): Checkbox do zaznaczania treningu.
    """

    def __init__(self, workout, screen, **kwargs):
        """
        Inicjalizuje element listy treningów.

        Args:
            workout (dict): Dane treningu.
            screen (HistoryScreen): Instancja ekranu historii.
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super().__init__(**kwargs)
        self.workout = workout
        self.screen = screen
        self.text = f"{translation_manager.get_translation('type')}: {workout['type']}"
        self.secondary_text = f"{translation_manager.get_translation('distance')}: {workout['distance']} km, {translation_manager.get_translation('time')}: {workout['time']} s"
        self.tertiary_text = f"{translation_manager.get_translation('calories_burned')}: {workout['calories_burned']}, {translation_manager.get_translation('avg_speed')}: {workout['avg_speed']} km/h"

        self.checkbox = WorkoutCheckbox(self)
        self.add_widget(self.checkbox)

    def on_release(self):
        """
        Wyświetla szczegóły treningu po kliknięciu na element listy.
        """
        if not self.checkbox.active:
            self.screen.show_workout_details(self.workout)

class WorkoutCheckbox(ILeftBody, MDCheckbox):
    """
    Checkbox do zaznaczania treningów w historii.

    Attributes:
        list_item (WorkoutListItem): Element listy treningów.
    """

    def __init__(self, list_item, **kwargs):
        """
        Inicjalizuje checkbox.

        Args:
            list_item (WorkoutListItem): Element listy treningów.
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super().__init__(**kwargs)
        self.list_item = list_item
        self.bind(active=self.on_checkbox_active)

    def on_checkbox_active(self, checkbox, value):
        """
        Obsługuje zmianę stanu checkboxa.

        Args:
            checkbox (MDCheckbox): Instancja checkboxa.
            value (bool): Nowy stan checkboxa.
        """
        self.list_item.screen.toggle_select_workout(self.list_item.workout)
