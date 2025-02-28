from utils import add_workout, read_workout, delete_exercise_from_workout, read_workouts, rename_workout, add_exercise_to_workout

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.list import MDListItem
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen


from kivy.lang.builder import Builder
Builder.load_file("screens/edit_workout/edit_workout_screen.kv")


class ExerciseListItem(MDListItem):
    # Basic properties
    name = StringProperty('')
    # Short and long press properties
    long_press_time    = .5
    long_press_trigger = None
    long_pressed       = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.long_pressed = False
            self.long_press_trigger = Clock.schedule_once(
                self.do_long_press,
                self.long_press_time
            )
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.long_press_trigger:
            self.long_press_trigger.cancel()
            self.long_press_trigger = None
        if self.long_pressed:
            self.long_pressed = False
            return True
        return super().on_touch_up(touch)

    def do_long_press(self, dt):
        self.long_pressed = True
        self.open_menu()

    def open_menu(self):
        menu_items =[
            {
                "text": option,
                "on_release": lambda x = option: self.menu_callback(x),
            } for option in ["Delete"]
        ]
        self.menu = MDDropdownMenu(
            caller = self,
            items  = menu_items
        )
        self.menu.open()

    def menu_callback(self, option):
        self.menu.dismiss()
        app = MDApp.get_running_app()
        app.root.get_screen("editworkout").workout.remove(self.name)
        app.root.get_screen("editworkout").update_exercises()


class AdditionalExercise(MDListItem):
    def on_press(self):
        app = MDApp.get_running_app()
        app.previous_screen = "editworkout"
        app.root.current = "addexercise"


class EditWorkoutScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_workout, self.workout = [], []
        self.is_editing = False

    def on_pre_enter(self, *args):
        app = MDApp.get_running_app()
        self.workout2edit = app.root.get_screen("workouts").workout2edit
        self.back_screen = "workouts"
        if self.workout2edit != '' and not self.is_editing:
            self.back_screen = self.workout2edit
            self.workout = read_workout(self.workout2edit, app.conn_str)
            self.old_workout = self.workout.copy()
            self.ids.workout_name.text = self.workout2edit
            self.is_editing = True
        self.update_exercises()

    def update_exercises(self):
        self.ids.exercise_list.clear_widgets()
        for exercise in self.workout:
            exercise_item = ExerciseListItem(name=exercise)
            exercise_item.bind(on_release=self.item_clicked)
            self.ids.exercise_list.add_widget(exercise_item)
        self.ids.exercise_list.add_widget(AdditionalExercise())

    def item_clicked(self, instance):
        ...

    def save_workout(self):
        app = MDApp.get_running_app()
        # Workout name check
        workout_name = self.ids.workout_name.text
        workout_name = workout_name.strip()
        if workout_name == '':
            print("Workout name cannot be empty.")
            return 1

        if self.workout2edit == '':
            workouts = read_workouts(app.conn_str)
            workouts = [workout[0] for workout in workouts]
            if workout_name in workouts:
                print(f"Workout {workout_name} already exists.")
                return 2
            add_workout(workout_name, app.conn_str)

        else:
            if self.ids.workout_name.text != self.workout2edit:
                rename_workout(self.ids.workout_name.text, self.workout2edit, app.conn_str)
        add_exercises = [new for new in self.workout     if new not in self.old_workout]
        rem_exercises = [old for old in self.old_workout if old not in self.workout]
        for new in add_exercises:
            add_exercise_to_workout(new, self.ids.workout_name.text, app.conn_str)
        for old in rem_exercises:
            delete_exercise_from_workout(old, self.ids.workout_name.text, app.conn_str)
        self.is_editing = False
        app.root.current = "workouts"

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.current = "workouts"
