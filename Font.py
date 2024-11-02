import os
from pico2d import load_font


class Font:
    def __init__(self, size=30):
        self.font = load_font(os.path.join('font', '경기천년제목_Bold.ttf'), size)

    def draw(self, x, y, text, color=(255, 255, 255)):
        self.font.draw(x, y, text, color)