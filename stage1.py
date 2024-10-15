# stage1.py
from pico2d import *
from boy import Boy
from grass import Grass
from ground import Ground

class Stage1:
    def __init__(self):
        self.boy = Boy()
        self.grass = Grass()
        self.ground = Ground()

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update()
        if self.boy.x < 0:
            self.boy.x = 0


    def draw(self):
        self.ground.draw()
        self.grass.draw(512, 30)
        self.boy.draw()