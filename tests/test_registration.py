import unittest
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.clock import mainthread
from screens.register_screen import RegisterScreen

class TestApp(MDApp):
    def build(self):
        sm = ScreenManager()
        self.register_screen = RegisterScreen(name='register')
        sm.add_widget(self.register_screen)
        return sm

    def on_start(self):
        self.stop()

class TestRegisterScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()
        cls.app.run()

    def setUp(self):
        self.register_screen = self.app.register_screen

    @mainthread
    def test_register_empty_fields(self):
        self.register_screen.username.text = ''
        self.register_screen.email.text = ''
        self.register_screen.password.text = ''
        self.register_screen.confirm_password.text = ''
        self.register_screen.register(None)
        self.assertEqual(self.register_screen.dialog.title, 'Error')

    @mainthread
    def test_register_password_mismatch(self):
        self.register_screen.username.text = 'newuser'
        self.register_screen.email.text = 'newuser@example.com'
        self.register_screen.password.text = 'password123'
        self.register_screen.confirm_password.text = 'password321'
        self.register_screen.register(None)
        self.assertEqual(self.register_screen.dialog.title, 'Error')

    @mainthread
    def test_register_success(self):
        self.register_screen.username.text = 'newuser'
        self.register_screen.email.text = 'newuser@example.com'
        self.register_screen.password.text = 'password123'
        self.register_screen.confirm_password.text = 'password123'
        self.register_screen.register(None)
        self.assertEqual(self.app.root.current, 'login')

if __name__ == '__main__':
    unittest.main()
