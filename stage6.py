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
            (0, 0, 128),
            (325, 20, 128),
            (600, 50, 120),
            (850, 60, 90),
            (980, 90, 32),
            (920, 175, 32),
            (770, 210, 92),
            (570, 250, 60),

            (400, 250, 70),
            (570, 330, 50),
            (570, 400, 40),
            (570, 470, 30),
            (570, 540, 20),
            (570, 610, 100),

            (280, 310, 80),
            (50, 360, 120),
            (240, 420, 40),
            (410, 490, 60),
            (150, 490, 20),
            (240, 550, 60),
            (100, 620, 40),
            (10, 670, 30),

            (320, 680, 120),
            (920, 680, 240),
            (920, 550, 120),
            (720, 510, 60),
            (920, 380, 150),
        ]
        self.grass = Grass(grass_positions, current_stage=4)

        self.ground = Ground(current_stage=6)

        self.stage_change_call = stage_change_call

        self.boy.savepointX = 1
        self.boy.savepointY = 45

        self.bullets = []

        self.boy.update_stage_info(6)

        collision_utils.clear_collision_pairs()

        for bullet in self.bullets:
            bullet.update()

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)

        if self.boy.x < 1:
            self.boy.x = 1

            if self.boy.y==45:
                self.stage_change_call(5)
                self.boy.x = 1020
                self.boy.y = 105

        if self.boy.y < -1:
            self.boy.x = self.boy.savepointX
            self.boy.y = self.boy.savepointY

        collision_utils.handle_collisions()

        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()

        for bullet in self.bullets:
            bullet.draw()