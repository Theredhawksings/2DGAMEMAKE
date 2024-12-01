from pico2d import *
from boss import Boss
from grass import Grass
from ground import Ground
import collision_utils
from obstacle import *
import time
from random import randint
from font import Font

class Stage7:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.start_time = time.time()
        self.volume = 32


        self.boss_activated = False
        self.boss_activated_time = 0
        self.laser_pattern_started = False
        self.font = Font(30)

        self.boss_obstacle = BossObstacle([])
        self.boss_bomb = BossBomb([])
        self.boss_laser = BossLaser([])

        self.last_obstacle_time = time.time()
        self.last_bomb_time = time.time()
        self.last_laser_time = time.time()

        grass_positions = [
            (60, 150, 180),
            (60, 300, 180),
            (60, 450, 180),
            (60, 600, 180),
        ]

        self.grass = Grass(grass_positions, current_stage=7)
        self.ground = Ground(current_stage=7)
        self.stage_change_call = stage_change_call
        self.bullets = []

        self.boss = Boss()
        self.boss.boy = boy
        self.boy.update_stage_info(7)

        self.boss_obstacle.boss = self.boss
        self.boss_bomb.boss = self.boss
        self.boss_laser.boss = self.boss
        self.boss_blood_image = load_image(os.path.join('image', 'boss blood.png'))

        self.bomb_fired = False

        collision_utils.clear_collision_pairs()

        collision_utils.add_collision_pair('boy:boss_obstacle', boy, self.boss_obstacle)
        collision_utils.add_collision_pair('boy:boss_bomb', boy, self.boss_bomb)
        collision_utils.add_collision_pair('boy:boss_laser', boy, self.boss_laser)

        collision_utils.add_collision_pair('bullet:boss', self.bullets, self.boss)


    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)

        if self.boy.x < 2:
            self.boy.x = 2
            if self.boy.y == 45:
                self.boy.y = 45
        elif self.boy.x >= 1024:
            self.stage_change_call(8)

        if self.boy.y < -1:
            self.boy.x = 10
            self.boy.y = 760

        if not self.boss_activated and time.time() - self.start_time >= 22:
            self.boss_activated = True
            self.boss_activated_time = time.time()
            self.boss.activate()

        if self.boss_activated:
            self.boss.update()

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.should_remove:
                self.bullets.remove(bullet)

        if 'bullet:boss' in collision_utils.collision_pairs:
            collision_utils.collision_pairs['bullet:boss'][0] = self.bullets

        if self.boss_activated and not self.boss.dead:
            current_time = time.time()

            # 장애물 패턴
            if current_time - self.last_obstacle_time >= 1.3:
                self.boss_obstacle.obstacles.append({
                    'x': randint(50, 180),
                    'y': 780,
                    'move_speed': OBSTACLE_SPEED_PPS
                })
                self.last_obstacle_time = current_time

            # 폭탄 패턴
            if self.bomb_fired and abs(self.boss.y - self.boy.y) <= 20:
                self.boss_bomb.bomb.append({
                    'x': self.boss.x,
                    'y': self.boss.y,
                    'move_speed': 3.0
                })
                self.last_bomb_time = current_time
                self.bomb_fired = False

            if current_time - self.last_bomb_time >= 5.0 and not self.bomb_fired:
                self.bomb_fired = True

            # 레이저 패턴
            if not self.laser_pattern_started and current_time - self.boss_activated_time >= 10.0:
                self.laser_pattern_started = True
                self.last_laser_time = current_time

            if self.laser_pattern_started and current_time - self.last_laser_time >= 5.0:
                y_difference = abs(self.boss.y - self.boy.y)
                if y_difference <= 5:
                    self.boss_laser.lasers.append({
                        'x': self.boss.x - 145,
                        'y': self.boss.y,
                        'charging': True,
                        'charge_start': time.time()
                    })
                    self.last_laser_time = current_time


        self.boss_obstacle.update()
        self.boss_bomb.update()
        self.boss_laser.update()

        collision_utils.handle_collisions()

    def draw(self):
        if not self.boss_activated:
            self.ground.draw(512, 384)
            self.font.draw(320, 540, "여기까지 온다고 고생하셨습니다.", (255, 255, 255))
            self.font.draw(320, 460, "곧 보스가 나옵니다. 기다립시시오", (255, 255, 255))
            self.font.draw(320, 380, "보스 공격을 맞으면 보스는 체력을 회복합니다", (255, 255, 255))
        else:
            if not self.boss.dead:
                self.ground.update_stage(8)
                self.ground.draw(512, 384)
                self.grass.update_stage(8)
            else:
                self.ground.update_stage(7)
                self.ground.draw(512, 384)
                self.grass = Grass([(512, 0, 520), ], current_stage=7)

        self.grass.draw()
        self.boy.draw()

        if self.boss_activated:
            self.boss.draw()
            health_ratio = max(self.boss.health / 200, 0)
            width = int(1024 * health_ratio)
            x = 1024 - (1024 - width)
            self.boss_blood_image.clip_draw(0, 0, width, 15, x / 2, 753, width, 15)
            self.boss_obstacle.draw()
            self.boss_bomb.draw()
            self.boss_laser.draw()


        for bullet in self.bullets:
            bullet.draw()
