from pico2d import *
import os

import collision_utils
from bullet import Bullet
from state_machine import StateMachine, RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE
from state_machine import right_down, left_down, right_up, left_up, space_down
import time

PIXEL_PER_METER = (10.0 / 0.3)

RUN_SPEED_KMPH = 0.54
RUN_SPEED_MPM = RUN_SPEED_KMPH * 1000.0 / 60.0
RUN_SPEED_MPS = RUN_SPEED_MPM / 60.0
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

JUMP_SPEED_MPS = 0.36
JUMP_SPEED_PPS = JUMP_SPEED_MPS * PIXEL_PER_METER

GRAVITY_ACCEL = 0.032
GRAVITY_PPS = GRAVITY_ACCEL * PIXEL_PER_METER

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

frame_time = 0.0
current_time = time.time()

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
            boy.image.clip_draw(boy.frame * 64, 64, 64, 64, boy.x, boy.y, 48, 48)
        else:
            boy.image.clip_draw(boy.frame * 64, 128, 64, 64, boy.x, boy.y, 48, 48)

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
        frame_time = time.time() - current_time

        if boy.dx != 0:
            boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * frame_time) % 4

        # 중력과 점프 처리
        boy.handle_gravity_and_jump(grass)

    @staticmethod
    def draw(boy):
        if boy.right:
            boy.image.clip_draw(int(boy.frame) * 64, 64, 64, 64, boy.x, boy.y, 48, 48)
        else:
            boy.image.clip_draw(int(boy.frame) * 64, 128, 64, 64, boy.x, boy.y, 48, 48)

class Boy:
    def __init__(self):
        self.x, self.y = 80, 80
        self.frame = 0
        self.image = load_image(os.path.join('charcater', 'run_animation1.png'))
        self.dx = 0
        self.right = True
        self.is_jumping = False
        self.gravity = -GRAVITY_PPS
        self.gravity_increment = GRAVITY_PPS  # 중력 증가량
        self.max_gravity = GRAVITY_PPS * 12  # 최대 중력값
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

                if self.y > 768:
                    self.y = 768
                    self.jump_speed = 0

                if self.jump_speed < 0:
                    self.is_jumping = False
                    self.falling = True
                    self.gravity = -GRAVITY_PPS  # 낙하 시작할 때 중력 초기화

            if self.falling:
                self.y += self.gravity
                if abs(self.gravity) < self.max_gravity:
                    self.gravity -= self.gravity_increment

                if self.check_grass_collision(grass.get_positions()):
                    self.reset_jump_state()

            print(f" x={self.x:.2f}, y={self.y:.2f}, gravity={self.gravity:.2f}")

    def reset_jump_state(self):
        self.falling = False
        self.is_jumping = False
        self.jump_speed = 0
        self.gravity = -GRAVITY_PPS

    def handle_collision(self, group, other):
        if group == 'boy:obstacle' and not self.is_invincible:
            self.x = self.savepointX
            self.y = self.savepointY
            self.is_jumping = False
            self.jump_speed = 0
            self.gravity = -GRAVITY_PPS
            self.falling = False

    def update(self, grass):
        self.state_machine.update(grass)

        if self.apply_gravity and not self.is_jumping and not self.check_grass_collision(grass.get_positions()):
            self.falling = True
            if abs(self.gravity) < self.max_gravity:
                self.gravity -= self.gravity_increment


    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.key_states['left'] = True
                self.add_event(('INPUT', LEFT_DOWN))
            elif event.key == SDLK_RIGHT:
                self.key_states['right'] = True
                self.add_event(('INPUT', RIGHT_DOWN))
            elif event.key == SDLK_SPACE:
                if not self.is_jumping and not self.falling:
                    self.is_jumping = True
                    self.jump_speed = JUMP_SPEED_PPS
                    self.gravity = -GRAVITY_PPS
            elif event.key == ord('h'):
                self.is_invincible = not self.is_invincible
            elif event.key == ord('e'):
                bullet = Bullet(self.x, self.y - 5, self.right)
                self.stage.bullets.append(bullet)
                print(f"Bullet added at position: ({bullet.x}, {bullet.y})")
                collision_utils.clear_collision_pairs()
                collision_utils.add_collision_pair('bullet:boss', self.stage.bullets, [self.stage.boss])



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
                    self.y <= grass_y + 50 and self.y > grass_y + 30):
                self.y = grass_y + 45
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
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        if self.is_invincible:
            return 0, 0, 0, 0
        return self.x-12, self.y-25, self.x + 12, self.y + 15

    def update_stage_info(self, stage_number):
        self.previous_stage = self.current_stage
        self.current_stage = stage_number