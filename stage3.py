from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from collision_utils import check_collision, handle_collision
import random
import time

class Stage3:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.ground = Ground(current_stage=3)
        self.stage_change_call = stage_change_call
        self.background_y = 384 if self.boy.previous_stage == 4 else 5229
        self.boy.x = 1020 if self.boy.previous_stage == 4 else 512
        self.boy.y = 50 if self.boy.previous_stage == 4 else 630
        self.boy.apply_gravity = False
        self.grass = Grass([(512, 0, 512)], current_stage=3)
        self.time = time.time()
        self.obstacle = Obstacle([])
        self.boy.update_stage_info(3)

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        if self.background_y < 400:
            self.boy.y -= 2

        if self.background_y <= 384:
            self.background_y = 384

        if self.boy.y <= 50:
            self.boy.y = 50
            self.boy.apply_gravity = True

        if self.boy.y == 50 and self.boy.x < 1:
            self.boy.x = 1
            self.boy.y = 50

        elif self.boy.y > 50 and self.boy.x > 1024:
            self.boy.x = 1024

        current_time = time.time()

        if current_time % 0.03 < 0.01 and self.background_y > 400:
            new_obstacle = {
                'x': random.randint(0, 1024),
                'y': -20,
                'image_direction': 0,
                'move_direction': 4,
                'move_speed': 7
            }
            self.obstacle.obstacles.append(new_obstacle)

        if current_time % 0.1 <= 0.01:
            self.boy.y-=1

        for obstacle in self.obstacle.obstacles:
            if check_collision(self.boy, obstacle['x'], obstacle['y'], obstacle['image_direction']):
                self.boy.savepointX = 310
                self.boy.savepointY = 150
                self.boy.apply_gravity = True
                handle_collision(self.boy)
                self.stage_change_call(2)
                break

        if self.boy.x > 1024 and self.boy.y == 50:
            self.boy.x = 1020
            self.boy.y = 80
            self.stage_change_call(4)


    def draw(self):
        self.ground.fallingdraw(512, 384, self.background_y)
        self.background_y -= 3

        if self.background_y < 400:
            self.grass.draw()

        self.boy.draw()
        self.obstacle.draw()