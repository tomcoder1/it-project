from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

from data import mealstore

Builder.load_file('styles/results.kv')

class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_result(self, text):
        self.ids.result_label.text = text
        self.ids.grams_input.text = ""

    def to_meal(self, instance):
        try:
            grams = int(self.ids.grams_input.text)
            if mealstore.meal_list:
                mealstore.meal_list[-1]["grams"] = grams
        except:
            pass

        self.manager.get_screen("meal").on_pre_enter()
        self.manager.current = "meal"

    def go_back(self, instance):
        self.manager.current = "camera"
        if mealstore.meal_list:
            mealstore.delete_meal(self, mealstore.meal_list[-1])