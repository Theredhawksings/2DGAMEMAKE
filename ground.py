from pico2d import load_image

class Ground:
    def __init__(self, current_stage=1):
        self.image1 = load_image('ground1.png')
        self.image2 = load_image('ground2.png')
        self.current_stage = current_stage

    def update_stage(self, stage):
        self.current_stage = stage

    def draw(self,x,y):
        if self.current_stage == 3:
           pass
        else:
            self.image1.draw(x,y)

    def fallingdraw(self,x,y,background_y):
        if self.current_stage == 3:
            self.image2.clip_draw(0, background_y, 1024, 768, x, y, 1024, 768)