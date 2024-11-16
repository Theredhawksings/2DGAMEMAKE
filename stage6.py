# stage5.py
from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from cyclicobstacle import CyclicObstacle
import collision_utils
import random
import time

class Stage6:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self

        grass_positions = [
            (0, 0, 128)
        ]
        self.grass = Grass(grass_positions, current_stage=4)

        self.ground = Ground(current_stage=6)

        self.stage_change_call = stage_change_call
        self.boy.x = 5
        self.boy.y = 50

        self.boy.savepointX = 15
        self.boy.savepointY = 730


        self.obstacle = Obstacle([])
        self.cyclic_obstacles = []

        self.bullets = []

        self.boy.update_stage_info(6)

        collision_utils.clear_collision_pairs()
        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

        for bullet in self.bullets:
            bullet.update()

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)

        collision_utils.handle_collisions()

        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()


        for bullet in self.bullets:
            bullet.draw()