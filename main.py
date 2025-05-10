import os
from kivymd.app import MDApp
from smanager.smanager import SManager
from kivy.base import EventLoop
from kivy.core.audio import SoundLoader

from screens import *


from kivy.core.window import Window
Window.size = (300, 680)


class MyApp(MDApp):
    current_workout:  str
    current_exercise: str
    previous_screen: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_workout  = ''
        self.current_exercise = ''
        self.previous_screen  = '' # To go back to the right screen after adding exercises to workouts (either during a workout or in general)
        self.conn_str = os.path.abspath("user.db")
        #self.pause_over_sound = SoundLoader.load(os.path.abspath("alarm_sound.wav")) # Does not work with kivymd for some reason.

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Steelblue"

        sm = SManager()
        sm.ids.screen_manager.add_widget(WorkoutsScreen(name="workouts"))
        sm.ids.screen_manager.add_widget(WorkoutScreen(name="workout"))
        sm.ids.screen_manager.add_widget(CurrentExerciseScreen(name="currentexercise"))
        sm.ids.screen_manager.add_widget(PauseScreen(name="pause"))
        sm.ids.screen_manager.add_widget(EditWorkoutScreen(name="editworkout"))
        sm.ids.screen_manager.add_widget(AddExerciseScreen(name="addexercise"))
        sm.ids.screen_manager.add_widget(BodyWeightScreen(name="bodyweight"))
        sm.ids.screen_manager.add_widget(SettingsScreen(name="settings"))

        return sm

    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.root.ids.screen_manager.get_screen(self.root.ids.screen_manager.current).back_btn()
        return True


if __name__ == "__main__":
    MyApp().run()
