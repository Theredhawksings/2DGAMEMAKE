from pico2d import *
from grass import Grass
from ground import Ground

class Stage3:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.ground = Ground(current_stage=3)
        self.stage_change_call = stage_change_call
        self.background_y = 5414
        self.boy.y = 540
        self.boy.apply_gravity = False
        self.height = 1
        self.grass = Grass([(512, 0)], current_stage=3)

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.background_y -= 3

        if self.background_y < 400:
            self.boy.y -= 2

        if self.background_y <= 384:
            self.background_y = 384

        if self.boy.y <= 50:
            self.boy.y = 50
            self.boy.apply_gravity = True

        if self.boy.y > 50 and self.boy.x < 0:
            self.boy.x = 0
        elif self.boy.y > 50 and self.boy.x > 1024:
            self.boy.x = 1024



    def draw(self):
        self.ground.fallingdraw(512, 384, self.background_y)

        if self.background_y < 400:
            self.grass.draw()

        self.boy.draw()