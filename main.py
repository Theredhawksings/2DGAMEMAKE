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


class GameWorld:
    def __init__(self):
        self.current_stage = None
        self.running = True
        self.last_stage = 1
        self.boy = Boy()
        self.current_music = None

    def load_music(self, stage_number):
        if stage_number in [1, 2, 3]:
            # music_path = os.path.join('bgm', 'Green Greens.mp3')
            music_path = os.path.join('bgm', '1,000,000 Monsters Attack.mp3')
        elif stage_number in [4, 5]:
            # music_path = os.path.join('bgm', 'sleepwood.mp3')
            music_path = os.path.join('bgm', '1,000,000 Monsters Attack.mp3')
        else:
            return

        if self.current_music != music_path:
            if self.current_music is not None:
                pygame.mixer.music.stop()
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play(-1)
            self.current_music = music_path

    def change_stage(self, stage_number):
        self.load_music(stage_number)  # 음악 로드

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
            else:
                self.current_stage.handle_event(event)

    def update(self):
        self.current_stage.update()

    def draw(self):
        clear_canvas()
        self.current_stage.draw()
        update_canvas()


def main():
    open_canvas(1024, 768)
    game_world = GameWorld()
    game_world.change_stage(4)
    game_world.boy.x = 15
    game_world.boy.y = 70

    while game_world.running:
        game_world.handle_events()
        game_world.update()
        game_world.draw()
        delay(0.01)

    close_canvas()


if __name__ == '__main__':
    main()
