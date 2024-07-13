import unittest
from unittest.mock import patch
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from screens.main_menu_screen import MainMenuScreen

class TestApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(Screen(name='workout_type'))
        sm.add_widget(Screen(name='history'))
        sm.add_widget(Screen(name='settings'))
        return sm

    def on_start(self):
        self.stop()

class TestMainMenuScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()
        cls.app.run()
        cls.main_menu_screen = cls.app.root.get_screen('main_menu')

    def test_go_to_workout(self):
        self.main_menu_screen.go_to_workout(None)
        self.assertEqual(self.app.root.current, 'workout_type')

    def test_go_to_history(self):
        self.main_menu_screen.go_to_history(None)
        self.assertEqual(self.app.root.current, 'history')

    def test_go_to_settings(self):
        self.main_menu_screen.go_to_settings(None)
        self.assertEqual(self.app.root.current, 'settings')

    @patch.object(MDApp, 'stop')
    @patch('kivymd.app.MDApp.get_running_app')
    def test_exit_app(self, mock_get_running_app, mock_stop):
        mock_get_running_app.return_value = self.app
        self.main_menu_screen.exit_app(None)
        mock_stop.assert_called_once()

if __name__ == '__main__':
    unittest.main()
