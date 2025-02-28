from utils import read_workout

from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import MDListItem
from kivymd.uix.screen import MDScreen


from kivy.lang.builder import Builder
Builder.load_file("screens/workout/workout_screen.kv")


class BodyWeightItem(MDListItem):
    ...


class WorkoutListItem(MDListItem):
    id = StringProperty('')
    name = StringProperty('')

    def on_press(self):
        app = MDApp.get_running_app()
        app.current_exercise = self.name
        app.root.current = "currentexercise"


class AdditionalExercise(MDListItem):
    def on_press(self):
        app = MDApp.get_running_app()
        app.previous_screen = "workout"
        app.root.current = "addexercise"


class WorkoutScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.workout = []

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        if  app.previous_screen == 'workouts':
            self.workout = read_workout(app.current_workout, app.conn_str)
        else:
            app.previous_screen = ''

        self.update_workout()

    def update_workout(self):
        self.ids.workout_list.clear_widgets()
        self.ids.workout_list.add_widget(BodyWeightItem())
        for exercise in self.workout:
            self.add_exercise(exercise)
        self.ids.workout_list.add_widget(
            AdditionalExercise()
        )

    def add_exercise(self, name):
        id = name.lower()
        id = id.replace(" ", "")
        self.ids.workout_list.add_widget(
            WorkoutListItem(id=id, name=name)
        )

    def finish_workout(self):
        app = MDApp.get_running_app()
        app.current_exercise = ''
        app.current_workout  = ''
        app.root.current = "workouts"

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.current = "workouts"
