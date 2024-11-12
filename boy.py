from pico2d import *
import os
from state_machine import StateMachine, RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE
from state_machine import right_down, left_down, right_up, left_up, space_down

PIXEL_PER_METER = (10.0 / 0.3)

# 달리기 속도
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

# 점프 속도
JUMP_SPEED_MPS = 15.0
JUMP_SPEED_PPS = JUMP_SPEED_MPS * PIXEL_PER_METER

# 중력 가속도
GRAVITY_ACCEL = 9.8
GRAVITY_PPS = GRAVITY_ACCEL * PIXEL_PER_METER

class IdleState:
   @staticmethod
   def enter(boy, event):
       boy.frame = 0
       boy.dx = 0

   @staticmethod
   def exit(boy, event):
       pass

   @staticmethod
   def do(boy, grass):
       if boy.key_states['right'] and not boy.key_states['left']:
           boy.state_machine.add_event(('INPUT', RIGHT_DOWN))
       elif boy.key_states['left'] and not boy.key_states['right']:
           boy.state_machine.add_event(('INPUT', LEFT_DOWN))

       # 중력과 점프 처리
       boy.handle_gravity_and_jump(grass)

   @staticmethod
   def draw(boy):
       if boy.right:
           boy.image.clip_draw(boy.frame * 64, 64, 64, 64, boy.x, boy.y, 64, 64)
       else:
           boy.image.clip_draw(boy.frame * 64, 128, 64, 64, boy.x, boy.y, 64, 64)

class RunState:
   @staticmethod
   def enter(boy, event):
       if boy.key_states['right'] and not boy.key_states['left']:
           boy.dx = RUN_SPEED_PPS
           boy.right = True
       elif boy.key_states['left'] and not boy.key_states['right']:
           boy.dx = -RUN_SPEED_PPS
           boy.right = False

   @staticmethod
   def exit(boy, event):
       pass

   @staticmethod
   def do(boy, grass):
       # 이동 처리
       if boy.key_states['right'] and not boy.key_states['left']:
           boy.dx = RUN_SPEED_PPS
           boy.right = True
       elif boy.key_states['left'] and not boy.key_states['right']:
           boy.dx = -RUN_SPEED_PPS
           boy.right = False
       else:
           boy.dx = 0
           boy.state_machine.add_event(('INPUT', LEFT_UP))

       boy.x += boy.dx

       if boy.dx != 0:
           boy.frame = (boy.frame + 1) % 3

       # 중력과 점프 처리
       boy.handle_gravity_and_jump(grass)

   @staticmethod
   def draw(boy):
       if boy.right:
           boy.image.clip_draw(boy.frame * 64, 64, 64, 64, boy.x, boy.y, 64, 64)
       else:
           boy.image.clip_draw(boy.frame * 64, 128, 64, 64, boy.x, boy.y, 64, 64)

class Boy:
   def __init__(self):
       self.x, self.y = 80, 80
       self.frame = 0
       self.image = load_image(os.path.join('charcater', 'run_animation1.png'))
       self.dx = 0
       self.right = True
       self.is_jumping = False
       self.gravity = -GRAVITY_PPS
       self.jump_speed = 0
       self.key_states = {'left': False, 'right': False}
       self.apply_gravity = True
       self.savepointX = 0
       self.savepointY = 0
       self.previous_stage = None
       self.is_invincible = False
       self.time_since_last_frame = 0
       self.current_stage = None
       self.event_queue = []
       self.falling = False

       self.state_machine = StateMachine(self)
       self.state_machine.set_transitions({
           IdleState: {
               right_down: RunState,
               left_down: RunState,
           },
           RunState: {
               right_down: RunState,
               left_down: RunState,
               right_up: RunState,
               left_up: RunState,
               lambda e: (right_up(e) and not self.key_states['left']) or
                         (left_up(e) and not self.key_states['right']): IdleState,
           }
       })
       self.state_machine.start(IdleState)

   def handle_gravity_and_jump(self, grass):
       if self.apply_gravity:
           if self.is_jumping:
               self.y += self.jump_speed
               self.jump_speed += self.gravity

               if self.y > 768:  # 화면 위쪽 경계
                   self.y = 768
                   self.jump_speed = 0

               # 낙하 전환
               if self.jump_speed < 0:
                   self.is_jumping = False
                   self.falling = True

           # 낙하 중일 때
           if self.falling:
               self.y += self.gravity
               self.gravity = max(self.gravity - 1, -10)  # 중력 최대값을 -10으로 제한

               # 착지 체크
               if self.check_grass_collision(grass.get_positions()):
                   self.falling = False
                   self.gravity = -GRAVITY_PPS

           print(f" x={self.x:.2f}, y={self.y:.2f}")

   def update(self, grass):
       self.state_machine.update(grass)

       if self.apply_gravity and not self.is_jumping and not self.check_grass_collision(grass.get_positions()):
           self.falling = True
           self.gravity = max(self.gravity - 1, -10)

       # 화면 경계 체크
       if self.x < 0:
           self.x = 0
       elif self.x > 1024:
           self.x = 1024

   def handle_event(self, event):
       if event.type == SDL_KEYDOWN:
           if event.key == SDLK_LEFT:
               self.key_states['left'] = True
               self.add_event(('INPUT', LEFT_DOWN))
           elif event.key == SDLK_RIGHT:
               self.key_states['right'] = True
               self.add_event(('INPUT', RIGHT_DOWN))
           elif event.key == SDLK_SPACE:
               if not self.is_jumping and not self.falling:  # 점프 중이거나 떨어지는 중이 아닐 때만 점프
                   self.is_jumping = True
                   self.jump_speed = JUMP_SPEED_PPS
                   self.gravity = -GRAVITY_PPS
           elif event.key == ord('h'):
               self.is_invincible = not self.is_invincible

       elif event.type == SDL_KEYUP:
           if event.key == SDLK_LEFT:
               self.key_states['left'] = False
               self.frame = 0
               self.add_event(('INPUT', LEFT_UP))
           elif event.key == SDLK_RIGHT:
               self.key_states['right'] = False
               self.frame = 0
               self.add_event(('INPUT', RIGHT_UP))

   def check_grass_collision(self, grass_positions):
       collided = False

       for grass_x, grass_y, width in grass_positions:
           if (grass_x - width < self.x < grass_x + width and
                   self.y <= grass_y + 70 and self.y > grass_y + 40):
               self.y = grass_y + 50
               self.is_jumping = False
               self.jump_speed = 0
               self.gravity = -GRAVITY_PPS
               self.falling = False
               collided = True
               break

       if collided:
           self.is_on_ground = True
       else:
           self.is_on_ground = False

       return collided

   def add_event(self, event):
       self.event_queue.append(event)

   def draw(self):
       self.state_machine.cur_state.draw(self)

   def get_bb(self):
       if self.is_invincible:
           return 0, 0, 0, 0
       return self.x, self.y, self.x + 32, self.y + 32

   def update_stage_info(self, stage_number):
       self.previous_stage = self.current_stage
       self.current_stage = stage_number