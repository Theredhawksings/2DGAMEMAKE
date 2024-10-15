from pico2d import load_image


class Ground:
    def __init__(self):
        self.image1 = load_image('Ground1.png')

    def draw(self):
        self.image1.draw(400,300)
