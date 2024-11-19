# boss.py
from pico2d import *
import os

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixels = 30 cm
BOSS_SPEED_KMPH = 40.0
BOSS_SPEED_MPM = BOSS_SPEED_KMPH * 1000.0 / 60.0
BOSS_SPEED_MPS = BOSS_SPEED_MPM / 60.0
BOSS_SPEED_PPS = BOSS_SPEED_MPS * PIXEL_PER_METER


class Boss:
    def __init__(self):
        self.image = load_image(os.path.join('image', 'boss.png'))
        self.x = 900
        self.y = 840
        self.active = False
        self.vy = BOSS_SPEED_PPS
        self.y_min = 100
        self.y_max = 760
        self.width = 250
        self.height = 300
        self.boy = None

    def activate(self):
        self.active = True

    def get_bb(self):
        return (self.x - 100,
                self.y - 125,
                self.x + 100,
                self.y + 125)

    def draw(self):
        self.image.clip_composite_draw(
            0, 0,
            500, 600,
            0,
            '',
            self.x, self.y,
            self.width, self.height
        )
        draw_rectangle(*self.get_bb())

    def update(self):
        if not self.active:
            return

        self.y += self.vy * 0.016

        if self.y <= self.y_min:
            self.y = self.y_min
            self.vy = abs(self.vy)
        elif self.y >= self.y_max:
            self.y = self.y_max
            self.vy = -abs(self.vy)


    def handle_collision(self, group, other):
        if group == 'bullet:boss':
            self.should_remove = True
