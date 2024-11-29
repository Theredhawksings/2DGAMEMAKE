from pico2d import *
import os
import collision_utils

PIXEL_PER_METER = (10.0 / 0.3)
BULLET_SPEED_KMPH = 2
BULLET_SPEED_MPM = BULLET_SPEED_KMPH * 1000.0 / 60.0
BULLET_SPEED_MPS = BULLET_SPEED_MPM / 60.0
BULLET_SPEED_PPS = BULLET_SPEED_MPS * PIXEL_PER_METER


class Bullet:
    def __init__(self, x, y, direction_right, stage):
        self.x = x
        self.y = y
        self.stage = stage
        self.image = load_image(os.path.join('bullet', 'bullet.png'))
        self.speed = BULLET_SPEED_PPS * (1 if direction_right else -1)
        self.should_remove = False

        self.gun_sound = load_wav(os.path.join('bgm', 'gun effects.mp3'))
        self.gun_sound.play()

        if hasattr(stage, 'savepoints'):
            for savepoint in stage.savepoints:
                collision_utils.add_collision_pair('bullet:savepoint', self, savepoint)

    def update(self):
        self.x += self.speed
        if self.x < -500 or self.x > 1524 or self.should_remove:
            if self in self.stage.bullets:
                self.stage.bullets.remove(self)

    def draw(self):
        self.image.clip_draw(0, 0, 5, 5, self.x, self.y, 10, 10)
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 8, self.y - 8, self.x + 8, self.y + 8

    def handle_collision(self, group, other):
        if group == 'bullet:boss':
            self.should_remove = True
            collision_utils.remove_collision_pair(group, self)
        elif group == 'bullet:savepoint':
            if self in self.stage.bullets:
                self.stage.bullets.remove(self)
                collision_utils.remove_collision_pair(group, self)
            self.should_remove = True