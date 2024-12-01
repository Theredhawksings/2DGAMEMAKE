# stage3.py
from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
import collision_utils
import random
import time


class Stage3:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.ground = Ground(current_stage=3)
        self.stage_change_call = stage_change_call

        is_from_stage4 = self.boy.previous_stage == 4
        self.background_y = 384 if is_from_stage4 else 5229
        self.boy.x = 1020 if is_from_stage4 else 512
        self.boy.y = 50 if is_from_stage4 else 630

        self.boy.apply_gravity = False
        self.grass = Grass([(512, 0, 512)], current_stage=3)
        self.time = time.time()
        self.last_obstacle_time = time.time()
        self.obstacle = Obstacle([])

        self.boy.update_stage_info(3)
        collision_utils.clear_collision_pairs()
        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

        self.bullets = []

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        if self.boy.game_world.state == 'PAUSE':
            return

        self.boy.update(self.grass)
        self.obstacle.update()

        if self.background_y < 400 and self.boy.apply_gravity == False:
            self.boy.y -= 2

        if self.background_y <= 384:
            self.background_y = 384

        if self.boy.y < 50:
            self.boy.y = 50
            self.boy.apply_gravity = True
            self.boy.falling = False
            self.boy.is_jumping = False

        if self.boy.x < 1:
            self.boy.x = 1
        elif self.boy.y == 45 and self.boy.x > 1024:
            self.boy.x = 1024

        current_time = time.time()

        if current_time - self.last_obstacle_time >= 0.08 and self.background_y > 400:
            new_obstacle = {
                'x': random.randint(0, 1024),
                'y': -20,
                'image_direction': 0,
                'move_direction': 4,
                'move_speed': 7
            }
            self.obstacle.obstacles.append(new_obstacle)
            self.last_obstacle_time = current_time

        if current_time % 0.1 <= 0.01 and self.boy.apply_gravity == False:
            self.boy.y -= 1

        if collision_utils.collide(self.boy, self.obstacle):
            self.boy.x = 310
            self.boy.y = 150
            self.boy.apply_gravity = True
            self.stage_change_call(2)

        if self.boy.x >= 1024:
            if self.boy.y == 50:
                self.boy.x = 30
                self.boy.y = 45
                self.stage_change_call(4)
            else:
                self.boy.x = 1024

        for bullet in self.bullets:
            bullet.update()

        if self.boy.game_world.state != 'PAUSE':
            self.background_y -= 3

    def draw(self):
        self.ground.falling_draw(512, 384, self.background_y)

        if self.background_y < 400:
            self.grass.draw()

        self.boy.draw()
        self.obstacle.draw()

        for bullet in self.bullets:
            bullet.draw()