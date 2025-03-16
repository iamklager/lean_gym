from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.transition import MDSlideTransition
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.app import MDApp

from kivy.lang.builder import Builder
Builder.load_file("smanager/smanager.kv")


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class SManager(MDBoxLayout):
    workout_tab_screen = StringProperty("workouts")
    came_from_settings = False

    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
    ):
        print("Start tab logic")
        print(self.came_from_settings)
        if item_text == "Workout":
            if self.came_from_settings == True:
                self.ids.screen_manager.transition = MDSlideTransition(direction="right")
                self.ids.screen_manager.current = self.workout_tab_screen
                self.ids.screen_manager.transition = MDSlideTransition(duration=0)
        elif item_text == "Settings":
            if self.came_from_settings == False:
                self.ids.screen_manager.transition = MDSlideTransition(direction="left")
                self.ids.screen_manager.current = "settings"
        print("End tab logic")
        print(self.came_from_settings)
