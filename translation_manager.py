import json
import os
from translations import translations

class TranslationManager:
    """
    Zarządza tłumaczeniami aplikacji.

    Attributes:
        language_file (str): Ścieżka do pliku z zapisanym językiem.
        current_language (str): Aktualnie ustawiony język.
        translations (dict): Słownik tłumaczeń.
        widgets_to_update (list): Lista widżetów do zaktualizowania.
    """

    def __init__(self):
        """
        Inicjalizuje menedżera tłumaczeń.
        """
        self.language_file = 'selected_language.json'
        self.current_language = self.load_language()
        self.translations = translations[self.current_language]
        self.widgets_to_update = []

    def set_language(self, lang_code):
        """
        Ustawia aktualny język aplikacji.

        Args:
            lang_code (str): Kod języka.
        """
        self.current_language = lang_code
        self.translations = translations[lang_code]
        self.save_language(lang_code)
        self.update_all_widgets()

    def get_translation(self, key):
        """
        Zwraca tłumaczenie dla danego klucza.

        Args:
            key (str): Klucz tłumaczenia.

        Returns:
            str: Tłumaczenie lub sam klucz, jeśli tłumaczenie nie jest dostępne.
        """
        return self.translations.get(key, key)

    def register_widget(self, widget, translation_key, attribute="text"):
        """
        Rejestruje widżet do aktualizacji tłumaczeń.

        Args:
            widget: Widżet do zaktualizowania.
            translation_key (str): Klucz tłumaczenia.
            attribute (str): Atrybut widżetu do zaktualizowania (domyślnie "text").
        """
        self.widgets_to_update.append((widget, translation_key, attribute))
        self.update_widget(widget, translation_key, attribute)

    def update_all_widgets(self):
        """
        Aktualizuje wszystkie zarejestrowane widżety.
        """
        for widget, translation_key, attribute in self.widgets_to_update:
            self.update_widget(widget, translation_key, attribute)

    def update_widget(self, widget, translation_key, attribute):
        """
        Aktualizuje dany widżet tłumaczeniem.

        Args:
            widget: Widżet do zaktualizowania.
            translation_key (str): Klucz tłumaczenia.
            attribute (str): Atrybut widżetu do zaktualizowania.
        """
        if hasattr(widget, attribute):
            setattr(widget, attribute, self.get_translation(translation_key))

    def save_language(self, lang_code):
        """
        Zapisuje aktualny język do pliku.

        Args:
            lang_code (str): Kod języka.
        """
        with open(self.language_file, 'w') as f:
            json.dump({'language': lang_code}, f)

    def load_language(self):
        """
        Ładuje zapisany język z pliku.

        Returns:
            str: Kod języka.
        """
        if os.path.exists(self.language_file):
            with open(self.language_file, 'r') as f:
                data = json.load(f)
                return data.get('language', 'en')
        return 'en'

translation_manager = TranslationManager()
