from pico2d import load_image

class Grass:
    def __init__(self, positions, current_stage=1):
        self.image1 = load_image('Grass.png')
        self.image2 = load_image('Grass2.png')
        self.current_stage = current_stage
        self.positions = positions
        self.width = 800
        self.height = 50

    def draw(self):
        for x, y in self.positions:
            if self.current_stage == 3:
                self.image2.draw(x, y)
            else:
                self.image1.draw(x, y)

    def get_positions(self):
        return self.positions