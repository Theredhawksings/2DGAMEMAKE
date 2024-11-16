# main.py
from pico2d import *
import stage1
import stage2
import stage3
import stage4
import stage5
import pygame
from boy import Boy
import os

from game_world import GameWorld


def main():
    open_canvas(1024, 768)
    game_world = GameWorld()


    game_world.state = 'PLAY'
    game_world.change_stage(4)
    game_world.load_music(4)
    game_world.boy.x = 20
    game_world.boy.y = 100

    while game_world.running:
        game_world.handle_events()
        game_world.update()
        game_world.draw()s

    close_canvas()


if __name__ == '__main__':
    main()