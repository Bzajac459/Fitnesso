import unittest
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.base import EventLoop
from screens.settings_screen import SettingsScreen

# Mock screens for testing purposes
class MainMenuScreen(Screen):
    pass

class LanguageSelectionScreen(Screen):
    pass

class UnitSelectionScreen(Screen):
    pass

class TestApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(LanguageSelectionScreen(name='language_selection'))
        sm.add_widget(UnitSelectionScreen(name='unit_selection'))
        return sm

    def on_start(self):
        self.stop()

class TestSettingsScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()
        cls.app.test_mode = True
        EventLoop.ensure_window()
        cls.app.run()
        cls.settings_screen = cls.app.root.get_screen('settings')

    def test_go_back(self):
        self.settings_screen.go_back(None)
        self.assertEqual(self.app.root.current, 'main_menu')

    def test_go_to_language_selection(self):
        self.settings_screen.go_to_language_selection(None)
        self.assertEqual(self.app.root.current, 'language_selection')

    def test_go_to_unit_selection(self):
        self.settings_screen.go_to_unit_selection(None)
        self.assertEqual(self.app.root.current, 'unit_selection')

if __name__ == '__main__':
    unittest.main()
