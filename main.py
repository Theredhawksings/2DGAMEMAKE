from pico2d import *
import pygame
from stage1 import Stage1
# from stage2 import Stage2  # 추후 추가

class GameWorld:
    def __init__(self):
        self.current_stage = None
        self.running = True

    def change_stage(self, new_stage):
        self.current_stage = new_stage

    def handle_events(self):
        events = get_events()
        for event in events:
            if event.type == SDL_QUIT:
                self.running = False
            elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
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
    game_world.change_stage(Stage1())

    pygame.mixer.init()
    pygame.mixer.music.load("Green Greens.mp3")
    pygame.mixer.music.play(-1)

    while game_world.running:
        game_world.handle_events()
        game_world.update()
        game_world.draw()
        delay(0.01)

    close_canvas()

if __name__ == '__main__':
    main()