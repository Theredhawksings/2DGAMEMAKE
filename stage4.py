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
        self.grass = Grass([(0, 0, 128),
                            (130, 60, 30),
                            (250, 100, 30),
                            (370, 150, 30),
                            (430, 220, 30),
                            (520, 300, 30),
                            (610, 350, 30),
                            (710, 430, 30),
                            (630, 510, 30),
                            (440, 510, 100),
                            (1000, 700, 200),
                            ],

                           current_stage=4)
        self.time = time.time()
        self.obstacle = Obstacle([])
        self.boy.update_stage_info(4)
        self.obstacle_created = [False] * 5

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        if self.boy.x < 2 and self.boy.y==50:
            self.stage_change_call(3)

        if self.boy.y < -1:
            self.boy.x = 20
            self.boy.y = 70
            self.obstacle_created = [False] * 5

        for obstacle in self.obstacle.obstacles:
            if check_collision(self.boy, obstacle['x'], obstacle['y'], obstacle['image_direction']):
                handle_collision(self.boy)
                self.stage_change_call(4)
                self.boy.savepointX = 5
                self.boy.savepointY = 50
                self.obstacle_created = [False] * 5
                break

        if not self.obstacle_created[0] and self.boy.x >= 110 and self.boy.x < 130:
            new_obstacle = {
                'x': 130,
                'y': -15,
                'image_direction': 0,
                'move_direction': 4,
                'move_speed': 15
            }
            self.obstacle.obstacles.append(new_obstacle)
            self.obstacle_created[0] = True

        if not self.obstacle_created[1] and self.boy.x >= 350 and self.boy.x < 380:
            new_obstacle = {
                'x': -30,
                'y': 220,
                'image_direction': 3,
                'move_direction': 1,
                'move_speed': 15
            }
            self.obstacle.obstacles.append(new_obstacle)
            self.obstacle_created[1] = True

        if not self.obstacle_created[2] and self.boy.x >= 490 and self.boy.x < 510:
            new_obstacle = {
                'x': 510,
                'y': 0,
                'image_direction': 0,
                'move_direction': 4,
                'move_speed': 30
            }
            self.obstacle.obstacles.append(new_obstacle)
            self.obstacle_created[2] = True

        if not self.obstacle_created[3] and self.boy.x >= 530 and self.boy.x < 550:
            new_obstacle = {
                'x': 530,
                'y': 800,
                'image_direction': 2,
                'move_direction': 2,
                'move_speed': 30
            }

            new_obstacle = {
                'x': 530,
                'y': 850,
                'image_direction': 2,
                'move_direction': 2,
                'move_speed': 30
            }

            self.obstacle.obstacles.append(new_obstacle)
            self.obstacle_created[3] = True

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()
