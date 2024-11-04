from pico2d import load_image
import os

class Grass:
   image1 = None
   image2 = None
   image3 = None

   def __init__(self, positions, current_stage=1):
       if Grass.image1 is None:
           Grass.image1 = load_image(os.path.join('Grass', 'Grass.png'))
       if Grass.image2 is None:
           Grass.image2 = load_image(os.path.join('Grass', 'Grass2.png'))
       if Grass.image3 is None:
           Grass.image3 = load_image(os.path.join('Grass', 'Grass3-3.png'))

       self.current_stage = current_stage
       self.positions = positions

   def draw(self):
       for x, y, width in self.positions:
           if self.current_stage == 4 or self.current_stage == 5:
               Grass.image3.clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)
           elif self.current_stage == 3:
               Grass.image2.clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)
           else:
               Grass.image1.clip_draw(0, 0, width * 2, 60, x, y, width * 2, 60)

   def get_positions(self):
       return self.positions