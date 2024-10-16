from pico2d import load_image
import math

class Ground:
    def __init__(self):
        self.image = load_image('obstacle.png')
        self.angles = [0, math.pi/4, math.pi/2, 3*math.pi/4, math.pi]  # 예시 각도 배열

    def draw(self, x, y, angle_index):
        angle = self.angles[angle_index]  # 각도 배열에서 선택
        self.image.clip_composite_draw(0, 0, 100, 120,  # 소스 이미지에서 잘라낼 영역 (100x120 고정)
                                       angle,  # 회전 각도 (배열에서 선택)
                                       '',  # 뒤집기 옵션 (빈 문자열 = 뒤집지 않음)
                                       x, y,  # 그릴 위치 (외부에서 받은 값)
                                       50, 60)  # 그려질 크기 (50x60으로 고정)