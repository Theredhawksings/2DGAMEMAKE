from pico2d import load_image
import os

class Ground:
    image1 = None
    image2 = None
    image3 = None

    def __init__(self, current_stage=1):
        if Ground.image1 is None:
            Ground.image1 = load_image(os.path.join('Ground', 'ground1.png'))
        if Ground.image2 is None:
            Ground.image2 = load_image(os.path.join('Ground', 'ground2.png'))
        if Ground.image3 is None:
            Ground.image3 = load_image(os.path.join('Ground', 'ground3.png'))

        self.current_stage = current_stage

    def update_stage(self, stage):
        self.current_stage = stage

    def draw(self,x,y):
        if self.current_stage >= 4:
           Ground.image3.draw(x,y)
        else:
            Ground.image1.draw(x,y)

    def fallingdraw(self,x,y,background_y):
        if self.current_stage == 3:
            Ground.image2.clip_draw(0, background_y, 1024, 768, x, y, 1024, 768)