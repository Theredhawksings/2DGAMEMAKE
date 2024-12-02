# stage1.py
from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
from font import Font
from bullet import Bullet
import collision_utils
from savepoint import SavePoint

class Stage1:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.grass = Grass([(512, 30, 514)])
        self.ground = Ground(current_stage=1)

        self.obstacle = Obstacle([
            (400, 65, 0, 0, 0),
            (600, 65, 0, 0, 0),
            (800, 65, 0, 0, 0),
            (200, 65, 0, 0, 0)
        ])

        self.stage_change_call = stage_change_call

        self.boy.savepointX = 80
        self.boy.savepointY = 80
        self.boy.update_stage_info(1)


        self.fonts = [
            {"font": Font(30), "x": 200, "y": 490, "text": "조작법", "color": (0, 0, 0)},
            {"font": Font(30), "x": 200, "y": 450, "text": "조작: ← → 이동, Space 점프, e 총알 발사", "color": (0, 0, 0)},
            {"font": Font(30), "x": 200, "y": 410, "text": "장애물에 닿으면 시작했던 곳으로 돌아가니 잘 하시길 바랍니다", "color": (0, 0, 0)},
            {"font": Font(30), "x": 230, "y": 370, "text": "<- 세이브 포인트에다가 총알을 발사해서 위치를 저장하세요", "color": (0, 0, 0)},
            {"font": Font(30), "x": 230, "y": 330, "text": "ESC 누르면 일시정지 됩니다", "color": (0, 0, 0)},
        ]

        savepoint_positions = [
            (210, 370)
        ]
        self.savepoints = [SavePoint(x, y, 1) for x, y in savepoint_positions]

        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

        self.bullets = []
        self.world = []
        self.world.append(self.ground)
        self.world.append(self.grass)
        self.world.extend(self.savepoints)
        self.world.append(self.boy)
        self.world.append(self.obstacle)
        self.world.append(self.bullets)
        self.world.extend(self.fonts)

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        self.boy.update(self.grass)
        self.obstacle.update()

        if self.boy.x <= 1:
            self.boy.x = 1
            self.boy.y = 75
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
        for obj in self.world:
            if isinstance(obj, list):
                for sub_obj in obj:
                    sub_obj.draw()
            elif isinstance(obj, Ground):
                obj.draw(512, 384)
            elif isinstance(obj, dict) and "font" in obj:  # 폰트 객체일 경우 처리
                font = obj["font"]
                x = obj["x"]
                y = obj["y"]
                text = obj["text"]
                color = obj["color"]
                font.draw(x, y, text, color)
            else:
                obj.draw()





