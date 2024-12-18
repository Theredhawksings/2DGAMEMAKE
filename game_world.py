import os
import time
from pico2d import *
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

from boy import Boy, IdleState
from stage1 import Stage1
from stage2 import Stage2
from stage3 import Stage3
from stage4 import Stage4
from stage5 import Stage5
from stage6 import Stage6
from stage7 import Stage7
from stage8 import Stage8


class MusicManager:
    def __init__(self):
        self.current_music = None
        self.bgm = None
        self.volume = 32  # 기본 볼륨 (0 ~ 128)

    def load_music(self, music_path):
        if self.current_music != music_path:
            if self.bgm is not None:
                self.stop_music()
            self.bgm = load_music(music_path)
            self.bgm.set_volume(self.volume)
            self.bgm.repeat_play()
            self.current_music = music_path

    def stop_music(self):
        if self.bgm is not None:
            self.bgm.stop()
            self.current_music = None

    def pause_music(self):
        if self.bgm is not None:
            self.bgm.pause()

    def unpause_music(self):
        if self.bgm is not None:
            self.bgm.resume()

    def set_volume(self, volume):
        self.volume = max(0, min(volume, 128))  # 볼륨 범위 제한 (0 ~ 128)
        if self.bgm is not None:
            self.bgm.set_volume(self.volume)


class MusicController:
    def __init__(self, game_world):
        self.game_world = game_world
        self.music_manager = game_world.music_manager
        self.stage_change_time = None
        self.current_stage = None

    def handle_stage_music(self, stage_number):
        self.stage_change_time = time.time()
        self.current_stage = stage_number

        if stage_number == 7:
            self.music_manager.stop_music()
        else:
            self.load_stage_music(stage_number)

    def load_stage_music(self, stage_number):
        if stage_number in [1, 2, 3]:
            music_path = os.path.join('bgm', 'Monster.mp3')
        elif stage_number in [4, 5, 6]:
            music_path = os.path.join('bgm', 'sleepwood.mp3')
        elif stage_number == 8:
            music_path = os.path.join('bgm', 'Different_Heaven_Even_Better_Feat_Sian.mp3')
        else:
            return

        self.music_manager.load_music(music_path)

    def update(self):
        if self.current_stage == 7:
            current_time = time.time()
            if 2.0 <= current_time - self.stage_change_time < 22:
                music_path = os.path.join('bgm', 'Hello Kitty and Friends - Intro Theme (closed captions).mp3')
                self.music_manager.load_music(music_path)
                self.music_manager.set_volume(80)
            elif current_time - self.stage_change_time >= 22:
                music_path = os.path.join('bgm', 'Boss 1 - Hell(o) Kitty.mp3')
                self.music_manager.load_music(music_path)
                self.music_manager.set_volume(12)


class GameWorld:
    def __init__(self):
        self.current_stage = None
        self.running = True
        self.last_stage = 1
        self.boy = Boy()
        self.boy.game_world = self
        self.state = 'LOGO'
        self.logo_time = 0.0
        self.logo_image = load_image(os.path.join('screen', '3570144307.png'))
        self.intro_image = load_image(os.path.join('screen', 'Intro.png'))
        self.music_manager = MusicManager()
        self.music_controller = MusicController(self)

        self.music_manager.load_music(os.path.join('bgm', 'Eagle_sing.mp3'))

    def change_stage(self, stage_number):
        stage_classes = [None, Stage1, Stage2, Stage3, Stage4, Stage5, Stage6, Stage7, Stage8]

        if 1 <= stage_number <= 8:
            stage_class = stage_classes[stage_number]
            self.current_stage = stage_class(self.change_stage, self.boy)
            self.music_controller.handle_stage_music(stage_number)

        self.last_stage = stage_number

    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.running = False
            elif event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    if self.state == 'PLAY':
                        self.state = 'PAUSE'
                        self.music_manager.pause_music()
                        self.boy.key_states['left'] = False
                        self.boy.key_states['right'] = False
                        self.boy.event_queue.clear()
                        self.boy.state_machine.start(IdleState)
                    elif self.state == 'PAUSE':
                        self.state = 'PLAY'
                        self.music_manager.unpause_music()
                    else:
                        self.running = False
                    continue

                elif self.state == 'INTRO' and event.key == SDLK_SPACE:
                    self.state = 'PLAY'
                    self.music_controller.load_stage_music(self.last_stage)
                    self.change_stage(1)
                    self.boy.x = 15
                    self.boy.y = 100
                    continue

            if self.state == 'PLAY':
                self.current_stage.handle_event(event)

    def update(self):
        if self.state == 'LOGO':
            self.logo_time += 0.01
            if self.logo_time >= 2.0:
                self.state = 'INTRO'
                self.music_manager.stop_music()
                self.music_manager.load_music(os.path.join('bgm', "102. Lucas' Theme.mp3"))
        elif self.state == 'PLAY':
            self.current_stage.update()
            self.music_controller.update()

    def draw(self):
        clear_canvas()
        if self.state == 'LOGO':
            self.logo_image.draw(512, 384)
        elif self.state == 'INTRO':
            self.intro_image.draw(512, 384)
        elif self.state in ['PLAY', 'PAUSE']:
            self.current_stage.draw()
        update_canvas()
