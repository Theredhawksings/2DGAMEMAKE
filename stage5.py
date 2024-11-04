from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from collision_utils import check_collision, handle_collision
import random
import time

class Stage5:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.ground = Ground(current_stage=5)
        self.stage_change_call = stage_change_call
        self.boy.x = 5
        self.boy.y = 50
        self.boy.apply_gravity = True

        # 플랫폼 위치 데이터 - (x, y, width) 형식
        self.grass = Grass([
            (0, 0, 100),

            (180, 0, 20),
            (300, 0, 20),
            (240, 60, 20),
            (360, 60, 20)
        ], current_stage=5)

        # 빈 장애물 리스트로 초기화
        self.obstacle = Obstacle([])

        self.time = time.time()
        self.boy.update_stage_info(5)
        self.obstacle_created = [False] * 10

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        # 이전 스테이지로 돌아가기
        if self.boy.x < 2 and self.boy.y == 50:
            self.stage_change_call(4)
            self.boy.x = 1020
            self.boy.y = 720

        # 낙사 처리
        if self.boy.y < -10:
            self.boy.x = 20
            self.boy.y = 70
            self.boy.falling = False
            self.boy.is_jumping = False
            self.boy.jump_speed = 0
            self.obstacle_created = [False] * 10

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()