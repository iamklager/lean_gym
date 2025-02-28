from utils import write_bodyweight

from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


from kivy.lang.builder import Builder
Builder.load_file("screens/body_weight/body_weight_screen.kv")


class BodyWeightScreen(MDScreen):
    weight = StringProperty('')

    def track_weight(self):
        # Check input type
        weight = self.ids.weight_input.text
        if weight == '':
            print("Weight is empty.")
            return 1
        elif not weight.replace('.','',1).lstrip("-").isdigit():
            print("Weight is not a number.")
            return 2
        weight = float(weight)
        if weight < 0:
            print("Humans cannot have a negative weight.")
            return 3
        # Append weight or overwrite existing weight if already exists.
        app = MDApp.get_running_app()
        write_bodyweight(weight, app.conn_str)
        # Fill text field with tracked weight
        # # Should be default?
        # Update chart
        # Go back to workout screen
        app.root.current = "workout"
        # Success check
        print("tracked weight")
        return 0

    def back_btn(self):
        app = MDApp.get_running_app()
        app.root.current = "workout"
