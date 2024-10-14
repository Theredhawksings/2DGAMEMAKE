from pico2d import *
import random
import pygame

class Boy:
    def __init__(self):
        self.x, self.y = 80, 80
        self.frame = 0
        self.image = load_image('run_animation1.png')
        self.dx = 0
        self.right = True

    def update(self):
        self.dx = 0
        if key_states['right']:
            self.dx += 7
            self.right = True
        if key_states['left']:
            self.dx -= 7
            self.right = False

        if(self.dx!=0):
            self.frame = (self.frame + 1) % 3
        self.x += self.dx

    def draw(self):
        if self.right:
            self.image.clip_draw(self.frame * 64, 64, 64, 64, self.x, self.y, 64, 64)
        else:
            self.image.clip_draw(self.frame * 64, 128, 64, 64, self.x, self.y, 64, 64)

class Ground:
    def __init__(self):
        self.image1 = load_image('Ground1.png')

    def draw(self):
        self.image1.draw(400,300)

class Grass:
    def __init__(self):
        self.frame = 0
        self.image = load_image('grass.png')

    def draw(self,x, y):
        self.image.draw(x,y)

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
            boy.frame = 0

def reset_world():
    global boy, running, key_states, ground, grass
    key_states = {'left': False, 'right': False, 'space': False}
    boy = Boy()
    ground = Ground()
    grass = Grass()
    running = True


def update_world():
    boy.update()

def render_world():
    clear_canvas()
    ground.draw()
    grass.draw(400,30)
    boy.draw()
    update_canvas()


open_canvas(800, 600)
reset_world()


pygame.mixer.init()
pygame.mixer.music.load("Green Greens.mp3")
pygame.mixer.music.play(-1)  # -1은 무한 반복을 의미합니다

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()