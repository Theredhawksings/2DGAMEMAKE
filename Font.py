from pico2d import load_font


class Font:
    def __init__(self, font_name, size):
        self.font = load_font(font_name, size)

    def draw(self, x, y, text, color=(255, 255, 255)):
        self.font.draw(x, y, text, color)