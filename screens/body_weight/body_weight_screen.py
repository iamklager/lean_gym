from utils import read_weight_history, write_bodyweight, plot_weight_history

from kivy_garden.matplotlib import FigureCanvasKivyAgg
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.widget import MDWidget
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogButtonContainer


from kivy.lang.builder import Builder
Builder.load_file("screens/body_weight/body_weight_screen.kv")


class BodyWeightScreen(MDScreen):
    weight = StringProperty('')

    def on_pre_enter(self, *args):
        self.plot_chart()
        return super().on_pre_enter(*args)

    def track_weight(self):
        # Check input type
        weight = self.ids.weight_input.text
        if weight == '':
            self.show_error_message("Weight is empty.")
            return 1
        elif not weight.replace('.','',1).lstrip("-").isdigit():
            self.show_error_message("Weight is not a number.")
            return 2
        weight = float(weight)
        if weight < 0:
            self.show_error_message("Humans cannot have a negative weight.")
            return 3
        # Append weight or overwrite existing weight if already exists.
        app = MDApp.get_running_app()
        write_bodyweight(weight, app.conn_str)
        # Fill text field with tracked weight
        # # Should be default?
        # Update chart
        self.plot_chart()
        # Go back to workout screen
        app.root.current = "workout"
        # Success check
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

    def plot_chart(self):
        app = MDApp.get_running_app()
        history = read_weight_history(app.conn_str)
        chart = plot_weight_history(
            history,
            app.theme_cls.primaryColor,
            app.theme_cls.backgroundColor
        )
        self.ids.weight_history.clear_widgets()
        self.ids.weight_history.add_widget(
            FigureCanvasKivyAgg(chart)
        )

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.current = "workout"
