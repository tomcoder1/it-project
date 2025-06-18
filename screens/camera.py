from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.app import App
from kivy.lang import Builder
import cv2
import os
import time

from model.model import classify_food
from data import mealstore
from data.data import food, format_name, return_calories

Builder.load_file(os.path.join(os.path.dirname(__file__), '../styles/camera.kv'))

def crop_to_square(frame):
    h, w, _ = frame.shape
    min_dim = min(h, w)
    start_x = (w - min_dim) // 2
    start_y = (h - min_dim) // 2
    return frame[start_y:start_y+min_dim, start_x:start_x+min_dim]

class CameraScreen(Screen):
    def __init__(self, base_dir, **kwargs):
        super().__init__(**kwargs)
        

        self.base_dir = base_dir
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        Clock.schedule_interval(self.update, 1 / 60)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            self.current_frame = frame
            square = crop_to_square(frame)
            buf = cv2.flip(square, -1) 
            buf = cv2.cvtColor(buf, cv2.COLOR_BGR2RGB)
            texture = Texture.create(size=(buf.shape[1], buf.shape[0]), colorfmt='rgb')
            texture.blit_buffer(buf.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.ids.image_widget.texture = texture

    def capture_image(self, instance):
        if hasattr(self, 'current_frame'):
            folder = os.path.join(self.base_dir, "img")
            os.makedirs(folder, exist_ok=True)
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            path = os.path.join(folder, f"photo_{timestamp}.png")
            square = crop_to_square(self.current_frame)
            square = cv2.flip(square, 1)
            success = cv2.imwrite(path, square)

            app = App.get_running_app()
            result_screen = app.sm.get_screen("result")

            if success:
                name = classify_food(path)
                cal = return_calories(name)
                name = format_name(name)
                mealstore.add_meal(name=name, image=path, cal=cal, grams=0)
                result_screen.set_result(f"This is {name}, with {cal} calories per 100 grams.")
            else:
                result_screen.set_result("Failed to save image.")

            app.sm.current = "result"