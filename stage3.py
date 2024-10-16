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
        self.boy.update(self.grass)  # grass 대신 None을 전달
        self.background_y -= 7

        if self.background_y <= 384:
            self.background_y = 384
        else:
            self.background_y -= 5

        if self.boy.y <= 50:
            self.boy.y = 50
            self.boy.apply_gravity = True
        else:
            self.boy.y -= 1


    def draw(self):
        self.ground.fallingdraw(512, 384, self.background_y)
        if self.background_y < 500:
            self.grass.draw()

        self.boy.draw()