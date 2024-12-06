from pico2d import *
from grass import Grass
from ground import Ground
import random
import time

from savepoint import SavePointManager


class Stage8:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.last_obstacle_time = time.time()
        self.background_y = 6229
        self.start_time = time.time()  #

        grass_positions = [
            (0, 0, 1026),
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

        # PAUSE 상태가 아닐 때만 배경 스크롤
        if self.boy.game_world.state != 'PAUSE':
            self.background_y -= 1

        if self.background_y <= 0:
            self.background_y = 0

        if self.boy.x < 2:
            self.boy.x = 2

        if self.boy.x > 1024:
            self.boy.x = 20
            self.boy.y = 700
            self.stage_change_call(1)
            SavePointManager()._instance.states.clear()

        for bullet in self.bullets:
            bullet.update()

        if time.time() - self.start_time >= 208:
            self.boy.game_world.running = False

    def draw(self):
        self.ground.falling_draw(512, 384, self.background_y)
        self.grass.draw()
        self.boy.draw()

        # 총알 그리기
        for bullet in self.bullets:
            bullet.draw()