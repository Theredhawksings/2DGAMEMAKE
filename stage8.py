from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from cyclicobstacle import CyclicObstacle
import collision_utils
import random
import time

class Stage8:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.last_obstacle_time = time.time()
        self.background_y = 6229

        grass_positions = [
            (0, 0, 128),
        ]

        self.grass = Grass(grass_positions, current_stage=7)
        self.ground = Ground(current_stage=9)
        self.stage_change_call = stage_change_call
        self.boy.savepointX = 1
        self.boy.savepointY = 45
        self.bullets = []

        self.boy.update_stage_info(8)

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)

        if self.boy.game_world.state != 'PAUSE':
            self.background_y -= 1

        if self.background_y <= 0:
            self.background_y = 0

        if self.boy.y < -1:
            self.boy.x = self.boy.savepointX
            self.boy.y = self.boy.savepointY

        for bullet in self.bullets:
            bullet.update()



    def draw(self):
        self.ground.falling_draw(512, 384, self.background_y)
        self.grass.draw()
        self.boy.draw()

        for bullet in self.bullets:
            bullet.draw()