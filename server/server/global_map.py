import numpy as np
import global_map_chank
import game_config
import random


class GlobalMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.global_map = np.zeros((self.height, self.width), dtype=np.uint8)

    def change_map_chank(self, x_coord, y_coord, new_id):
        self.global_map[y_coord, x_coord] = new_id

    def randomize_chanks(self):
        for i in range(game_config.Config.gl_map_height):
            for j in range(game_config.Config.gl_map_width):
                self.global_map[i, j] = random.randrange(0, 256, 1)

    def generate_map(self):
        pass
