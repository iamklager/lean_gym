from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from plyer.facades.vibrator import Vibrator

from kivy.lang.builder import Builder
Builder.load_file("screens/pause/pause_screen.kv")

def int_to_mmss(n):
    # Assumes we never have pauses > 60min
    mm = n // 60
    ss = n - mm * 60
    mm = f"0{mm}" if mm < 10 else str(mm)
    ss = f"0{ss}" if ss < 10 else str(ss)
    return f"{mm}:{ss}"


class PauseScreen(MDScreen):
    pause_time = NumericProperty(60)
    pause_time_display = StringProperty("01:00")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.pause_over_sound = SoundLoader.load("alarm_sound.wav")

    def on_pre_enter(self, *args):
        self.pause_time = 60 # Store this in a settings table later
        self.pause_time_display = int_to_mmss(self.pause_time)

    def on_enter(self):
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.pause_time -= 1
        self.pause_time_display = int_to_mmss(self.pause_time)
        if self.pause_time == 0:
            #MDApp.get_running_app().pause_over_sound.play()
            try:
                Vibrator().vibrate() # Not yet implemented for linux.
            except NotImplementedError:
                print("plyr Vibrator does not have a linux implementation.")
            app = MDApp.get_running_app()
            app.root.current = "currentexercise"
            Clock.unschedule(self.update_timer)
        return True

    def skip_pause(self):
        app = MDApp.get_running_app()
        Clock.unschedule(self.update_timer)
        app.root.current = "currentexercise"

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.current = "currentexercise"
