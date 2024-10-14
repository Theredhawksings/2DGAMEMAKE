from pico2d import *
import random
import pygame

class Boy:
    def __init__(self):
        self.x, self.y = 80, 90
        self.frame = 0
        self.image = load_image('run_animation1.png')
        self.dx = 0

    def update(self):
        self.frame = (self.frame + 1) % 3
        self.x += self.dx

    def draw(self):
        self.image.clip_draw(self.frame * 64, 64, 64, 64, self.x, self.y, 64, 64)

class Ground:
    def __init__(self):
        self.image1 = load_image('Ground1.png')

    def draw(self):
        self.image1.draw(400,300)


def handle_events():
    global running, boy
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                key_states['left'] = True
            elif event.key == SDLK_RIGHT:
                key_states['right'] = True
            elif event.key == SDLK_SPACE:
                key_states['space'] = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LEFT:
                key_states['left'] = False
            elif event.key == SDLK_RIGHT:
                key_states['right'] = False
            elif event.key == SDLK_SPACE:
                key_states['space'] = False


def update_boy_movement():
    boy.dx, boy.dy = 0, 0
    if key_states['right']:
        boy.dx += 7
        boy.right = True
    if key_states['left']:
        boy.dx -= 7
        boy.right = False

def reset_world():
    global boy, running, key_states, ground
    key_states = {'left': False, 'right': False, 'space': False}
    boy = Boy()
    ground = Ground()
    running = True


def update_world():
    boy.update()
    update_boy_movement()

def render_world():
    clear_canvas()
    ground.draw()
    boy.draw()
    update_canvas()


open_canvas(800, 600)
reset_world()


while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()