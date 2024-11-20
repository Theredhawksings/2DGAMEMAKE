from pico2d import load_image, draw_rectangle
import math, os
import boss
PIXEL_PER_METER = (10.0 / 0.3)
OBSTACLE_SPEED_KMPH = 0.108
OBSTACLE_SPEED_MPM = OBSTACLE_SPEED_KMPH * 1000.0 / 60.0
OBSTACLE_SPEED_MPS = OBSTACLE_SPEED_MPM / 60.0
OBSTACLE_SPEED_PPS = OBSTACLE_SPEED_MPS * PIXEL_PER_METER


class Obstacle:
    death_count = 0

    def __init__(self, obstacle_data):
        self.image = load_image(os.path.join('obstacle', 'obstacle.png'))
        self.obstacles = []
        self.angles = [0, math.pi / 2, math.pi, 3 * math.pi / 2]

        for x, y, image_direction, move_direction, move_speed in obstacle_data:
            self.obstacles.append({
                'x': x,
                'y': y,
                'image_direction': image_direction,
                'move_direction': move_direction,
                'move_speed': OBSTACLE_SPEED_PPS * move_speed
            })

    def get_bb(self):
        bbs = []
        for obstacle in self.obstacles:
            if obstacle['image_direction'] == 0 or obstacle['image_direction'] == 2:
                bb = (obstacle['x'] - 9,
                      obstacle['y'] - 13,
                      obstacle['x'] + 8,
                      obstacle['y'] + 8)
            else:
                bb = (obstacle['x'] - 15,
                      obstacle['y'] - 15,
                      obstacle['x'] + 15,
                      obstacle['y'] + 15)
            bbs.append(bb)
        return bbs

    def draw(self):
        for obstacle, bb in zip(self.obstacles, self.get_bb()):
            angle = self.angles[obstacle['image_direction']]
            self.image.clip_composite_draw(0, 0, 100, 120,
                                           angle,
                                           '',
                                           obstacle['x'],
                                           obstacle['y'],
                                           25, 30)
            draw_rectangle(*bb)

    def update(self):
        obstacles_to_remove = []
        for obstacle in self.obstacles:
            if obstacle['move_direction'] == 1:
                obstacle['x'] += obstacle['move_speed']
            elif obstacle['move_direction'] == 2:
                obstacle['x'] -= obstacle['move_speed']
            elif obstacle['move_direction'] == 3:
                obstacle['y'] -= obstacle['move_speed']
            elif obstacle['move_direction'] == 4:
                obstacle['y'] += obstacle['move_speed']

            if (obstacle['x'] < -30 or obstacle['x'] > 1054 or
                    obstacle['y'] < -30 or obstacle['y'] > 798):
                obstacles_to_remove.append(obstacle)

        for obstacle in obstacles_to_remove:
            if obstacle in self.obstacles:
                self.obstacles.remove(obstacle)

    def handle_collision(self, group, other):
        if group == 'boy:obstacle':
            Obstacle.death_count += 1

    @staticmethod
    def get_death_count():
        return Obstacle.death_count

class BossObstacle:
    def __init__(self, obstacle_data):
        self.image = load_image(os.path.join('obstacle', 'boss_obstacle.png'))
        self.obstacles = []
        self.boss = None

        for x, y, move_speed in obstacle_data:
            self.obstacles.append({
                'x': x,
                'y': y,
                'move_speed': OBSTACLE_SPEED_PPS * move_speed
            })


    def get_bb(self):
        bbs = []
        for obstacle in self.obstacles:
            bb = (obstacle['x'] - 13,
                  obstacle['y'] - 15,
                  obstacle['x'] + 13,
                  obstacle['y'] + 15)
            bbs.append(bb)
        return bbs

    def draw(self):
        for obstacle, bb in zip(self.obstacles, self.get_bb()):
            self.image.clip_composite_draw(0, 0, 300, 360,
                                           0,
                                           '',
                                           obstacle['x'],
                                           obstacle['y'],
                                           30, 36)
            draw_rectangle(*bb)

    def update(self):
        if self.boss.dead:
            self.obstacles.clear()
            return

        obstacles_to_remove = []
        for obstacle in self.obstacles:
            velocity = OBSTACLE_SPEED_PPS * obstacle['move_speed']
            obstacle['y'] -= velocity

            if obstacle['y'] < -15:
                obstacles_to_remove.append(obstacle)

        for obstacle in obstacles_to_remove:
            if obstacle in self.obstacles:
                self.obstacles.remove(obstacle)

    def handle_collision(self, group, other):
        if group == 'boy:boss_obstacle':
            Obstacle.death_count += 1

class BossBomb:
    def __init__(self, obstacle_data):
        self.image = load_image(os.path.join('obstacle', 'boss_bomb.png'))
        self.bomb = []
        self.boss = None

        for x, y, move_speed in obstacle_data:
            self.bomb.append({
                'x': x,
                'y': y,
                'move_speed': move_speed
            })

    def get_bb(self):
        bbs = []
        for bombs in self.bomb:
            bb = (bombs['x'] - 13,
                  bombs['y'] - 15,
                  bombs['x'] + 13,
                  bombs['y'] + 15)
            bbs.append(bb)
        return bbs

    def draw(self):
        for bombs, bb in zip(self.bomb, self.get_bb()):
            self.image.clip_composite_draw(0, 0, 200, 150,
                                           0,
                                           '',
                                           bombs['x'],
                                           bombs['y'],
                                           100, 75)
            draw_rectangle(*bb)

    def update(self):
        if self.boss.dead:
            self.bomb.clear()
            return

        bomb_to_remove = []

        for bombs in self.bomb:
            dx = OBSTACLE_SPEED_PPS * 15
            bombs['x'] -= dx

            if bombs['x'] < -15:
                bomb_to_remove.append(bombs)

        for bomb in bomb_to_remove:
            if bomb in self.bomb:
                self.bomb.remove(bomb)

        def handle_collision(self, group, other):
            if group == 'boy:boss_obstacle':
                Obstacle.death_count += 1