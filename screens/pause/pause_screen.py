from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import NumericProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from kivy.lang.builder import Builder
Builder.load_file("screens/pause/pause_screen.kv")


class PauseScreen(MDScreen):
    pause_time = NumericProperty(60)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.pause_over_sound = SoundLoader.load('.wav')

    def on_pre_enter(self, *args):
        self.pause_time = 60 # Store this in a settings table later

    def on_enter(self):
        Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.pause_time -= 1
        if self.pause_time == 0:
            #self.pause_over_sound.play()
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
