from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from kivy.lang.builder import Builder
Builder.load_file("screens/settings/settings_screen.kv")

class SettingsScreen(MDScreen):
    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.root.came_from_settings = True
        return super().on_enter(*args)

    def back_btn(self):
        ...
