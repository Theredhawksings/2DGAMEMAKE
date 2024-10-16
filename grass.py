from pico2d import load_image

class Grass:
    def __init__(self, positions):
        self.image = load_image('Grass.png')
        self.positions = positions
        self.width = 800
        self.height = 50

    def draw(self):
        for x, y in self.positions:
            self.image.draw(x, y)

    def get_positions(self):
        return self.positions