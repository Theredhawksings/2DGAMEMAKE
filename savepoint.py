from pico2d import load_image
import os

class SavePoint:
    images = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        if not SavePoint.images:
            SavePoint.images.append(load_image(os.path.join('savepoint', 'activate.png')))
            SavePoint.images.append(load_image(os.path.join('savepoint', 'deactivate.png')))
        self.is_activated = False

    def draw(self):
        if self.is_activated:
            SavePoint.images[0].clip_draw(0, 0, 60, 60, self.x, self.y, 30, 30)
        else:
            SavePoint.images[1].clip_draw(0, 0, 60, 60, self.x, self.y, 30, 30)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def handle_collision(self, group, other):
        if group == 'bullet:savepoint':
            self.is_activated = True