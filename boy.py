from pico2d import load_image
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
import grass


class Boy:
    def __init__(self):
        self.x, self.y = 80, 80
        self.frame = 0
        self.image = load_image('run_animation1.png')
        self.dx = 0
        self.right = True
        self.is_jumping = False
        self.jump_gravity = -1
        self.fall_gravity = -1
        self.ground_y = 80
        self.jump_speed = 0
        self.key_states = {'left': False, 'right': False}
        self.falling = False
        self.height = 48
        self.apply_gravity = True
        self.savepointX = 0
        self.savepointY = 0
        self.previous_stage = None

    def update(self, grass):
        self.dx = 0

        if self.key_states['right']:
            self.dx += 5
            self.right = True
        if self.key_states['left']:
            self.dx -= 5
            self.right = False

        if self.is_jumping or self.falling:
            self.dx = max(min(self.dx, 5), -5)

        self.x += self.dx

        if self.apply_gravity:
            if self.is_jumping:
                next_y = self.y + self.jump_speed

                self.y = next_y
                self.jump_speed += self.jump_gravity

                if self.y > 768:
                    self.y = 768
                    self.jump_speed = 0

                if self.jump_speed < 0:
                    self.check_grass_collision(grass.get_positions())
            else:
                self.check_grass_collision(grass.get_positions())

            if self.falling:
                self.y += self.fall_gravity
                self.fall_gravity -= 1
                self.check_grass_collision(grass.get_positions())

        if (self.dx != 0):
            self.frame = (self.frame + 1) % 3

        if (self.x < 0):
            self.x = 0

        print(f" x={self.x:.2f}, y={self.y:.2f}")

    def check_grass_collision(self, grass_positions):
        self.falling = True
        for grass_x, grass_y, width in grass_positions:
            if (grass_x - width < self.x < grass_x + width and self.y <= grass_y + 70 and self.y > grass_y + 45):
                self.y = grass_y + 50
                self.ground_y = grass_y + 50
                self.is_jumping = False
                self.jump_speed = 0
                self.fall_gravity = -1
                self.falling = False
                print(f"풀 위치 x={grass_x:.2f}, y={grass_y:.2f}")
                break

    def jump(self):
        if not self.is_jumping and not self.falling:
            self.is_jumping = True
            self.jump_speed = 12

    def draw(self):
        if self.right:
            self.image.clip_draw(self.frame * 64, 64, 64, 64, self.x, self.y, 64, 64)
        else:
            self.image.clip_draw(self.frame * 64, 128, 64, 64, self.x, self.y, 64, 64)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.key_states['left'] = True
            elif event.key == SDLK_RIGHT:
                self.key_states['right'] = True
            elif event.key == SDLK_SPACE:
                self.jump()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                self.key_states['left'] = False
            elif event.key == SDLK_RIGHT:
                self.key_states['right'] = False
            self.frame = 0

    def get_bb(self):
        return self.x, self.y, self.x + 32, self.y + 32

    def update_stage_info(self, stage_number):  # 스테이지 정보를 업데이트하는 메서드 추가
        self.previous_stage = stage_number

