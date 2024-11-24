from pico2d import *
import os

PIXEL_PER_METER = (10.0 / 0.3)
BOSS_SPEED_KMPH = 40.0
BOSS_SPEED_MPM = BOSS_SPEED_KMPH * 1000.0 / 60.0
BOSS_SPEED_MPS = BOSS_SPEED_MPM / 60.0
BOSS_SPEED_PPS = BOSS_SPEED_MPS * PIXEL_PER_METER

class Boss:
   def __init__(self):
       self.image = load_image(os.path.join('image', 'boss.png'))
       self.x = 900
       self.y = 940
       self.active = False
       self.vy = BOSS_SPEED_PPS
       self.y_min = 130
       self.y_max = 760
       self.width = 250
       self.height = 350
       self.boy = None
       self.health = 200
       self.dead = False
       self.death_speed = 100
       self.damage_sound = load_wav(os.path.join('bgm', 'damage7.mp3'))

   def activate(self):
       self.active = True

   def get_bb(self):
       return (self.x - 80, self.y - 130, self.x + 80, self.y + 130)

   def draw(self):
       self.image.clip_composite_draw(0, 0, 500, 600, 0, '', self.x, self.y, self.width, self.height)
       draw_rectangle(*self.get_bb())

   def update(self):
       if not self.active:
           return

       if self.dead:
           self.y -= self.death_speed * 0.16
           if self.y < -180:
               self.y = -180
           return

       self.y += self.vy * 0.016

       if self.y <= self.y_min:
           self.y = self.y_min
           self.vy = abs(self.vy)
       elif self.y >= self.y_max:
           self.y = self.y_max
           self.vy = -abs(self.vy)

       bullets_to_remove = [bullet for bullet in self.boy.stage.bullets if bullet.should_remove]
       for bullet in bullets_to_remove:
           if bullet in self.boy.stage.bullets:
               self.boy.stage.bullets.remove(bullet)

   def handle_collision(self, group, other):
       if group == 'bullet:boss' :
           self.health -= 2
           self.damage_sound.play()
           other.should_remove = True
           other.is_collided = True
           if self.health <= 0:
               self.dead = True