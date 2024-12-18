from pico2d import *
from grass import Grass
from ground import Ground
from obstacle import Obstacle
import collision_utils
import time
from font import Font

class Stage4:
   def __init__(self, stage_change_call, boy):
       self.boy = boy
       self.boy.stage = self

       self.ground = Ground(current_stage=4)
       self.stage_change_call = stage_change_call
       self.font = Font(30)

       grass_positions = [
           (0, 0, 128),
           (130, 60, 30),
           (250, 100, 30),
           (350, 150, 40),
           (430, 220, 30),
           (520, 300, 45),
           (630, 350, 50),
           (710, 430, 30),
           (630, 510, 30),
           (440, 510, 100),
           (290, 550, 30),
           (180, 550, 50),
           (150, 610, 20),
           (150, 670, 20),
           (480, 670, 300),
           (1000, 670, 200),
       ]

       self.grass = Grass(grass_positions, current_stage=4)

       static_obstacle_data = [
           (220, 400, 0, 0, 0),
           (245, 400, 0, 0, 0),
           (270, 400, 0, 0, 0),
           (295, 400, 0, 0, 0),
           (320, 400, 0, 0, 0),
           (890, 580, 0, 0, 0),
           (865, 580, 0, 0, 0),
           (840, 580, 0, 0, 0),
           (815, 580, 0, 0, 0),
           (665, 385, 0, 0, 0),
           (445, 550, 0, 0, 0),
           (445, 400, 0, 0, 0),
           (445, 430, 0, 0, 0),
           (575, 515, 0, 0, 0),
           (785, 480, 1, 0, 0),
       ]

       self.obstacle = Obstacle(static_obstacle_data)
       self.initial_obstacles = self.obstacle.obstacles.copy()

       self.obstacle_definitions = [
           {'trigger': {'x_min': 110, 'x_max': 130, 'y_min': None, 'y_max': None},
            'obstacle': {'x': 160, 'y': -15, 'image_direction': 0, 'move_direction': 4, 'move_speed': 15}},
           {'trigger': {'x_min': 330, 'x_max': 350, 'y_min': 190, 'y_max': None},
            'obstacle': {'x': -30, 'y': 220, 'image_direction': 3, 'move_direction': 1, 'move_speed': 20}},
           {'trigger': {'x_min': 490, 'x_max': 510, 'y_min': None, 'y_max': None},
            'obstacle': {'x': 530, 'y': 0, 'image_direction': 0, 'move_direction': 4, 'move_speed': 30}},
           {'trigger': {'x_min': 560, 'x_max': 590, 'y_min': None, 'y_max': None},
            'obstacle': {'x': 580, 'y': -15, 'image_direction': 0, 'move_direction': 4, 'move_speed': 30}},
           {'trigger': {'x_min': 610, 'x_max': 640, 'y_min': None, 'y_max': None},
            'obstacle': {'x': 630, 'y': 730, 'image_direction': 2, 'move_direction': 3, 'move_speed': 20}},
           {'trigger': {'x_min': 610, 'x_max': 630, 'y_min': 500, 'y_max': None},
            'obstacle': {'x': -10, 'y': 565, 'image_direction': 3, 'move_direction': 1, 'move_speed': 10}},
           {'trigger': {'x_min': 300, 'x_max': 320, 'y_min': 600, 'y_max': None},
            'obstacle': {'x': 1030, 'y': 580, 'image_direction': 1, 'move_direction': 2, 'move_speed': 30}},
           {'trigger': {'x_min': 180, 'x_max': 800, 'y_min': 720, 'y_max': None},
            'obstacle': {'x': 20, 'y': 740, 'image_direction': 3, 'move_direction': 1, 'move_speed': 5}}
       ]

       self.time = time.time()
       self.boy.update_stage_info(4)

       self.obstacle_created = [False] * len(self.obstacle_definitions)
       collision_utils.add_collision_pair('boy:obstacle', self.boy, self.obstacle)

       self.boy.savepointX = 10
       self.boy.savepointY = 50

       collision_utils.handle_collisions()

       self.bullets = []


   def handle_event(self, event):
       self.boy.handle_event(event)

   def check_and_create_obstacles(self):
       for i, definition in enumerate(self.obstacle_definitions):
           if self.obstacle_created[i]:
               continue

           trigger = definition['trigger']
           x_condition = (self.boy.x >= trigger['x_min'] and self.boy.x < trigger['x_max'])

           y_condition = True

           if trigger['y_min'] is not None:
               y_condition = self.boy.y >= trigger['y_min']
           if trigger['y_max'] is not None:
               y_condition = y_condition and self.boy.y < trigger['y_max']

           if x_condition and y_condition:
               self.obstacle.obstacles.append(definition['obstacle'].copy())
               self.obstacle_created[i] = True

   def update(self):
       self.boy.update(self.grass)
       self.obstacle.update()

       if self.boy.x < 1 and self.boy.y == 45:
           self.boy.previous_stage = 4
           self.boy.current_stage = 3
           self.boy.x = 1020
           self.boy.y = 50
           self.stage_change_call(3)
           return

       if self.boy.x >= 1024 and self.boy.y == 715:
           self.stage_change_call(5)
           self.boy.x = 5
           self.boy.y = 730

       self.check_and_create_obstacles()

       collision_utils.handle_collisions()

       if self.boy.y < -10:
           self.boy.x = self.boy.savepointX
           self.boy.y = self.boy.savepointY
           self.obstacle_created = [False] * len(self.obstacle_definitions)

       for bullet in self.bullets:
           bullet.update()

   def draw(self):
       self.ground.draw(512, 384)

       self.grass.draw()
       self.boy.draw()
       self.obstacle.draw()
       self.font.draw(100, 300, "날아오는 장애물들을 피하세요", (255, 255, 255))

       for bullet in self.bullets:
           bullet.draw()