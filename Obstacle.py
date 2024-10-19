from pico2d import load_image
import math

class Obstacle:
    def __init__(self, obstacle_data):
        self.image = load_image('obstacle.png')
        self.obstacles = []
        self.angles = [0, math.pi/2, math.pi, 3*math.pi/2]
        self.screen_width = 1024
        self.screen_height = 768

        for x, y, image_direction, move_direction, move_speed in obstacle_data:
            self.obstacles.append({x, y, image_direction, move_direction, move_speed})



    def draw(self):
        for obstacle in self.obstacles:
            angle = self.angles[obstacle['image_direction']]
            self.image.clip_composite_draw(0, 0, 100, 120,
                                           angle,
                                           '',
                                           obstacle['x'],
                                           obstacle['y'],
                                           25, 30)

    def update(self):
        pass