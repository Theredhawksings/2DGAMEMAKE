# bullet.py
from pico2d import *
import os

PIXEL_PER_METER = (10.0 / 0.3)
BULLET_SPEED_KMPH = 1.5
BULLET_SPEED_MPM = BULLET_SPEED_KMPH * 1000.0 / 60.0
BULLET_SPEED_MPS = BULLET_SPEED_MPM / 60.0
BULLET_SPEED_PPS = BULLET_SPEED_MPS * PIXEL_PER_METER


class Bullet:
    def __init__(self, x, y, direction_right):
        self.x = x
        self.y = y
        self.image = load_image(os.path.join('bullet', 'bullet.png'))
        self.speed = BULLET_SPEED_PPS * (1 if direction_right else -1)
        self.should_remove = False

    def update(self):
        self.x += self.speed
        if self.x < 0 or self.x > 1024:
            self.should_remove = True

    def draw(self):
        self.image.clip_draw(0, 0, 5, 5, self.x, self.y, 10, 10)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8