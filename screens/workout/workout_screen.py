from utils import read_workout, split_exercise_name

from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.list import MDListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.divider import MDDivider

from kivy.lang.builder import Builder
Builder.load_file("screens/workout/workout_screen.kv")


class BodyWeightItem(MDListItem):
    ...


class WorkoutListItem(MDListItem):
    id = StringProperty('')
    name = StringProperty('')
    exercise = StringProperty()
    type = StringProperty()
    hands = StringProperty()

    def on_press(self):
        app = MDApp.get_running_app()
        app.current_exercise = self.name
        app.root.ids.screen_manager.current = "currentexercise"


class AdditionalExercise(MDListItem):
    def on_press(self):
        app = MDApp.get_running_app()
        app.previous_screen = "workout"
        app.root.ids.screen_manager.current = "addexercise"


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

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.root.came_from_settings = False
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        app = MDApp.get_running_app()
        app.root.workout_tab_screen = "workout"
        return super().on_pre_leave(*args)

    def update_workout(self):
        self.ids.workout_list.clear_widgets()
        self.ids.workout_list.add_widget(BodyWeightItem())
        self.ids.workout_list.add_widget(MDDivider())
        for exercise in self.workout:
            self.add_exercise(exercise)
            self.ids.workout_list.add_widget(MDDivider())
        self.ids.workout_list.add_widget(
            AdditionalExercise()
        )
        self.ids.workout_list.add_widget(MDDivider())

    def add_exercise(self, name):
        id = name.lower()
        id = id.replace(" ", "")
        exercise_info = split_exercise_name(name)
        self.ids.workout_list.add_widget(
            WorkoutListItem(
                id=id, name=name, exercise=exercise_info[0],
                type=exercise_info[1], hands=exercise_info[2]
            )
        )

    def finish_workout(self):
        app = MDApp.get_running_app()
        app.current_exercise = ''
        app.current_workout  = ''
        app.root.ids.screen_manager.current = "workouts"

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.ids.screen_manager.current = "workouts"
