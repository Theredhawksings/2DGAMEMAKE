from pico2d import load_image, draw_rectangle
import math, os

PIXEL_PER_METER = (10.0 / 0.3)

OBSTACLE_SPEED_KMPH = 0.108
OBSTACLE_SPEED_MPM = OBSTACLE_SPEED_KMPH * 1000.0 / 60.0
OBSTACLE_SPEED_MPS = OBSTACLE_SPEED_MPM / 60.0
OBSTACLE_SPEED_PPS = OBSTACLE_SPEED_MPS * PIXEL_PER_METER  # = 1 픽셀/프레임

class Obstacle:
    death_count = 0

    def __init__(self, obstacle_data):
        self.image = load_image(os.path.join('obstacle', 'obstacle.png'))
        self.obstacles = []
        self.angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]
        self.screen_width = 1024
        self.screen_height = 768

        for x, y, image_direction, move_direction, move_speed in obstacle_data:
            self.obstacles.append({
                'x': x,
                'y': y,
                'image_direction': image_direction,
                'move_direction': move_direction,
                'move_speed': OBSTACLE_SPEED_PPS * move_speed
            })


    def get_bb(self):
        bbs = []
        for obstacle in self.obstacles:
            if obstacle['image_direction'] == 0 or obstacle['image_direction'] == 2:
                bb = (obstacle['x'] - 8,
                      obstacle['y'] - 13,
                      obstacle['x'] + 8,
                      obstacle['y'] + 8)
            else:
                bb = (obstacle['x'] - 15,
                      obstacle['y'] - 15,
                      obstacle['x'] + 15,
                      obstacle['y'] + 15)
            bbs.append(bb)
        return bbs

    def draw(self):
        for obstacle, bb in zip(self.obstacles, self.get_bb()):
            angle = self.angles[obstacle['image_direction']]
            self.image.clip_composite_draw(0, 0, 100, 120,
                                        angle,
                                        '',
                                        obstacle['x'],
                                        obstacle['y'],
                                        25, 30)
            draw_rectangle(*bb)  # 충돌 박스 표시

    def update(self):
        obstacles_to_remove = []
        for obstacle in self.obstacles:
            if obstacle['move_direction'] == 1:
                obstacle['x'] += obstacle['move_speed']
            elif obstacle['move_direction'] == 2:
                obstacle['x'] -= obstacle['move_speed']
            elif obstacle['move_direction'] == 3:
                obstacle['y'] -= obstacle['move_speed']
            elif obstacle['move_direction'] == 4:
                obstacle['y'] += obstacle['move_speed']

            if (obstacle['x'] < -30 or obstacle['x'] > 1054 or
                    obstacle['y'] < -30 or obstacle['y'] > 798):
                obstacles_to_remove.append(obstacle)

        for obstacle in obstacles_to_remove:
            if obstacle in self.obstacles:
                self.obstacles.remove(obstacle)

    def check_collision(self, boy):
        if boy.is_invincible:
            return False

        for obstacle, bb in zip(self.obstacles, self.get_bb()):
            boy_left, boy_bottom, boy_right, boy_top = boy.get_bb()
            obstacle_left, obstacle_bottom, obstacle_right, obstacle_top = bb

            if boy_right < obstacle_left: continue
            if boy_left > obstacle_right: continue
            if boy_top < obstacle_bottom: continue
            if boy_bottom > obstacle_top: continue

            collision_direction = ""
            if boy_right >= obstacle_left and boy_left < obstacle_left:
                collision_direction = "왼쪽"
            elif boy_left <= obstacle_right and boy_right > obstacle_right:
                collision_direction = "오른쪽"
            elif boy_top >= obstacle_bottom and boy_bottom < obstacle_bottom:
                collision_direction = "아래쪽"
            elif boy_bottom <= obstacle_top and boy_top > obstacle_top:
                collision_direction = "위쪽"

            print(
                f"충돌 감지: 소년({boy_left}, {boy_bottom}, {boy_right}, {boy_top}), "
                f"장애물({obstacle_left}, {obstacle_bottom}, {obstacle_right}, {obstacle_top}), "
                f"방향: {obstacle['image_direction']}, 충돌 방향: {collision_direction}"
            )

            Obstacle.death_count += 1
            self.handle_collision(boy)
            return True

        return False

    def handle_collision(self, boy):
        boy.x = boy.savepointX
        boy.y = boy.savepointY
        boy.is_jumping = False
        boy.jump_speed = 0
        boy.frame = 0
        boy.falling = False
        print(f'충돌 발생! 세이브포인트로 이동: x={boy.x}, y={boy.y}')

    @staticmethod
    def get_death_count():
        return Obstacle.death_count

    def check_collisions(self, boy):
        return self.check_collision(boy)