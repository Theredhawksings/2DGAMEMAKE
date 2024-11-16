# cyclic_obstacle.py
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
           self.draw_collision_box()

   def draw_collision_box(self):
       left, bottom, right, top = self.get_bb()
       draw_rectangle(left, bottom, right, top)

   def get_bb(self):
       if not self.is_active:
           return 0, 0, 0, 0

       if self.image_direction == 0 or self.image_direction == 2:
           left = self.x - 10
           right = self.x + 10
           bottom = self.y - 15
           top = self.y + 10
       else:
           left = self.x - 15
           right = self.x + 15
           bottom = self.y - 15
           top = self.y + 15

       return left, bottom, right, top

   def handle_collision(self, group, other):
       if group == 'boy:cyclic_obstacle' and self.is_active:
           self.death_count += 1
           other.x = other.savepointX
           other.y = other.savepointY