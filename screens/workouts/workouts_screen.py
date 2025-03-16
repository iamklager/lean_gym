from utils import read_workouts, delete_workout

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivymd.uix.list import MDListItem
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen

from kivy.lang.builder import Builder
Builder.load_file("screens/workouts/workouts_screen.kv")


class WorkoutsListItem(MDListItem):
    # Basic properties
    id           = StringProperty('')
    name         = StringProperty('')
    last_session = StringProperty('')
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
            } for option in ["Edit", "Delete"]
        ]
        self.menu = MDDropdownMenu(
            caller = self,
            items  = menu_items
        )
        self.menu.open()

    def menu_callback(self, option):
        self.menu.dismiss()
        if option == "Edit":
            self.edit_workout()
        elif option == "Delete":
            self.delete_workout()

    def start_workout(self):
        app = MDApp.get_running_app()
        app.current_workout = self.name
        app.root.ids.screen_manager.get_screen("workout").workout = app.current_workout
        app.previous_screen = "workouts"
        app.root.ids.screen_manager.current = "workout"

    def edit_workout(self):
        app = MDApp.get_running_app()
        app.root.ids.screen_manager.get_screen("workouts").workout2edit = self.name
        app.root.ids.screen_manager.current = "editworkout"

    def delete_workout(self):
        app = MDApp.get_running_app()
        delete_workout(self.name, app.conn_str)
        app.root.ids.screen_manager.get_screen("workouts").workouts = read_workouts(app.conn_str)
        app.root.ids.screen_manager.get_screen("workouts").update_workouts()



class WorkoutsScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn_str = MDApp.get_running_app().conn_str
        self.workouts = read_workouts(self.conn_str)
        self.workout2edit = ''

    def after_init(self, dt):
        app = MDApp.get_running_app()
        app.root.came_from_settings = False
        app.root.workout_tab_screen = "workouts"

    def on_pre_leave(self, *args):
        app = MDApp.get_running_app()
        app.root.workout_tab_screen = "workouts"
        return super().on_pre_leave(*args)

    def on_pre_enter(self, *args):
        self.workouts = read_workouts(self.conn_str)
        self.update_workouts()

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        if app.root:
            app.root.came_from_settings = False
        else:
            Clock.schedule_once(self.after_init)
        return super().on_enter(*args)

    def update_workouts(self):
        self.ids.workouts_list.clear_widgets()
        for workout in self.workouts:
            name = workout[0]
            last_session = workout[1]
            id = name.lower()
            id = id.replace(" ", "")
            workout_item = WorkoutsListItem(
                id=id,
                name=name,
                last_session=f"Last session: {last_session}"
            )
            workout_item.bind(on_release=self.item_clicked)
            self.ids.workouts_list.add_widget(workout_item)

    def item_clicked(self, instance):
        instance.start_workout()

    def back_btn(self):
        ...
