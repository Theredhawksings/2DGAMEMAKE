from pico2d import load_image

class Gameover:
    image1 = None

    def __init__(self):
        Gameover.image1 = load_image('gameover.png')

    def draw(self):
        Gameover.image1.draw(177, 284)
