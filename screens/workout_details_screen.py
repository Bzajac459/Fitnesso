import json
import os
import random
from datetime import datetime
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton, MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivy.metrics import dp
from kivy.clock import Clock
from kivy_garden.mapview import MapView, MapMarker
from kivy_garden.mapview.geojson import GeoJsonMapLayer
from plyer import gps
import platform
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class StatRow(MDBoxLayout):
    """
    Rząd statystyk w aplikacji fitness.

    Attributes:
        icon (MDIconButton): Ikona statystyki.
        label (MDLabel): Etykieta statystyki.
        value (MDLabel): Wartość statystyki.
    """

    def __init__(self, icon, label_text, value_text, **kwargs):
        """
        Inicjalizuje rząd statystyk.

        Args:
            icon (str): Ikona statystyki.
            label_text (str): Tekst etykiety statystyki.
            value_text (str): Wartość statystyki.
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint = (1, None)
        self.height = dp(40)

        self.icon = MDIconButton(icon=icon, icon_size='24sp')
        self.label = MDLabel(text=label_text, bold=True)
        self.value = MDLabel(text=value_text)

        self.add_widget(self.icon)
        self.add_widget(self.label)
        self.add_widget(self.value)


class WorkoutDetailsScreen(Screen):
    """
    Ekran szczegółów treningu w aplikacji fitness.

    Attributes:
        layout (MDBoxLayout): Główny layout ekranu.
        unit_system (str): Aktualnie ustawiony system jednostek.
        map_view (MapView): Widok mapy.
        path_layer (GeoJsonMapLayer): Warstwa ścieżki na mapie.
        stats_layout (GridLayout): Layout statystyk.
        start_button (MDIconButton): Przycisk rozpoczęcia treningu.
        stop_button (MDIconButton): Przycisk zatrzymania treningu.
        cancel_button (MDIconButton): Przycisk anulowania treningu.
        end_button (MDIconButton): Przycisk zakończenia treningu.
        back_button (MDIconButton): Przycisk powrotu do poprzedniego ekranu.
        timer (Clock): Timer do aktualizacji statystyk.
        start_time (float): Czas rozpoczęcia treningu.
        elapsed_time (float): Upłynięty czas treningu.
        workout_type (str): Typ treningu.
        distance (float): Przebyty dystans.
        max_speed (float): Maksymalna prędkość.
        total_speed (float): Łączna prędkość.
        speed_samples (int): Liczba próbek prędkości.
        map_marker (MapMarker): Znacznik na mapie.
        path_coordinates (list): Lista współrzędnych ścieżki.
        met_values (dict): Słownik wartości MET dla różnych typów treningów.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran szczegółów treningu.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.unit_system = 'metric'  # Default unit system, will be updated later

        self.map_view = MapView(zoom=11, lat=52.22977, lon=21.01178, size_hint=(1, None), height=dp(300))
        self.path_layer = GeoJsonMapLayer()
        self.map_view.add_layer(self.path_layer)

        self.layout.add_widget(self.map_view)

        self.stats_layout = GridLayout(cols=3, size_hint=(1, None), spacing=20, padding=20)

        self.type_row = StatRow(icon='run', label_text='Type', value_text='Walk')
        self.time_row = StatRow(icon='clock-outline', label_text='Time', value_text='0 s')
        self.distance_row = StatRow(icon='map-marker-distance', label_text='Distance', value_text='0.00 km')
        self.elevation_row = StatRow(icon='image-filter-hdr', label_text='Elevation Gain', value_text='0.00 m')
        self.max_speed_row = StatRow(icon='speedometer', label_text='Max Speed', value_text='0.00 km/h')
        self.current_speed_row = StatRow(icon='speedometer', label_text='Current Speed', value_text='0.00 km/h')
        self.avg_speed_row = StatRow(icon='speedometer-medium', label_text='Avg Speed', value_text='0.00 km/h')
        self.calories_row = StatRow(icon='fire', label_text='Calories Burned', value_text='0.00 kcal')
        self.hydration_row = StatRow(icon='cup-water', label_text='Hydration Needed', value_text='0.00 L')

        self.stats_layout.add_widget(self.type_row)
        self.stats_layout.add_widget(self.time_row)
        self.stats_layout.add_widget(self.distance_row)
        self.stats_layout.add_widget(self.elevation_row)
        self.stats_layout.add_widget(self.max_speed_row)
        self.stats_layout.add_widget(self.current_speed_row)
        self.stats_layout.add_widget(self.avg_speed_row)
        self.stats_layout.add_widget(self.calories_row)
        self.stats_layout.add_widget(self.hydration_row)

        scroll_view = MDScrollView(size_hint=(1, 1))
        scroll_view.add_widget(self.stats_layout)

        self.layout.add_widget(scroll_view)

        self.start_button = MDIconButton(
            icon='play-circle',
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            on_press=self.start_timer
        )
        self.stop_button = MDIconButton(
            icon='stop-circle',
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            on_press=self.stop_timer
        )
        self.cancel_button = MDIconButton(
            icon='cancel',
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            on_press=self.cancel_workout
        )
        self.end_button = MDIconButton(
            icon='check-circle',
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            on_press=self.end_workout
        )
        self.back_button = MDIconButton(
            icon='arrow-left-circle',
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            on_press=self.go_back
        )

        button_layout = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(60), spacing=10,
                                    padding=dp(20))
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        button_layout.add_widget(self.cancel_button)
        button_layout.add_widget(self.end_button)
        button_layout.add_widget(self.back_button)

        self.layout.add_widget(button_layout)

        self.add_widget(self.layout)

        self.stop_button.disabled = True
        self.cancel_button.disabled = True
        self.end_button.disabled = True

        self.timer = None
        self.start_time = 0
        self.elapsed_time = 0
        self.workout_type = ""
        self.distance = 0
        self.max_speed = 0
        self.total_speed = 0
        self.speed_samples = 0
        self.map_marker = None
        self.path_coordinates = []

        self.met_values = {
            'Walk': 3.8,
            'Run': 7.5,
            'Bike': 7.5,
            'Roller Skate': 7.0,
            'Hiking': 6.0,
            'Scooter': 4.0
        }

        if platform.system() in ['Darwin', 'Linux']:
            gps.configure(on_location=self.update_gps_location)
            gps.start(minTime=1000, minDistance=0)

    def on_pre_enter(self, *args):
        """
        Aktualizuje system jednostek przed wejściem na ekran.

        Args:
            *args: Argumenty przekazane do metody.
        """
        super().on_pre_enter(*args)
        self.unit_system = self.manager.unit_system

    def start_workout(self, workout_type):
        """
        Rozpoczyna trening o podanym typie.

        Args:
            workout_type (str): Typ treningu.
        """
        self.workout_type = workout_type
        self.type_row.value.text = workout_type
        self.update_stats(0)

    def start_timer(self, instance):
        """
        Rozpoczyna timer do aktualizacji statystyk.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.cancel_button.disabled = False
        self.end_button.disabled = False
        self.start_time = Clock.get_boottime()
        self.timer = Clock.schedule_interval(self.update_stats, 1)

    def stop_timer(self, instance):
        """
        Zatrzymuje timer do aktualizacji statystyk.

        Args:
            instance: Instancja wywołująca metodę.
        """
        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.cancel_button.disabled = True
        self.end_button.disabled = True

    def cancel_workout(self, instance):
        """
        Anuluje trening i resetuje statystyki.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.stop_timer(instance)
        self.reset_stats()

    def end_workout(self, instance):
        """
        Kończy trening i wyświetla dialog zapisu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.stop_timer(instance)
        self.show_save_dialog()

    def show_save_dialog(self):
        """
        Wyświetla dialog zapisu treningu.
        """
        self.dialog = MDDialog(
            title="Save Workout",
            text="Do you want to save this workout?",
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=self.dismiss_dialog
                ),
                MDRaisedButton(
                    text="SAVE",
                    on_release=self.save_and_end_workout
                ),
            ],
        )
        self.dialog.open()

    def dismiss_dialog(self, *args):
        """
        Zamyka dialog.

        Args:
            *args: Argumenty przekazane do metody.
        """
        self.dialog.dismiss()

    def save_and_end_workout(self, instance):
        """
        Zapisuje trening i kończy go.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.save_workout()
        self.dismiss_dialog()
        self.reset_stats()
        self.manager.current = 'history'

    def update_stats(self, dt):
        """
        Aktualizuje statystyki treningu.

        Args:
            dt (float): Upłynięty czas od ostatniego wywołania.
        """
        elapsed_time = Clock.get_boottime() - self.start_time
        self.elapsed_time = elapsed_time
        self.time_row.value.text = f'{int(elapsed_time)} s'
        self.distance += random.uniform(0.01, 0.05)
        current_speed = random.uniform(5, 15)
        self.max_speed = max(self.max_speed, current_speed)
        self.total_speed += current_speed
        self.speed_samples += 1
        avg_speed = self.total_speed / self.speed_samples

        weight = 70  # Waga w kg
        met = self.met_values.get(self.workout_type, 8)
        time_in_minutes = elapsed_time / 60
        calories_burned = time_in_minutes * met * weight * 0.0175
        hydration_needed = time_in_minutes * 0.03
        elevation_gain = random.random() * 100

        if self.unit_system == 'imperial':
            distance = self.distance * 0.621371
            current_speed = current_speed * 0.621371
            max_speed = self.max_speed * 0.621371
            avg_speed = avg_speed * 0.621371
            elevation_gain = elevation_gain * 3.28084
        else:
            distance = self.distance
            max_speed = self.max_speed
            avg_speed = self.avg_speed

        self.distance_row.value.text = f'{distance:.2f} {"mi" if self.unit_system == "imperial" else "km"}'
        self.current_speed_row.value.text = f'{current_speed:.2f} {"mph" if self.unit_system == "imperial" else "km/h"}'
        self.max_speed_row.value.text = f'{max_speed:.2f} {"mph" if self.unit_system == "imperial" else "km/h"}'
        self.avg_speed_row.value.text = f'{avg_speed:.2f} {"mph" if self.unit_system == "imperial" else "km/h"}'
        self.calories_row.value.text = f'{calories_burned:.2f} kcal'
        self.hydration_row.value.text = f'{hydration_needed:.2f} L'
        self.elevation_row.value.text = f'{elevation_gain:.2f} {"ft" if self.unit_system == "imperial" else "m"}'

        if platform.system() == 'Windows':
            lat, lon = self.get_random_location()
            if self.map_marker:
                self.map_view.remove_marker(self.map_marker)
            self.map_marker = MapMarker(lat=lat, lon=lon)
            self.map_view.add_marker(self.map_marker)

            self.path_coordinates.append([lon, lat])
            self.update_path_layer()

    def update_gps_location(self, **kwargs):
        """
        Aktualizuje lokalizację GPS.

        Args:
            **kwargs: Argumenty lokalizacji GPS.
        """
        lat = kwargs['lat']
        lon = kwargs['lon']
        if self.map_marker:
            self.map_view.remove_marker(self.map_marker)
        self.map_marker = MapMarker(lat=lat, lon=lon)
        self.map_view.add_marker(self.map_marker)

        self.path_coordinates.append([lon, lat])
        self.update_path_layer()

    def get_random_location(self):
        """
        Generuje losową lokalizację.

        Returns:
            tuple: Współrzędne losowej lokalizacji.
        """
        base_lat, base_lon = 52.22977, 21.01178
        lat = base_lat + random.uniform(-0.001, 0.001)
        lon = base_lon + random.uniform(-0.001, 0.001)
        return lat, lon

    def update_path_layer(self):
        """
        Aktualizuje warstwę ścieżki na mapie.
        """
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": self.path_coordinates
                    },
                    "properties": {
                        "stroke": "#1E90FF",
                        "stroke-width": 2,
                        "stroke-opacity": 1
                    }
                }
            ]
        }
        self.path_layer.geojson = geojson

    def save_workout(self):
        """
        Zapisuje trening do pliku.
        """
        workout_data = {
            "type": self.workout_type,
            "time": int(self.elapsed_time),
            "distance": f'{self.distance:.2f}',
            "calories_burned": f'{float(self.calories_row.value.text.split()[0]):.2f}',
            "avg_speed": f'{float(self.avg_speed_row.value.text.split()[0])::.2f}',
            "max_speed": f'{float(self.max_speed_row.value.text.split()[0])::.2f}',
            "elevation_gain": f'{float(self.elevation_row.value.text.split()[0]):.2f}',
            "hydration_needed": f'{float(self.hydration_row.value.text.split()[0]):.2f}',
            "path_coordinates": self.path_coordinates,
            "date": datetime.now().strftime('%Y-%m-%d')
        }

        if os.path.exists('workout_history.json'):
            with open('workout_history.json', 'r') as f:
                history = json.load(f)
        else:
            history = []

        history.append(workout_data)

        with open('workout_history.json', 'w') as f:
            json.dump(history, f, indent=4)

    def reset_stats(self):
        """
        Resetuje statystyki treningu.
        """
        self.type_row.value.text = ""
        self.time_row.value.text = "0 s"
        self.distance_row.value.text = ""
        self.elevation_row.value.text = ""
        self.max_speed_row.value.text = ""
        self.current_speed_row.value.text = ""
        self.avg_speed_row.value.text = ""
        self.calories_row.value.text = ""
        self.hydration_row.value.text = ""
        self.map_marker = None
        self.path_coordinates = []
        self.update_path_layer()

    def go_back(self, instance):
        """
        Przenosi użytkownika do ekranu wyboru typu treningu.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'workout_type'
