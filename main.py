from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
import os

from screens.camera import CameraScreen
from screens.results import ResultScreen
from screens.meal import MealScreen

from kivy.clock import Clock

class CameraApp(App):
    def build(self):
        self.sm = ScreenManager(transition=FadeTransition(duration=0.05))
        self.sm.add_widget(CameraScreen(name="camera", base_dir=os.path.dirname(__file__)))
        self.sm.add_widget(ResultScreen(name="result"))
        self.sm.add_widget(MealScreen(name="meal"))
        return self.sm

if __name__ == '__main__':
    CameraApp().run()