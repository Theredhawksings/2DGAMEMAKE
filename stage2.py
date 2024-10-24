from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from collision_utils import check_collision, handle_collision
import time
import random


class Stage2:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        grass_positions = [(400, 650, 512), (800, 100, 512), (400, 330, 512), (800, 500, 512)]
        self.grass = Grass(grass_positions)
        self.ground = Ground(current_stage=2)
        self.last_obstacle_time = time.time()

        obstacle_data = [
            (270, 680, 0, 0, 0),
            (400, 680, 0, 0, 0),
            (460, 755, 2, 0 ,0),
            (600, 755, 2, 0, 0),
            (800, 680, 0, 0, 0),
            (200, 755, 2, 0, 0),
            (520, 680, 0, 0, 0),
            (680, 680, 0, 0, 0),
            (780, 680, 0, 0, 0),
            #1

            (200, 530, 0, 0, 0),
            (200, 606, 2, 0, 0),
            (250, 606, 2, 0, 0),
            (400, 606, 2, 0, 0),
            (500, 530, 0, 0, 0),
            (650, 530, 0, 0, 0),
            (700, 606, 2, 0, 0),
            (780, 530, 0, 0, 0),
            (1000, 530, 0, 0, 0),
            #2

            (30, 360, 0, 0, 0),
            (55, 360, 0, 0, 0),
            (80, 360, 0, 0, 0),
            (240, 360, 0, 0, 0),
            (265, 360, 0, 0, 0),
            (380, 360, 0, 0, 0),
            (420, 456, 2, 0, 0),
            (470, 360, 0, 0, 0),
            (520, 456, 2, 0, 0),
            (570, 360, 0, 0, 0),
            (620, 456, 2, 0, 0),
            (670, 360, 0, 0, 0),
            (720, 456, 2, 0, 0),
            (770, 360, 0, 0, 0),
            (810, 456, 2, 0, 0),
            (890, 360, 0, 0, 0),
            (925, 330, 0, 0, 0),
            #3
        ]
        
        self.obstacle = Obstacle(obstacle_data)

        self.stage_change_call = stage_change_call

        self.boy.savepointX = 356
        self.boy.savepointY = 500
        self.boy.update_stage_info(2)

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        current_time = time.time()

        if current_time % 0.05 < 0.01 and self.boy.y < 300:
            new_obstacle = {
                'x': random.randint(350, 900),
                'y': 300,
                'image_direction': 2,
                'move_direction': 3,
                'move_speed': 4
            }
            self.obstacle.obstacles.append(new_obstacle)

        if self.boy.x < 1 and self.boy.y == 700:
            self.boy.x = 1020
            self.boy.y = 80
            self.stage_change_call(1)

        elif self.boy.x > 1024:
            self.boy.x = 1024

        elif self.boy.x <= 280 and self.boy.y < 0:
            self.stage_change_call(3)

        for obstacle in self.obstacle.obstacles:
            if check_collision(self.boy, obstacle['x'], obstacle['y'], obstacle['image_direction']):
                handle_collision(self.boy)
                break

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()