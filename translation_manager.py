import json
import os
from translations import translations

class TranslationManager:
    def __init__(self):
        self.language_file = 'selected_language.json'
        self.current_language = self.load_language()
        self.translations = translations[self.current_language]
        self.widgets_to_update = []

    def set_language(self, lang_code):
        self.current_language = lang_code
        self.translations = translations[lang_code]
        self.save_language(lang_code)
        self.update_all_widgets()

    def get_translation(self, key):
        return self.translations.get(key, key)

    def register_widget(self, widget, translation_key, attribute="text"):
        self.widgets_to_update.append((widget, translation_key, attribute))
        self.update_widget(widget, translation_key, attribute)

    def update_all_widgets(self):
        for widget, translation_key, attribute in self.widgets_to_update:
            self.update_widget(widget, translation_key, attribute)

    def update_widget(self, widget, translation_key, attribute):
        if hasattr(widget, attribute):
            setattr(widget, attribute, self.get_translation(translation_key))

    def save_language(self, lang_code):
        with open(self.language_file, 'w') as f:
            json.dump({'language': lang_code}, f)

    def load_language(self):
        if os.path.exists(self.language_file):
            with open(self.language_file, 'r') as f:
                data = json.load(f)
                return data.get('language', 'en')
        return 'en'

translation_manager = TranslationManager()