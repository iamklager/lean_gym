from utils import (
    read_last_sets, read_new_sets, read_last_exercise_number, read_exercise_units,
    write_new_set, write_last_session, read_exercise_history, plot_exercise_history
)

from kivy.properties import StringProperty, NumericProperty
from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.segmentedbutton import MDSegmentedButton
from kivymd.uix.widget import MDWidget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.lang.builder import Builder
Builder.load_file("screens/current_exercise/current_exercise_screen.kv")


class LastSetItem(MDBoxLayout):
    intensity      = StringProperty('')
    unit_intensity = StringProperty('')
    volume         = StringProperty('')
    unit_volume    = StringProperty('')


class NewSetItem(MDFloatLayout):
    unit_intensity = StringProperty('')
    unit_volume    = StringProperty('')

    def track_set(self):
        intensity = self.ids.new_intensity.text
        volume    = self.ids.new_volume.text
        # Breakout conditions: Wrong input types
        if (intensity == '') or (volume == ''):
            self.show_error_message("New intensity or volumne is empty.")
            return 1
        elif (not intensity.replace('.','',1).lstrip("-").isdigit()) or (not volume.replace('.','',1).lstrip("-").isdigit()):
            self.show_error_message("New intensity or volumne is not a number.")
            return 2
        # Writing the new set to the database
        intensity = float(intensity)
        volume    = float(volume)
        app = MDApp.get_running_app()
        exercise_number = read_last_exercise_number(app.current_workout, app.conn_str) + 1
        write_new_set(
            app.current_workout,
            app.current_exercise,
            exercise_number,
            intensity,
            volume,
            app.conn_str
        )
        # Updating last session for this workout
        write_last_session(app.current_workout, app.conn_str)
        # Updating the UI
        last_sets = read_last_sets(app.current_exercise, app.conn_str)
        if len(last_sets) != 0:
            last_sets = last_sets[len(last_sets) - 1]
            app.root.ids.screen_manager.get_screen("currentexercise").ids.current_set_list.add_widget(
                LastSetItem(
                    intensity      = str(last_sets[0]),
                    unit_intensity = last_sets[1],
                    volume         = str(last_sets[2]),
                    unit_volume    = last_sets[3]
                )
            )
        self.ids.new_intensity.text = ''
        self.ids.new_volume.text    = ''
        # Switching to pause timer
        app.root.ids.screen_manager.current = "pause"
        # Unused return value
        return 0

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
                spacing="8dp"
            )
        )
        self.error_message.open()


class HistoryChoice(MDSegmentedButton):
    def select_last_sets(self):
        scr = MDApp.get_running_app().root.ids.screen_manager.get_screen("currentexercise")
        scr.ids.box_history.height = 0
        scr.ids.box_history.clear_widgets()
        scr.ids.scroll_last_sets.height = scr.height * .4 - scr.ids.exercise_history.height

    def select_history(self):
        scr = MDApp.get_running_app().root.ids.screen_manager.get_screen("currentexercise")
        scr.ids.scroll_last_sets.height = 0
        scr.ids.box_history.height = scr.height * .4 - scr.ids.exercise_history.height
        scr.ids.box_history.clear_widgets()
        scr.ids.box_history.add_widget(FigureCanvasKivyAgg(scr.chart))


class CurrentExerciseScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ...

    def on_pre_enter(self):
        app = MDApp.get_running_app()
        self.last_sets = read_last_sets(app.current_exercise, app.conn_str)
        self.new_sets = read_new_sets(app.current_workout, app.current_exercise, app.conn_str)
        self.populate_last_sets()
        self.populate_new_sets()
        units = read_exercise_units(app.current_exercise, app.conn_str)
        self.ids.new_set_item.unit_intensity = units[0]
        self.ids.new_set_item.unit_volume    = units[1]
        exercise_history = read_exercise_history(app.current_exercise, app.conn_str)
        self.chart = plot_exercise_history(
            exercise_history,
            units[0],
            app.theme_cls.primaryColor,
            app.theme_cls.backgroundColor
        )
        self.ids.box_history.clear_widgets()
        self.ids.box_history.add_widget(FigureCanvasKivyAgg(self.chart))

    def on_enter(self, *args):
        app = MDApp.get_running_app()
        app.root.came_from_settings = False
        return super().on_enter(*args)

    def on_pre_leave(self, *args):
        app = MDApp.get_running_app()
        app.root.workout_tab_screen = "currentexercise"
        return super().on_pre_leave(*args)

    def populate_last_sets(self):
        self.ids.last_set_list.clear_widgets()
        for last_set in self.last_sets:
            self.ids.last_set_list.add_widget(
                LastSetItem(
                    intensity      = str(last_set[0]),
                    unit_intensity = last_set[1],
                    volume         = str(last_set[2]),
                    unit_volume    = last_set[3]
                )
            )

    def populate_new_sets(self):
        self.ids.current_set_list.clear_widgets()
        for new_set in self.new_sets:
            self.ids.current_set_list.add_widget(
                LastSetItem(
                    intensity      = str(new_set[0]),
                    unit_intensity = new_set[1],
                    volume         = str(new_set[2]),
                    unit_volume    = new_set[3]
                )
            )

    def finish_exercise(self):
        app = MDApp.get_running_app()
        app.current_exercise = ''
        app.root.ids.screen_manager.current = "workout"

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.ids.screen_manager.current = "workout"
