from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from translation_manager import translation_manager


class UnitSelectionScreen(MDScreen):
    """
    Ekran wyboru jednostek dla aplikacji fitness.

    Attributes:
        unit_switch (MDSwitch): Przełącznik jednostek metrycznych i imperialnych.
    """

    def __init__(self, **kwargs):
        """
        Inicjalizuje ekran wyboru jednostek.

        Args:
            **kwargs: Słownik argumentów przekazanych do konstruktora.
        """
        super(UnitSelectionScreen, self).__init__(**kwargs)

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=20)

        unit_label = MDLabel(text="", halign="center")
        translation_manager.register_widget(unit_label, 'select_units')

        self.unit_switch = MDSwitch()
        self.unit_switch.bind(active=self.on_unit_switch_active)

        unit_layout = MDBoxLayout(orientation='horizontal', padding=20, spacing=20)
        unit_layout.add_widget(MDLabel(text="Metric", halign="center"))
        unit_layout.add_widget(self.unit_switch)
        unit_layout.add_widget(MDLabel(text="Imperial", halign="center"))

        back_button = MDRaisedButton(text='', size_hint=(1, None), height=dp(50))
        back_button.bind(on_press=self.go_back)
        translation_manager.register_widget(back_button, 'back')

        layout.add_widget(unit_label)
        layout.add_widget(unit_layout)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def on_unit_switch_active(self, switch, value):
        """
        Obsługuje zmianę jednostek.

        Args:
            switch (MDSwitch): Przełącznik jednostek.
            value (bool): Nowy stan przełącznika.
        """
        unit = "imperial" if value else "metric"
        self.manager.unit_system = unit
        print(f"Selected unit: {unit}")

    def go_back(self, instance):
        """
        Przenosi użytkownika do ekranu ustawień.

        Args:
            instance: Instancja wywołująca metodę.
        """
        self.manager.current = 'settings'
