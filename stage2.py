from pico2d import *

import collision_utils
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from font import Font
from bullet import Bullet
from savepoint import SavePoint

import time
import random


class Stage2:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        grass_positions = [(400, 650, 512), (800, 100, 512), (400, 330, 512), (800, 500, 512)]
        self.grass = Grass(grass_positions)
        self.ground = Ground(current_stage=2)
        self.last_obstacle_time = time.time()

        obstacle_data = [
            (270, 680, 0, 0, 0),
            (400, 680, 0, 0, 0),
            (460, 755, 2, 0, 0),
            (600, 755, 2, 0, 0),
            (820, 680, 0, 0, 0),
            (200, 755, 2, 0, 0),
            (520, 680, 0, 0, 0),
            (680, 680, 0, 0, 0),

            (200, 530, 0, 0, 0),
            (200, 606, 2, 0, 0),
            (250, 606, 2, 0, 0),
            (400, 606, 2, 0, 0),
            (500, 530, 0, 0, 0),
            (650, 530, 0, 0, 0),
            (700, 606, 2, 0, 0),
            (1000, 530, 0, 0, 0),

            (30, 360, 0, 0, 0),
            (55, 360, 0, 0, 0),
            (80, 360, 0, 0, 0),
            (240, 360, 0, 0, 0),
            (265, 360, 0, 0, 0),

            (420, 456, 2, 0, 0),
            (470, 360, 0, 0, 0),

            (570, 360, 0, 0, 0),
            (620, 456, 2, 0, 0),
            (670, 360, 0, 0, 0),

            (770, 360, 0, 0, 0),
            (810, 456, 2, 0, 0),
            (890, 360, 0, 0, 0),
            (925, 330, 0, 0, 0),
        ]

        collision_utils.clear_collision_pairs()

        self.obstacle = Obstacle(obstacle_data)
        self.stage_change_call = stage_change_call
        self.boy.update_stage_info(2)
        self.font = Font(30)

        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

        self.fonts = [
            {"font": Font(30), "x": 30, "y": 750, "text": f"죽은 횟수: {Obstacle.get_death_count()}",
             "color": (0, 0, 0)},
        ]
        self.fonts[0]["text"] = f"죽은 횟수: {Obstacle.get_death_count()}"
        self.bullets = []

        self.world = []

        savepoint_positions = [
            (794, 605)
        ]
        self.savepoints = [SavePoint(x, y, 2) for x, y in savepoint_positions]

        self.world.append(self.ground)
        self.world.append(self.grass)
        self.world.extend(self.savepoints)
        self.world.append(self.boy)
        self.world.append(self.obstacle)
        self.world.append(self.bullets)
        self.world.extend(self.fonts)

        collision_utils.add_collision_pair('bullet:savepoint', self.bullets, self.savepoints)

        self.boy.savepointX = 5
        self.boy.savepointY = 760

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        self.fonts[0]["text"] = f"죽은 횟수: {Obstacle.get_death_count()}"

        current_time = time.time()

        if current_time - self.last_obstacle_time >= 0.1 and self.boy.y < 300 and self.boy.x >= 315:
            new_obstacle = {
                'x': random.randint(350, 900),
                'y': 300,
                'image_direction': 2,
                'move_direction': 3,
                'move_speed': 4
            }
            self.obstacle.obstacles.append(new_obstacle)
            self.last_obstacle_time = current_time

        if self.boy.x < 0 and self.boy.y == 695:
            self.boy.x = 1020
            self.boy.y = 80
            self.stage_change_call(1)
        elif self.boy.x > 1024:
            self.boy.x = 1024
        elif self.boy.x <= 280 and self.boy.y < 0:
            self.stage_change_call(3)

        collision_utils.handle_collisions()

        for bullet in self.bullets:
            bullet.update()


    def draw(self):
        for obj in self.world:
            if isinstance(obj, list):
                for sub_obj in obj:
                    sub_obj.draw()
            elif isinstance(obj, Ground):
                obj.draw(512, 384)
            elif isinstance(obj, dict) and "font" in obj:
                font = obj["font"]
                x = obj["x"]
                y = obj["y"]
                text = obj["text"]
                color = obj["color"]
                font.draw(x, y, text, color)
            else:
                obj.draw()