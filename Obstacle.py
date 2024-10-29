from pico2d import load_image
import math, os

class Obstacle:
    def __init__(self, obstacle_data):
        self.image = load_image(os.path.join('obstacle', 'obstacle.png'))
        self.obstacles = []
        self.angles = [0, math.pi/2, math.pi, 3*math.pi/2]
        self.screen_width = 1024
        self.screen_height = 768

        for x, y, image_direction, move_direction, move_speed in obstacle_data:
            self.obstacles.append({
                'x': x,
                'y': y,
                'image_direction': image_direction,
                'move_direction': move_direction,
                'move_speed': move_speed
            })



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
        for obstacle in self.obstacles:

            if obstacle['move_direction'] == 1:
                obstacle['x']+=obstacle['move_speed']

            elif obstacle['move_direction'] == 2:
                obstacle['x']-=obstacle['move_speed']

            elif obstacle['move_direction'] == 3:
                obstacle['y'] -= obstacle['move_speed']

            elif obstacle['move_direction'] == 4:
                obstacle['y'] += obstacle['move_speed']

            if (obstacle['x'] < -30 or obstacle['x'] > 1054 or
                    obstacle['y'] < -30 or obstacle['y'] > 798):
                self.obstacles.remove(obstacle)
