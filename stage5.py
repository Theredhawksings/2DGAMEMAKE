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
            (0, 0, 100),            # 시작 지점
            (150, 70, 40),          # 첫 번째 발판
            (250, 140, 50),         # 두 번째 발판
            (380, 200, 60),         # 세 번째 발판
            (500, 250, 70),         # 네 번째 발판
            (620, 300, 80),         # 다섯 번째 발판
            (740, 350, 90),         # 여섯 번째 발판
            (860, 400, 100),        # 일곱 번째 발판
            (740, 450, 90),         # 여덟 번째 발판
            (620, 500, 80),         # 아홉 번째 발판
            (500, 550, 70),         # 열 번째 발판
            (380, 600, 60),         # 열한 번째 발판
            (260, 650, 50),         # 열두 번째 발판
            (140, 700, 40),         # 열세 번째 발판
            (300, 750, 200),        # 열네 번째 발판(넓은 발판)
            (600, 750, 400)         # 마지막 발판(가장 넓은 발판)
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