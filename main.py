# main.py
from pico2d import *
import stage1
import stage2
from boy import Boy

class GameWorld:
    def __init__(self):
        self.current_stage = None
        self.running = True
        self.last_stage = 1
        self.boy = Boy()

    def change_stage(self, stage_number):
        if stage_number == 1:
            self.current_stage = stage1.Stage1(self.change_stage, self.boy)
            self.last_stage = 1
        elif stage_number == 2:
            self.current_stage = stage2.Stage2(self.change_stage, self.boy)
            self.last_stage = 2

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
    game_world.change_stage(1)

    while game_world.running:
        game_world.handle_events()
        game_world.update()
        game_world.draw()
        delay(0.01)

    close_canvas()

if __name__ == '__main__':
    main()