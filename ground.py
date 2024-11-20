from pico2d import load_image
import os

class Ground:
    images = {}

    @classmethod
    def load_images(cls):
        image_files = {
            1: 'ground1.png',
            2: 'ground2.png',
            3: 'ground3.png',
            4: 'ground4.png',
            5: 'ground5.png'
        }

        for key, filename in image_files.items():
            if key not in cls.images:
                cls.images[key] = load_image(os.path.join('Ground', filename))

    def __init__(self, current_stage=1):
        Ground.load_images()
        self.current_stage = current_stage

    def update_stage(self, stage):
        self.current_stage = stage

    def draw(self, x, y):
        if self.current_stage in [1, 2, 3]:
            Ground.images[1].draw(x, y)
        elif self.current_stage in [4, 5, 6]:
            Ground.images[3].draw(x, y)
        elif self.current_stage in [7]:
            Ground.images[4].draw(x, y)
        elif self.current_stage in [8]:
            Ground.images[5].draw(x, y)

    def falling_draw(self, x, y, background_y):
        if self.current_stage == 3:
            Ground.images[2].clip_draw(0, background_y, 1024, 768, x, y, 1024, 768)
