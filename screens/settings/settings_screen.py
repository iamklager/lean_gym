from utils import read_settings, write_setting
from utils import export_user_data, import_user_data

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.widget import MDWidget
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivy.metrics import dp
import os
from datetime import datetime

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
        self.manager_open = False
        self.file_manager_mode = "export"
        self.file_manager = MDFileManager(
            exit_manager = self.exit_manager,
            select_path = self.select_path
        )
        self.setup_platform()

    def setup_platform(self):
        from kivy.utils import platform
        if platform == 'linux':
            import os
            self.default_path = os.path.expanduser("~")
        elif platform == 'android':
            from android.permissions import request_permissions, Permission
            from android.storage import primary_external_storage_path
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            self.default_path = primary_external_storage_path()

    def file_manager_open(self, mode):
        self.file_manager_mode = mode
        self.file_manager.show(
            #os.path.expanduser("~")
            self.default_path
        )
        self.manager_open = True

    def select_path(self, path: str):
        if self.file_manager_mode == "export":
            if not os.path.isdir(path):
                msg_str = "Invalid folder!"
            else:
                file_name = datetime.today().strftime('%Y%m%d_%H%M%S') + "_lean_gym_data.json"
                export_user_data(
                    output_path = path + '/' + file_name,
                    conn_str = self.conn_str
                )
                msg_str = "Data exported!"
        elif self.file_manager_mode == "import":
            if path.endswith("_lean_gym_data.json") and not os.path.isdir(path):
                import_user_data(
                    input_path = path,
                    conn_str = self.conn_str
                )
                msg_str = "Data imported!"
            else:
                msg_str = "Invalid file!"
        self.exit_manager()
        MDSnackbar(
            MDSnackbarText(text=msg_str),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()


    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

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
                spacing=dp(8)
            )
        )
        self.error_message.open()

    def back_btn(self):
        ...
