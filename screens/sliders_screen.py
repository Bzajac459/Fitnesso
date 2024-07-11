from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
import json
import os
from translation_manager import translation_manager

class SlidersScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SlidersScreen, self).__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        self.weight_field = MDTextField(
            hint_text='',
            size_hint=(1, None),
            height=dp(50)
        )
        translation_manager.register_widget(self.weight_field, 'enter_weight', 'hint_text')

        self.height_field = MDTextField(
            hint_text='',
            size_hint=(1, None),
            height=dp(50)
        )
        translation_manager.register_widget(self.height_field, 'enter_height', 'hint_text')

        save_button = MDRaisedButton(
            text='',
            size_hint=(1, None),
            height=dp(50)
        )
        save_button.bind(on_press=self.save_data)
        translation_manager.register_widget(save_button, 'save')

        back_button = MDRaisedButton(
            text='',
            size_hint=(1, None),
            height=dp(50)
        )
        back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(back_button, 'back')

        layout.add_widget(self.weight_field)
        layout.add_widget(self.height_field)
        layout.add_widget(save_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

        # Load data if it exists
        self.load_data()

    def save_data(self, instance):
        weight = self.weight_field.text
        height = self.height_field.text

        if not weight or not height:
            self.show_dialog(translation_manager.get_translation("error"), translation_manager.get_translation("both_fields_required"))
            return

        try:
            weight = float(weight)
            height = float(height)
        except ValueError:
            self.show_dialog(translation_manager.get_translation("error"), translation_manager.get_translation("valid_numbers"))
            return

        data = {
            "weight": weight,
            "height": height
        }

        with open('user_data.json', 'w') as f:
            json.dump(data, f)

        self.show_dialog(translation_manager.get_translation("success"), translation_manager.get_translation("data_saved"))

    def load_data(self):
        if os.path.exists('user_data.json'):
            with open('user_data.json', 'r') as f:
                data = json.load(f)
                self.weight_field.text = str(data.get("weight", ""))
                self.height_field.text = str(data.get("height", ""))

    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(
                    text=translation_manager.get_translation("ok"),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def go_back(self, instance):
        self.manager.current = 'settings'
