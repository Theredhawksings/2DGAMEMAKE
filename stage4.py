from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from collision_utils import check_collision, handle_collision
import random
import time


class Stage4:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.ground = Ground(current_stage=4)
        self.stage_change_call = stage_change_call
        self.boy.x = 5
        self.boy.y = 50
        self.boy.apply_gravity = True
        self.grass = Grass([(0, 0, 512), (100, 50, 25),  (200, 100, 25)], current_stage=4)
        self.time = time.time()
        self.obstacle = Obstacle([])
        self.boy.update_stage_info(4)


    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)

        if self.boy.x < 2 and self.boy.y==50:
            self.stage_change_call(3)


    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()
