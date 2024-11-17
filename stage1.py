# stage1.py
from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from font import Font
from bullet import Bullet
import collision_utils


class Stage1:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        grass_positions = [(512, 30, 512)]
        self.grass = Grass(grass_positions)
        self.ground = Ground(current_stage=1)

        obstacle_data = [
            (400, 65, 0, 0, 0),
            (600, 65, 0, 0, 0),
            (800, 65, 0, 0, 0),
            (200, 65, 0, 0, 0),
        ]
        self.obstacle = Obstacle(obstacle_data)

        self.stage_change_call = stage_change_call

        self.boy.savepointX = 80
        self.boy.savepointY = 80
        self.boy.update_stage_info(1)

        self.font = Font(30)

        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)
        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)
        
        self.bullets = []

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        if self.boy.x <= 1:
            self.boy.x = 1
            self.boy.y = 70
            self.boy.falling = False
            self.boy.gravity = -1
        elif self.boy.x >= 1024:
            self.stage_change_call(2)
            self.boy.x = 2
            self.boy.y = 700

        collision_utils.handle_collisions()

        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()

        self.font.draw(200, 490, "조작법", (0, 0, 0))
        self.font.draw(200, 450, "조작: ← → 이동, Space 점프", (0, 0, 0))
        self.font.draw(200, 410, "장애물에 닿이면 시작했던 곳으로 돌아가니 잘 하시길 바랍니다", (0, 0, 0))

        for bullet in self.bullets:
            bullet.draw()

