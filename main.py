import os
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.transition import MDSlideTransition
from kivy.base import EventLoop
from kivy.core.audio import SoundLoader

from screens import *


from kivy.core.window import Window
Window.size = (400, 780)


class MyScreenManager(MDScreenManager):
    pass


class MyApp(MDApp):
    current_workout:  str
    current_exercise: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_workout  = ''
        self.current_exercise = ''
        self.previous_screen  = '' # To back to the right screen after adding exercises to workouts (either during a workout or in general)
        self.conn_str = os.path.abspath("user.db")
        #self.pause_over_sound = SoundLoader.load(os.path.abspath("alarm_sound.wav"))

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Steelblue"

        sm = MyScreenManager(transition=MDSlideTransition(duration=0))
        sm.add_widget(WorkoutsScreen(name="workouts"))
        sm.add_widget(WorkoutScreen(name="workout"))
        sm.add_widget(CurrentExerciseScreen(name="currentexercise"))
        sm.add_widget(PauseScreen(name="pause"))
        sm.add_widget(EditWorkoutScreen(name="editworkout"))
        sm.add_widget(AddExerciseScreen(name="addexercise"))
        sm.add_widget(BodyWeightScreen(name="bodyweight"))

        return sm

    def on_start(self):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            self.root.get_screen(self.root.current).back_btn()
        return True


if __name__ == "__main__":
    MyApp().run()
