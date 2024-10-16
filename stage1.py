from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle

class Stage1:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        grass_positions = [(512, 30)]
        self.grass = Grass(grass_positions)
        self.ground = Ground()

        self.stage_change_call = stage_change_call

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        if self.boy.x < 0:
            self.boy.x = 0
        elif self.boy.x > 1024:
            self.stage_change_call(2)
            self.boy.x = 2
            self.boy.y = 700

    def draw(self):
        self.ground.draw()
        self.grass.draw()
        self.boy.draw()