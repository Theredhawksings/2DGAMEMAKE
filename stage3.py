# game_world.py
import os
import pygame
from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import stage1, stage2, stage3, stage4, stage5, stage6
from boy import Boy


class GameWorld:
    def __init__(self):
        self.current_stage = None
        self.running = True
        self.last_stage = 1
        self.boy = Boy()
        self.boy.game_world = self  # Boy에게 game_world 참조 추가
        self.current_music = None
        self.state = 'LOGO'
        self.logo_time = 0.0
        self.logo_image = load_image(os.path.join('screen', '3570144207.png'))
        self.intro_image = load_image(os.path.join('screen', 'Intro.png'))
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join('bgm', 'Eagle_sing.mp3'))
        pygame.mixer.music.play(-1)

    def load_music(self, stage_number):
        if stage_number in [1, 2, 3]:
            music_path = os.path.join('bgm', 'Monster.mp3')
        elif stage_number in [4, 5, 6]:
            music_path = os.path.join('bgm', 'sleepwood.mp3')
        else:
            return

        if self.current_music != music_path:
            if self.current_music is not None:
                pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            self.current_music = music_path

    def change_stage(self, stage_number):
        stage_classes = [
            None, stage1.Stage1, stage2.Stage2, stage3.Stage3,
            stage4.Stage4, stage5.Stage5, stage6.Stage6,
        ]

        if 1 <= stage_number <= 7:
            stage_class = stage_classes[stage_number]
            self.current_stage = stage_class(self.change_stage, self.boy)

        self.last_stage = stage_number
        self.load_music(stage_number)

    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.running = False
            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    if self.state == 'PLAY':
                        self.state = 'PAUSE'
                        pygame.mixer.music.pause()
                    elif self.state == 'PAUSE':
                        self.state = 'PLAY'
                        pygame.mixer.music.unpause()
                    else:
                        self.running = False
                elif self.state == 'INTRO' and event.key == SDLK_SPACE:
                    self.state = 'PLAY'
                    self.load_music(self.last_stage)
                    self.change_stage(1)
                    self.boy.x = 15
                    self.boy.y = 100

            if self.state == 'PLAY':  # PLAY 상태일 때만 이벤트 처리
                self.current_stage.handle_event(event)

    def update(self):
        if self.state == 'LOGO':
            self.logo_time += 0.01
            if self.logo_time >= 2.0:
                self.state = 'INTRO'
                pygame.mixer.music.stop()
                pygame.mixer.music.load(os.path.join('bgm', "102. Lucas' Theme.mp3"))
                pygame.mixer.music.play(-1)
        elif self.state == 'PLAY':
            self.current_stage.update()

    def draw(self):
        clear_canvas()
        if self.state == 'LOGO':
            self.logo_image.draw(512, 384)
        elif self.state == 'INTRO':
            self.intro_image.draw(512, 384)
        elif self.state in ['PLAY', 'PAUSE']:
            self.current_stage.draw()
        update_canvas()


# stage3.py
from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
import collision_utils
import random
import time


class Stage3:
    def __init__(self, stage_change_call, boy):
        self.boy = boy
        self.boy.stage = self
        self.ground = Ground(current_stage=3)
        self.stage_change_call = stage_change_call

        is_from_stage4 = self.boy.previous_stage == 4
        self.background_y = 384 if is_from_stage4 else 5229
        self.boy.x = 1020 if is_from_stage4 else 512
        self.boy.y = 50 if is_from_stage4 else 630

        self.boy.apply_gravity = False
        self.grass = Grass([(512, 0, 512)], current_stage=3)
        self.time = time.time()
        self.last_obstacle_time = time.time()
        self.obstacle = Obstacle([])

        self.boy.update_stage_info(3)
        collision_utils.clear_collision_pairs()
        collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

        self.bullets = []

    def handle_event(self, event):
        self.boy.handle_event(event)

    def update(self):
        if self.boy.game_world.state == 'PAUSE':
            return

        self.boy.update(self.grass)
        self.obstacle.update()

        if self.background_y < 400 and self.boy.apply_gravity == False:
            self.boy.y -= 2

        if self.background_y <= 384:
            self.background_y = 384

        if self.boy.y < 50:
            self.boy.y = 50
            self.boy.apply_gravity = True
            self.boy.falling = False
            self.boy.is_jumping = False

        if self.boy.x < 1:
            self.boy.x = 1
        elif self.boy.y == 45 and self.boy.x > 1024:
            self.boy.x = 1024

        current_time = time.time()

        if current_time - self.last_obstacle_time >= 0.08 and self.background_y > 400:
            new_obstacle = {
                'x': random.randint(0, 1024),
                'y': -20,
                'image_direction': 0,
                'move_direction': 4,
                'move_speed': 7
            }
            self.obstacle.obstacles.append(new_obstacle)
            self.last_obstacle_time = current_time

        if current_time % 0.1 <= 0.01:
            self.boy.y -= 1

        if collision_utils.collide(self.boy, self.obstacle):
            self.boy.x = 310
            self.boy.y = 150
            self.boy.apply_gravity = True
            self.stage_change_call(2)

        if self.boy.x >= 1024 and self.boy.y == 50:
            self.boy.x = 30
            self.boy.y = 45
            self.stage_change_call(4)

        for bullet in self.bullets:
            bullet.update()

        if self.boy.game_world.state != 'PAUSE':
            self.background_y -= 3

    def draw(self):
        self.ground.falling_draw(512, 384, self.background_y)

        if self.background_y < 400:
            self.grass.draw()

        self.boy.draw()
        self.obstacle.draw()

        for bullet in self.bullets:
            bullet.draw()