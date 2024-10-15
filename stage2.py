# stage2.py
from pico2d import *
from grass import Grass
from ground import Ground

class Stage2:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.grass = Grass()
        self.ground = Ground()
        self.stage_change_call = stage_change_call

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update()
        if self.boy.x < 0:
            self.boy.x = 1020
            self.stage_change_call(1)  # Stage1로 전환
        elif self.boy.x > 1024:
            self.boy.x = 1024

    def draw(self):
        self.ground.draw()
        self.grass.draw(0, 30)
        self.boy.draw()