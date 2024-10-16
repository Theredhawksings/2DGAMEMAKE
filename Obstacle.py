from pico2d import load_image
import math

class Ground:
    def __init__(self):
        self.image = load_image('obstacle.png')
        self.angles = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]  # 예시 각도 배열

    def draw(self, x, y, angle_index):
        angle = self.angles[angle_index]
        self.image.clip_composite_draw(0, 0, 100, 120,
                                       angle,
                                       '',  # 뒤집기 옵션 (빈 문자열 = 뒤집지 않음)
                                       x, y,
                                       50, 60)