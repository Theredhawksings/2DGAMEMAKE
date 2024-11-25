from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from cyclicobstacle import CyclicObstacle
import collision_utils
import random
import time
from font import Font

class Stage6:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.last_obstacle_time = time.time()

        grass_positions = [
            (0, 0, 128),
            (325, 20, 128),
            (600, 50, 120),
            (850, 60, 90),
            (980, 90, 32),
            (920, 155, 32),
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

        #10빼면 됨
        obstacle_data = [
            (280, 60, 0, 0, 0),
            (400, 60, 0, 0, 0),
            (660, 90, 0, 0, 0),
            (860, 100, 0, 0, 0),
            (1020, 130, 1, 0, 0),
            (916, 280, 2, 0, 0),
            (941, 280, 2, 0, 0),
            (750, 250, 0, 0, 0),
            (500, 440, 0, 0, 0),
            (571, 365, 0, 0, 0),
            (571, 440, 0, 0, 0),
            (510, 515, 0, 0, 0),
            (631, 440, 0, 0, 0),
            (630, 515, 0, 0, 0),
            (726, 550, 0, 0, 0),
            (436, 530, 0, 0, 0),
            (396, 285, 0, 0, 0),
            (286, 345, 0, 0, 0),
            (81, 395, 0, 0, 0),
            (311, 455, 1, 0, 0),
            (71, 520, 3, 0, 0),
            (275, 595, 1, 0, 0),
            (886, 585, 1, 0, 0),
            (446, 600, 0, 0, 0),
        ]

        self.obstacle = Obstacle(obstacle_data)
        self.initial_obstacles = self.obstacle.obstacles.copy()

        self.obstacle_definitions = [
            {'trigger': {'x_min': 115, 'x_max': 130, 'y_min': 45, 'y_max': None},
             'obstacle': {'x': 160, 'y': -15, 'image_direction': 0, 'move_direction': 4, 'move_speed': 15}},
            {'trigger': {'x_min': 530, 'x_max': 540, 'y_min': 90, 'y_max': None},
             'obstacle': {'x': -10, 'y': 85, 'image_direction': 3, 'move_direction': 1, 'move_speed': 15}},
            {'trigger': {'x_min': 550, 'x_max': 560, 'y_min': 90, 'y_max': None},
             'obstacle': {'x': 1030, 'y': 85, 'image_direction': 1, 'move_direction': 2, 'move_speed': 15}},
            {'trigger': {'x_min': 705, 'x_max': 710, 'y_min': 255, 'y_max': None},
             'obstacle': {'x': 710, 'y': 780, 'image_direction': 2, 'move_direction': 3, 'move_speed': 30}},
            {'trigger': {'x_min': 555, 'x_max': 580, 'y_min': 515, 'y_max': None},
             'obstacle': {'x': 571, 'y': -15, 'image_direction': 0, 'move_direction': 4, 'move_speed': 10}},
            {'trigger': {'x_min': 140, 'x_max': 154, 'y_min': 535, 'y_max': None},
             'obstacle': {'x': 1030, 'y': 535, 'image_direction': 1, 'move_direction': 2, 'move_speed': 15}},
            {'trigger': {'x_min': 80, 'x_max': 120, 'y_min': 665, 'y_max': None},
             'obstacle': {'x': 100, 'y': 780, 'image_direction': 2, 'move_direction': 3, 'move_speed': 1}},
            {'trigger': {'x_min': 240, 'x_max': 254, 'y_min': 725, 'y_max': None},
             'obstacle': {'x': 1030, 'y': 725, 'image_direction': 1, 'move_direction': 2, 'move_speed': 15}},
            {'trigger': {'x_min': 306, 'x_max': 310, 'y_min': 725, 'y_max': None},
             'obstacle': {'x': -10, 'y': 725, 'image_direction': 3, 'move_direction': 1, 'move_speed': 15}},
            {'trigger': {'x_min': 340, 'x_max': 350, 'y_min': 725, 'y_max': None},
             'obstacle': {'x': -10, 'y': 725, 'image_direction': 3, 'move_direction': 1, 'move_speed': 15}},
            {'trigger': {'x_min': 390, 'x_max': 395, 'y_min': 725, 'y_max': None},
             'obstacle': {'x': 1030, 'y': 725, 'image_direction': 1, 'move_direction': 2, 'move_speed': 15}},
        ]
        self.font = Font(30)

        self.obstacle_created = [False] * len(self.obstacle_definitions)

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

        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

    def handle_event(self, event):
        self.boy.handle_event(event)

    def check_and_create_obstacles(self):
        for i, definition in enumerate(self.obstacle_definitions):
            if self.obstacle_created[i]:
                continue

            trigger = definition['trigger']

            x_condition = (self.boy.x >= trigger['x_min']) and \
                          (trigger['x_max'] is None or self.boy.x < trigger['x_max'])

            y_condition = True
            if trigger['y_min'] is not None:
                y_condition = self.boy.y >= trigger['y_min']
            if trigger['y_max'] is not None:
                y_condition = y_condition and self.boy.y < trigger['y_max']

            if x_condition and y_condition:
                self.obstacle.obstacles.append(definition['obstacle'].copy())
                self.obstacle_created[i] = True

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        if self.boy.x < 1:
            if self.boy.y == 715:
                self.stage_change_call(5)
                self.boy.x = 1020
                self.boy.y = 715
            else:
                self.boy.x = 1

            if self.boy.y == 45:
                self.stage_change_call(5)
                self.boy.x = 1020
                self.boy.y = 105

        if self.boy.y < -1:
            self.boy.x = self.boy.savepointX
            self.boy.y = self.boy.savepointY
            self.obstacle_created = [False] * len(self.obstacle_definitions)
            self.obstacle.obstacles = self.initial_obstacles.copy()

        if self.boy.x > 1024:
            if self.boy.y == 595:
                self.boy.x= self.boy.savepointX
                self.boy.y = self.boy.savepointY

            elif self.boy.y==425:
                self.stage_change_call(7)
                self.boy.x = 30
                self.boy.y = 1020

        self.check_and_create_obstacles()

        if collision_utils.handle_collisions():
            self.obstacle_created = [False] * len(self.obstacle_definitions)
            self.obstacle.obstacles = self.initial_obstacles.copy()

        for bullet in self.bullets:
            bullet.update()


        current_time = time.time()

        if self.boy.x > 820 and self.boy.y > 720:
            new_obstacle = {
                'x': 1030,
                'y': 725,
                'image_direction': 1,
                'move_direction': 2,
                'move_speed': 5
            }
            self.obstacle.obstacles.append(new_obstacle)
            self.last_obstacle_time = current_time

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()

        self.font.draw(50, 190, "끝으로 이어진 땅으로 가서 탈출구를 찾으세요", (255, 255, 255))

        for bullet in self.bullets:
            bullet.draw()