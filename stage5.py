# stage5.py
from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from cyclicobstacle import CyclicObstacle
import collision_utils
import random
import time

class Stage5:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.ground = Ground(current_stage=5)
        self.stage_change_call = stage_change_call
        self.boy.x = 5
        self.boy.y = 50
        self.boy.apply_gravity = True
        self.boy.savepointX = 15
        self.boy.savepointY = 730

        self.grass = Grass(
            [(0, 680, 100)] +
            [(x, y, 31)
             for y in range(60, 601, 60)
             for x in range(180 if y % 120 == 0 else 240, 841, 120)] +
            [(960, 60, 80)],
            current_stage=5
        )

        self.obstacle = Obstacle([])
        self.cyclic_obstacles = []

        self.bullets = []

        for x in range(240, 960, 120):
            for y in range(95, 577, 120):
                self.cyclic_obstacles.append(
                    CyclicObstacle(x, y, 0, 4, 0,
                                   random.uniform(1.0, 2.0),
                                   random.uniform(4.0, 5.0))
                )
        for x in range(180, 840, 120):
            for y in range(155, 697, 120):
                self.cyclic_obstacles.append(
                    CyclicObstacle(x, y, 0, 4, 0,
                                   random.uniform(1.0, 2.0),
                                   random.uniform(4.0, 5.0))
                )

        self.time = time.time()
        self.boy.update_stage_info(5)

        collision_utils.clear_collision_pairs()
        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

        for cyclic_obstacle in self.cyclic_obstacles:
            collision_utils.add_collision_pair('boy:cyclic_obstacle', self.boy, cyclic_obstacle)

        for bullet in self.bullets:
            bullet.update()

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()
        for cyclic_obstacle in self.cyclic_obstacles:
            cyclic_obstacle.update()

        if self.boy.x < 1 and self.boy.y == 730:
            self.stage_change_call(4)
            self.boy.x = 1000
            self.boy.y = 720

        if self.boy.x > 1024 :
            self.stage_change_call(6)
            self.boy.x = 1000
            self.boy.y = 720

        collision_utils.handle_collisions()

        if self.boy.y < -1:
            self.boy.x = self.boy.savepointX
            self.boy.y = self.boy.savepointY

        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()

        for cyclic_obstacle in self.cyclic_obstacles:
            cyclic_obstacle.draw()

        for bullet in self.bullets:
            bullet.draw()