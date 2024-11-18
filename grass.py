from pico2d import load_image, draw_rectangle
import os

class Grass:
    images = {}

    @classmethod
    def load_images(cls):
        image_files = {
            1: 'Grass.png',
            2: 'Grass2.png',
            3: 'Grass3-3.png',
            4: 'Grass4.png'
        }

        for key, filename in image_files.items():
            if key not in cls.images:
                cls.images[key] = load_image(os.path.join('Grass', filename))

    def __init__(self, positions, current_stage=1):
        Grass.load_images()
        self.current_stage = current_stage
        self.positions = positions

    def draw(self):
        for x, y, width in self.positions:
            if self.current_stage == 7:
                Grass.images[4].clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)
            elif 4 <= self.current_stage <= 6:
                Grass.images[3].clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)
            elif self.current_stage == 3:
                Grass.images[2].clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)
            else:
                Grass.images[1].clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)

        # 충돌 박스 그리기
        for bb in self.get_bb():
            draw_rectangle(*bb)

    def get_positions(self):
        return self.positions

    def get_bb(self):
        bounding_boxes = []
        for x, y, width in self.positions:
            bounding_boxes.append((x - width, y - 30, x + width, y + 60))
        return bounding_boxes
