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

    def draw(self):
        for x, y, width in self.positions:
            if self.current_stage == 3:
                Grass.image2.clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)
            else:
                Grass.image1.clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)

    def get_positions(self):
        return self.positions