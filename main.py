from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from screens import (
    LoginScreen,
    RegisterScreen,
    MainMenuScreen,
    HistoryScreen,
    SettingsScreen,
    UnitSelectionScreen,
    LanguageSelectionScreen,
    SlidersScreen,
    WorkoutDetailsScreen,
    WorkoutTypeScreen,
    PasswordResetScreen
)

class FitnessApp(MDApp):
    """
    Główna klasa aplikacji FitnessApp, która zarządza ekranami i stanem aplikacji.
    """

    def build(self):
        """
        Tworzy i zwraca główny menedżer ekranów aplikacji.

        Returns:
            MDScreenManager: Menedżer ekranów.
        """
        sm = MDScreenManager()
        sm.unit_system = 'metric'
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(UnitSelectionScreen(name='unit_selection'))
        sm.add_widget(LanguageSelectionScreen(name='language_selection'))
        sm.add_widget(SlidersScreen(name='sliders'))
        sm.add_widget(WorkoutDetailsScreen(name='workout_details'))
        sm.add_widget(WorkoutTypeScreen(name='workout_type'))
        sm.add_widget(PasswordResetScreen(name='password_reset'))
        return sm

if __name__ == '__main__':
    FitnessApp().run()
