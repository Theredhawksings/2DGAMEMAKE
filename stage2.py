from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from collision_utils import check_collision, handle_collision

class Stage2:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        grass_positions = [(400, 650), (800, 100), (400, 330), (800, 500)]
        self.grass = Grass(grass_positions)
        self.ground = Ground(current_stage=2)

        obstacle_data = [
            (280, 680, 0),
            (400, 680, 0),
            (460, 755, 2),
            (600, 755, 2),
            (800, 680, 0),
            (200, 755, 2),
            (520, 680, 0),
            (680, 680, 0),
            (780, 680, 0)
        ]

        self.obstacle = Obstacle(obstacle_data)

        self.stage_change_call = stage_change_call

        self.boy.savepointX = 40
        self.boy.savepointY = 700

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        if self.boy.x < 1 and self.boy.y == 700:
            self.boy.x = 1020
            self.boy.y = 80
            self.stage_change_call(1)

        elif self.boy.x > 1024:
            self.boy.x = 1024

        elif self.boy.x <= 280 and self.boy.y < 0:
            self.stage_change_call(3)

        for x, y, angle_index in self.obstacle.obstacles:
            if check_collision(self.boy, x, y, angle_index):
                handle_collision(self.boy)
                break

    def draw(self):
        self.ground.draw(512, 384)
        self.grass.draw()
        self.boy.draw()
        self.obstacle.draw()