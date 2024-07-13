import unittest
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from screens.workout_details_screen import WorkoutDetailsScreen

class TestScreenManager(ScreenManager):
    unit_system = "metric"  # przykładowa wartość, dostosuj według potrzeb

class TestApp(MDApp):
    def build(self):
        sm = TestScreenManager()
        sm.add_widget(WorkoutDetailsScreen(name='workout_details'))
        return sm

    def on_start(self):
        self.stop()

class TestWorkoutDetailsScreen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = TestApp()
        cls.app.run()
        cls.workout_details_screen = cls.app.root.get_screen('workout_details')

    def test_reset_stats(self):
        self.workout_details_screen.reset_stats()
        self.assertEqual(self.workout_details_screen.time_row.value.text, '0 s')

    def test_start_workout(self):
        self.workout_details_screen.start_workout('Run')
        self.assertEqual(self.workout_details_screen.type_row.value.text, 'Run')

if __name__ == '__main__':
    unittest.main()
