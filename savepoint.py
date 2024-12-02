from pico2d import *
import os


class SavePointManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SavePointManager, cls).__new__(cls)
            cls._instance.states = {}
        return cls._instance

    def get_state(self, stage, x, y):
        return self.states.get((stage, x, y), False)

    def set_state(self, stage, x, y, state):
        self.states[(stage, x, y)] = state


class SavePoint:
    images = []

    def __init__(self, x, y, stage):
        self.x = x
        self.y = y
        self.stage = stage
        if not SavePoint.images:
            SavePoint.images.append(load_image(os.path.join('savepoint', 'activate.png')))
            SavePoint.images.append(load_image(os.path.join('savepoint', 'deactivate.png')))

        self.manager = SavePointManager()
        self.is_activated = self.manager.get_state(stage, x, y)

    def draw(self):
        if self.is_activated:
            SavePoint.images[0].clip_draw(0, 0, 60, 60, self.x, self.y, 30, 30)
        else:
            SavePoint.images[1].clip_draw(0, 0, 60, 60, self.x, self.y, 30, 30)
        #draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def activate(self):
        self.is_activated = True
        self.manager.set_state(self.stage, self.x, self.y, True)

    def handle_collision(self, group, other):
        if group == 'bullet:savepoint':
            self.activate()