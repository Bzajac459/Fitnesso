import unittest
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from screens.login_screen import LoginScreen
from screens.main_menu_screen import MainMenuScreen


class TestApp(MDApp):
    def build(self):
        self.manager = ScreenManager()
        self.login_screen = LoginScreen(name='login')
        self.main_menu_screen = MainMenuScreen(name='main_menu')
        self.manager.add_widget(self.login_screen)
        self.manager.add_widget(self.main_menu_screen)
        return self.manager

    def stop_app(self, *args):
        self.stop()


class TestLoginScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()
        cls.app_running = False

        # Start the Kivy app in the main thread
        Clock.schedule_once(cls.start_app, 0)

        # Run the Kivy app in the main thread
        cls.app.run()

    @classmethod
    def start_app(cls, dt):
        cls.app_running = True

    @classmethod
    def tearDownClass(cls):
        if cls.app_running:
            cls.app.stop()

    def test_login_empty_fields(self):
        Clock.schedule_once(self._test_login_empty_fields, 0)
        self.app.stop_app()

    def _test_login_empty_fields(self, dt):
        self.app.login_screen.username.text = ''
        self.app.login_screen.password.text = ''
        self.app.login_screen.login(None)
        self.assertEqual(self.app.manager.current, 'login')

    def test_login_failure(self):
        Clock.schedule_once(self._test_login_failure, 0)
        self.app.stop_app()

    def _test_login_failure(self, dt):
        self.app.login_screen.username.text = 'wronguser'
        self.app.login_screen.password.text = 'wrongpassword'
        self.app.login_screen.login(None)
        self.assertEqual(self.app.manager.current, 'login')

    def test_login_success(self):
        Clock.schedule_once(self._test_login_success, 0)
        self.app.stop_app()

    def _test_login_success(self, dt):
        self.app.login_screen.username.text = 'newuser'
        self.app.login_screen.password.text = 'password123'
        self.app.login_screen.login(None)
        self.assertEqual(self.app.manager.current, 'main_menu')


if __name__ == '__main__':
    unittest.main()
