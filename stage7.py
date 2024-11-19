from pico2d import *
from boss import Boss
from grass import Grass
from ground import Ground
import collision_utils
import time


class Stage7:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.start_time = time.time()
        self.boss_activated = False

        grass_positions = [
            (20, 0, 120),
            (20, 150, 120),
            (20, 300, 120),
            (20, 450, 120),
            (20, 600, 120),
        ]

        self.grass = Grass(grass_positions, current_stage=7)
        self.ground = Ground(current_stage=7)
        self.stage_change_call = stage_change_call
        self.bullets = []
        self.boss = Boss()
        self.boss.boy = boy
        self.boy.update_stage_info(7)

        self.boss_blood_image = load_image(os.path.join('image', 'boss blood.png'))

        collision_utils.clear_collision_pairs()
        collision_utils.add_collision_pair('bullet:boss', self.bullets, [self.boss])

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)

        if self.boy.y < -1:
            self.boy.x = 10
            self.boy.y = 760

        if self.boy.x < 1:
            self.boy.x = 1

        if not self.boss_activated and time.time() - self.start_time >= 10:
            self.boss_activated = True
            self.boss.activate()

        if self.boss_activated:
            self.boss.update()

        for bullet in self.bullets:
            bullet.update()

        collision_utils.handle_collisions()

        bullets_to_remove = [bullet for bullet in self.bullets if bullet.should_remove]
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()

        if self.boss.dead:
            self.grass = Grass([(512, 0, 512)], current_stage=7)

        if self.boss_activated:
            self.boss.draw()
            health_ratio = max(self.boss.health / 200, 0)
            width = int(1024 * health_ratio)
            self.boss_blood_image.clip_draw(0, 0, width, 15, 1024 - width / 2, 753, width, 15)

        for bullet in self.bullets:
            bullet.draw()