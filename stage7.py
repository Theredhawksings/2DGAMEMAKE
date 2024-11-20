from pico2d import *
from boss import Boss
from grass import Grass
from ground import Ground
import collision_utils
from obstacle import BossObstacle, OBSTACLE_SPEED_PPS
import time
from random import randint

class Stage7:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.start_time = time.time()
        self.boss_activated = False

        self.boss_obstacle = BossObstacle([])
        self.last_obstacle_time = time.time()

        #collision_utils.add_collision_pair('boy:boss_obstacle', [self.boy], [self.boss_obstacle])

        grass_positions = [
            (20, 0, 180),
            (20, 150, 180),
            (20, 300, 180),
            (20, 450, 180),
            (20, 600, 180),
        ]

        self.grass = Grass(grass_positions, current_stage=7)

        self.ground = Ground(current_stage=7)
        self.stage_change_call = stage_change_call
        self.bullets = []
        self.boss = Boss()
        self.boss.boy = boy
        self.boy.update_stage_info(7)
        self.boss_obstacle.boss = self.boss

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

        if self.boss_activated and not self.boss.dead:
            current_time = time.time()
            if current_time - self.last_obstacle_time >= 3.0:
                self.boss_obstacle.obstacles.append({
                    'x': randint(50, 180),
                    'y': 780,
                    'move_speed': OBSTACLE_SPEED_PPS
                })
                self.last_obstacle_time = current_time

        self.boss_obstacle.update()

    def draw(self):
        if not self.boss_activated:
            self.ground.draw(512, 384)
        else:
            if not self.boss.dead:
                self.ground.update_stage(8)
                self.ground.draw(512, 384)
                self.grass.update_stage(8)
            else:
                self.ground.update_stage(7)
                self.ground.draw(512, 384)
                self.grass = Grass([(512, 0, 512)], current_stage=7)

        self.grass.draw()
        self.boy.draw()

        if self.boss_activated:
            self.boss.draw()
            health_ratio = max(self.boss.health / 200, 0)
            width = int(1024 * health_ratio)
            x = 1024 - (1024 - width)
            self.boss_blood_image.clip_draw(0, 0, width, 15, x / 2, 753, width, 15)

        for bullet in self.bullets:
            bullet.draw()

        self.boss_obstacle.draw()