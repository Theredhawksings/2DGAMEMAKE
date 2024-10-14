from pico2d import *
import random
import pygame


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
    global running
    running = True



reset_world()
open_canvas(800, 600)

while running:
    handle_events()
    delay(0.01)

close_canvas()