import numpy as np
from . import game_config
import random


class GlobalMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.global_map_first = np.zeros((self.height, self.width), dtype=np.uint16)
        self.global_map_second = np.zeros((self.height, self.width), dtype=np.uint16)
        self.global_map_objects = np.zeros((self.height, self.width), dtype=np.uint16)
        self.global_map_armies = np.zeros((self.height, self.width), dtype=np.uint16)
        self.global_map_passable = np.zeros((self.height, self.width), dtype=np.bool_)

    def change_map_chank(self, x_coord, y_coord, layer, new_id):
        if layer == 0:
            self.global_map_first[y_coord, x_coord] = new_id
        elif layer == 1:
            self.global_map_second[y_coord, x_coord] = new_id
        elif layer == 2:
            self.global_map_objects[y_coord, x_coord] = new_id
        else:
            self.global_map_armies[y_coord, x_coord] = new_id

    def randomize_chanks(self):
        for i in range(game_config.Config.gl_map_height):
            for j in range(game_config.Config.gl_map_width):
                self.global_map[i, j] = random.randrange(0, 256, 1)

    def generate_map(self):
        pass
