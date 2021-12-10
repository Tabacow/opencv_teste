import time
from pynput.mouse import Button, Controller as MouseController
import pyautogui
from random import random
class Controller:
    def __init__(self):
        self.mouse = MouseController()

    def move_to_with_randomness(self, x,y,t=0.5): #função roubada do mpcabete, valeu! https://github.com/mpcabete/bombcrypto-bot
        pyautogui.moveTo(self.add_randomness(x,10),self.add_randomness(y,10),t+random()/2)

    def add_randomness(self, n, randomn_factor_size=None): #função roubada do mpcabete, valeu! https://github.com/mpcabete/bombcrypto-bot
        if randomn_factor_size is None:
            randomness_percentage = 0.1
            randomn_factor_size = randomness_percentage * n

        random_factor = 2 * random() * randomn_factor_size
        if random_factor > 5:
            random_factor = 5
        without_average_random_factor = n - randomn_factor_size
        randomized_n = int(without_average_random_factor + random_factor)
        # logger('{} with randomness -> {}'.format(int(n), randomized_n))
        return int(randomized_n)

    def move_mouse(self, x, y):
        def set_mouse_position(x, y):
            self.mouse.position = (int(x), int(y))
        def smooth_move_mouse(from_x, from_y, to_x, to_y, speed=0.5):
            steps = 40
            sleep_per_step = speed // steps
            x_delta = (to_x - from_x) / steps
            y_delta = (to_y - from_y) / steps
            for step in range(steps):
                new_x = x_delta * (step + 1) + from_x
                new_y = y_delta * (step + 1) + from_y
                set_mouse_position(new_x, new_y)
                time.sleep(sleep_per_step)
        return smooth_move_mouse(
            self.mouse.position[0],
            self.mouse.position[1],
            x,
            y
        )

    def left_mouse_click(self):
        self.mouse.click(Button.left)

    def left_mouse_drag(self, start, end):
        self.move_mouse(*start)
        time.sleep(0.2)
        self.mouse.press(Button.left)
        time.sleep(0.2)
        self.move_mouse(*end)
        time.sleep(0.2)
        self.mouse.release(Button.left)
        time.sleep(0.2)

    def left_mouse_press(self):
        self.mouse.press(Button.left)
        
    def left_mouse_release(self):
        self.mouse.release(Button.left)

    def left_mouse_drag_move(self,x, y):
        self.mouse.press(Button.left)
        time.sleep(0.2)
        self.move_mouse(x,y)
        time.sleep(0.2)
        self.mouse.release(Button.left)
        time.sleep(0.2)

    def mouse_scroll(self, x, y):
        self.mouse.scroll(x,y)
        time.sleep(0.1)