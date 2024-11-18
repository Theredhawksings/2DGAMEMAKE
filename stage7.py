from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from cyclicobstacle import CyclicObstacle
import collision_utils
import random
import time

class Stage7:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.last_obstacle_time = time.time()

        grass_positions = [
            (20, 0, 120),
            (20, 150, 120),
            (20, 300, 120),
            (20, 450, 120),
            (20, 600, 120),
        ]

        self.grass = Grass(grass_positions, current_stage=7)
        self.ground = Ground(current_stage=7)
        self.stage_change_call = stage_change_call

        self.bullets = []

        self.boy.update_stage_info(7)

        collision_utils.clear_collision_pairs()

        for bullet in self.bullets:
            bullet.update()

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)


        if self.boy.y < -1:
            self.boy.x = 10
            self.boy.y = 760

        for bullet in self.bullets:
            bullet.update()


    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()

        for bullet in self.bullets:
            bullet.draw()