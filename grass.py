from pico2d import load_image

class Grass:
    image1 = None
    image2 = None

    def __init__(self, positions, current_stage=1):
        if Grass.image1 is None:
            Grass.image1 = load_image('Grass.png')
        if Grass.image2 is None:
            Grass.image2 = load_image('Grass2.png')

        self.current_stage = current_stage
        self.positions = positions
        self.width = 800
        self.height = 50

    def draw(self):
        for x, y in self.positions:
            if self.current_stage == 3:
                Grass.image2.draw(x, y)
            else:
                Grass.image1.draw(x, y)

    def get_positions(self):
        return self.positions
