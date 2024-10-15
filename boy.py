from pico2d import load_image
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT

class Boy:
    def __init__(self):
        self.x, self.y = 80, 80
        self.frame = 0
        self.image = load_image('run_animation1.png')
        self.dx = 0
        self.right = True
        self.is_jumping = False
        self.gravity = -1
        self.ground_y = 80
        self.jump_speed = 0
        self.key_states = {'left': False, 'right': False}

    def update(self):
        self.dx = 0
        if self.key_states['right']:
            self.dx += 7
            self.right = True
        if self.key_states['left']:
            self.dx -= 7
            self.right = False

        if self.is_jumping:
            self.y += self.jump_speed
            self.jump_speed += self.gravity
            if self.y <= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.jump_speed = 0

        if (self.dx!=0):
            self.frame = (self.frame + 1) % 3
        self.x += self.dx

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_speed = 13

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