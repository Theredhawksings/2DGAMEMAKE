from pico2d import *
from grass import Grass
from ground import Ground


class Stage2:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        grass_positions = [(400, 650), (800, 100), (400, 330), (800, 500)]
        self.grass = Grass(grass_positions)
        self.ground = Ground()
        self.stage_change_call = stage_change_call

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        if self.boy.x < 1 and self.boy.y == 700:
            self.boy.x = 1020
            self.boy.y = 80
            self.stage_change_call(1)
        elif self.boy.x > 1024:
            self.boy.x = 1024

    def draw(self):
        self.ground.draw()
        self.grass.draw()
        self.boy.draw()