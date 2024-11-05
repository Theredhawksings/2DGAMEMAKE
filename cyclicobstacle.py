from pico2d import load_image, draw_rectangle
import math, os
import time


class CyclicObstacle:
    def __init__(self, x, y, image_direction, move_direction, move_speed, active_time=3.0, inactive_time=2.0):
        self.image = load_image(os.path.join('obstacle', 'obstacle.png'))
        self.angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]

        self.x = x
        self.y = y
        self.original_x = x
        self.original_y = y
        self.image_direction = image_direction
        self.move_direction = move_direction
        self.move_speed = move_speed

        self.active_time = active_time
        self.inactive_time = inactive_time
        self.start_time = time.time()
        self.is_active = True

        self.death_count = 0

    def update(self):
        current_time = time.time()
        cycle_time = self.active_time + self.inactive_time
        elapsed_time = (current_time - self.start_time) % cycle_time

        self.is_active = elapsed_time < self.active_time

        if self.is_active:
            if self.move_direction == 1:
                self.x += self.move_speed
            elif self.move_direction == 2:
                self.x -= self.move_speed
            elif self.move_direction == 3:
                self.y -= self.move_speed
            elif self.move_direction == 4:
                self.y += self.move_speed
        else:
            self.x = self.original_x
            self.y = self.original_y

    def draw(self):
        if self.is_active:
            angle = self.angles[self.image_direction]
            self.image.clip_composite_draw(0, 0, 100, 120,
                                           angle,
                                           '',
                                           self.x,
                                           self.y,
                                           25, 30)

    def get_bb(self):
        if not self.is_active:
            return None

        if self.image_direction == 0 or self.image_direction == 2:
            left = self.x + 15
            right = self.x + 17
            bottom = self.y
            top = self.y + 20

        else:
            left = self.x
            right = self.x + 25
            bottom = self.y + 10
            top = self.y + 20

        return left, bottom, right, top

    def check_collision(self, boy):
        if not self.is_active:
            return False

        boy_left, boy_bottom, boy_right, boy_top = boy.get_bb()
        obstacle_left, obstacle_bottom, obstacle_right, obstacle_top = self.get_bb()

        if boy_right < obstacle_left: return False
        if boy_left > obstacle_right: return False
        if boy_top < obstacle_bottom: return False
        if boy_bottom > obstacle_top: return False

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
            f"방향: {self.image_direction}, 충돌 방향: {collision_direction}"
        )

        self.death_count += 1

        return True