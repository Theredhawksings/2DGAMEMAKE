from pico2d import *
import random
import pygame

class Boy:
    def __init__(self):
        self.x, self.y = random.randint(0, 700), 90
        self.frame = 0
        self.image = load_image('run_animation1.png')

    def update(self):
        self.frame = (self.frame + 1) % 3

    def draw(self):
        self.image.clip_draw(self.frame * 64, 64, 64, 64, self.x, self.y, 64, 64)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False

def reset_world():
    global boy, running
    boy = Boy()
    running = True

def update_world():
    boy.update()

def render_world():
    clear_canvas()
    boy.draw()
    update_canvas()

open_canvas(800, 600)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()