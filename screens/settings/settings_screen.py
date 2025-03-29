from utils import read_settings, write_setting

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.widget import MDWidget

from kivy.lang.builder import Builder
Builder.load_file("screens/settings/settings_screen.kv")


def format_pause_time(n):
    minutes = n // 60
    seconds = n - (minutes * 60)
    minutes = str(int(minutes))
    seconds = str(int(seconds))
    minutes = '0' + minutes if len(minutes) == 1 else minutes
    seconds = '0' + seconds if len(seconds) == 1 else seconds
    return minutes, seconds

def unformat_pause_time(minutes, seconds):
    return int(minutes) * 60 + int(seconds)


class PauseTimeSetting(BoxLayout):
    minutes = StringProperty("01")
    seconds = StringProperty("00")

class PauseVibration(BoxLayout):
    is_on = BooleanProperty(True)

class PauseSound(BoxLayout):
    is_on = BooleanProperty(True)


class SettingsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_str = MDApp.get_running_app().conn_str

    def on_pre_enter(self, *args):
        self.settings = read_settings(self.conn_str)
        self.ids.pause_time.minutes, self.ids.pause_time.seconds = format_pause_time(self.settings[0])
        self.ids.pause_vibration.is_on = self.settings[1]
        self.ids.pause_sound.is_on = self.settings[2]
        return super().on_pre_enter(*args)

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.root.came_from_settings = True
        return super().on_enter(*args)

    def update_settings(self):
        self.settings = read_settings(self.conn_str)
        self.ids.pause_time.ids.time_minutes.text, self.ids.pause_time.ids.time_seconds.text = format_pause_time(self.settings[0])
        self.ids.pause_vibration.is_on = self.settings[1]
        self.ids.pause_sound.is_on = self.settings[2]

    def save_settings(self):
        # Pause time
        minutes = self.ids.pause_time.ids.time_minutes.text
        seconds = self.ids.pause_time.ids.time_seconds.text
        if (not minutes.isdigit()) or (not seconds.isdigit()) or (int(minutes) > 59) or (int(seconds) > 59):
            self.show_error_message("Invalid pause time.")
        else:
            write_setting("PauseTime", unformat_pause_time(minutes, seconds), self.conn_str)
        # Pause vibration
        write_setting("PauseVibration", self.ids.pause_vibration.ids.alarm_vibration.active, self.conn_str)
        # Pause sound
        write_setting("PauseSound", self.ids.pause_sound.ids.alarm_sound.active , self.conn_str)
        # Updating settings
        self.update_settings()

    def show_error_message(self, message):
        self.error_message = MDDialog(
            MDDialogHeadlineText(text=message),
            MDDialogButtonContainer(
                MDWidget(),
                MDButton(
                    MDButtonText(text="Ok"),
                    style="text",
                    on_release=lambda _: self.error_message.dismiss()
                ),
                spacing="8dp"
            )
        )
        self.error_message.open()
