# game_world.py
import os
import pygame
from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import stage1
import stage2
import stage3
import stage4
import stage5
from boy import Boy

class GameWorld:
   def __init__(self):
       self.current_stage = None
       self.running = True
       self.last_stage = 1
       self.boy = Boy()
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
           #music_path = os.path.join('bgm', '1,000,000 Monsters Attack.mp3')
       elif stage_number in [4, 5]:
           music_path = os.path.join('bgm', 'sleepwood.mp3')
           #music_path = os.path.join('bgm', '1,000,000 Monsters Attack.mp3')
       else:
           return

       if self.current_music != music_path:
           if self.current_music is not None:
               pygame.mixer.music.stop()
           pygame.mixer.music.load(music_path)
           pygame.mixer.music.play(-1)
           self.current_music = music_path

   def change_stage(self, stage_number):
       if stage_number == 1:
           self.current_stage = stage1.Stage1(self.change_stage, self.boy)
       elif stage_number == 2:
           self.current_stage = stage2.Stage2(self.change_stage, self.boy)
       elif stage_number == 3:
           self.current_stage = stage3.Stage3(self.change_stage, self.boy)
       elif stage_number == 4:
           self.current_stage = stage4.Stage4(self.change_stage, self.boy)
       elif stage_number == 5:
           self.current_stage = stage5.Stage5(self.change_stage, self.boy)

       self.last_stage = stage_number

   def handle_events(self):
       events = get_events()
       for event in events:
           if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
               self.running = False
           elif self.state == 'INTRO' and event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
               self.state = 'PLAY'
               self.load_music(self.last_stage)
               self.change_stage(1)
               self.boy.x = 15
               self.boy.y = 100
           else:
               if self.state == 'PLAY':
                   self.current_stage.handle_event(event)

   def update(self):
       if self.state == 'LOGO':
           self.logo_time += 0.01
           if self.logo_time >= 2.0:
               self.state = 'INTRO'
       elif self.state == 'PLAY':
           self.current_stage.update()

   def draw(self):
       clear_canvas()
       if self.state == 'LOGO':
           self.logo_image.draw(512, 384)
       elif self.state == 'INTRO':
           self.intro_image.draw(512, 384)  # 인트로 화면 표시
       elif self.state == 'PLAY':
           self.current_stage.draw()
       update_canvas()