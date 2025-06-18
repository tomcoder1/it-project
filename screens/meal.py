from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from data import mealstore

Builder.load_file('styles/meal.kv')
Builder.load_file('styles/mealgrid.kv')

def calculate_current_calories(grams, cal):
    return round(grams * cal / 100, 2)

class MealScreen(Screen):
    def on_pre_enter(self):
        scroll_layout = self.ids.scroll_layout
        total_label = self.ids.total_calories
        scroll_layout.clear_widgets()

        total = 0
        for meal in mealstore.meal_list:
            item = MealItem(
                data=meal,
                method=lambda data=meal: mealstore.delete_meal(self, data)
            )
            scroll_layout.add_widget(item)
            total += calculate_current_calories(meal.get('grams', 0), meal.get('cal', 0))

        total_label.text = f"Total: {total} calories"

    def go_back(self, instance):
        self.manager.current = "camera"

class MealItem(BoxLayout):
    def __init__(self, data, method, **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.method = method

        self.ids.image.source = data['image']
        self.ids.name.text = data.get('name', 'Unknown')
        self.ids.cal.text = f"{data.get('cal', 0)} calories/100g"
        self.ids.grams.text = f"{data.get('grams', 0)}g"

        curr_cal = calculate_current_calories(data.get('grams', 0), data.get('cal', 0))
        self.ids.curr_cal.text = f"{curr_cal} calories"

        self.ids.delete_btn.bind(on_press=lambda inst: self.method())
