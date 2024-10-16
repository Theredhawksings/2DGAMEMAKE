from pico2d import load_image
import math

class Obstacle:
    def __init__(self, obstacle_data):
        self.image = load_image('obstacle.png')
        self.obstacles = obstacle_data
        self.angles = [0, math.pi/2, math.pi, 3*math.pi/2]

    def draw(self):
        for x, y, angle_index in self.obstacles:
            angle = self.angles[angle_index]
            self.image.clip_composite_draw(0, 0, 100, 120,
                                           angle,
                                           '',
                                           x, y,
                                           25, 30)