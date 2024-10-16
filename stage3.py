from pico2d import *
from grass import Grass
from ground import Ground


class Stage3:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.ground = Ground(current_stage=3)
        self.stage_change_call = stage_change_call
        self.background_y = 5232  # 초기 배경 y 위치
        self.boy.y = 6000  # 소년의 초기 y 위치

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        original_boy_y = self.boy.y
        self.boy.update(None)  # 소년 업데이트 (grass는 사용하지 않으므로 None 전달)

        fall_distance = original_boy_y - self.boy.y

        self.background_y -= fall_distance

        self.background_y = max(512, self.background_y)

        if self.boy.y <= 0:
            self.boy.y = 0;

    def draw(self):
        self.ground.draw(512, self.background_y)
        self.boy.draw()