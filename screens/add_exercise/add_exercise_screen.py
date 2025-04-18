from kivymd.app import MDApp
from utils import read_all_exercises

from kivy.properties import StringProperty
from kivymd.uix.list import MDListItem
from kivymd.uix.screen import MDScreen


from kivy.lang.builder import Builder
Builder.load_file("screens/add_exercise/add_exercise_screen.kv")


class ExerciseItem(MDListItem):
    name = StringProperty('')

    def on_press(self):
        app = MDApp.get_running_app()
        if app.previous_screen == "workout":
            app.root.ids.screen_manager.get_screen("workout").workout.append(self.name)
        elif app.previous_screen == "editworkout":
            app.root.ids.screen_manager.get_screen("editworkout").workout.append(self.name)
        app.root.ids.screen_manager.current = app.previous_screen


class AddExerciseScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.all_exercises = read_all_exercises(MDApp.get_running_app().conn_str)
        self.filtered_exercises = self.all_exercises

    def on_pre_enter(self):
        self.populate_list()

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.root.came_from_settings = False
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        app = MDApp.get_running_app()
        app.root.workout_tab_screen = "addexercise"
        return super().on_pre_leave(*args)

    def populate_list(self):
        self.ids.exercise_list.data = [
            {"name": exercise} for exercise in self.filtered_exercises
        ]

    def filter_list(self, search_text):
        self.filtered_exercises = [
            exercise for exercise in self.all_exercises
            if search_text.lower() in exercise.lower()
        ]
        self.populate_list()

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.ids.screen_manager.current = app.previous_screen
