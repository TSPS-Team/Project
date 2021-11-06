import numpy as np
from . import game_config
import random


class GlobalMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.global_map_first = np.zeros((self.height, self.width), dtype=np.uint16)        # biomes
        self.global_map_second = np.zeros((self.height, self.width), dtype=np.uint16)       # terrain like mountains roads
        self.global_map_objects = np.zeros((self.height, self.width), dtype=np.uint16)      # barraks, castles, etc.
        self.global_map_armies = np.zeros((self.height, self.width), dtype=np.uint16)       # heroes and items
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

    def update_passable(self):
        for i in range(game_config.Config.gl_map_height):
            for j in range(game_config.Config.gl_map_width):
                if (self.get_passable(self.global_map_first[i, j])) and (self.get_passable(self.global_map_second[i, j])) and (self.get_passable(self.global_map_objects[i, j])) and (self.get_passable(self.global_map_armies[i, j])):
                    self.global_map_passable[i, j] = True
                else:
                    self.global_map_passable[i, j] = False

    @staticmethod
    def get_passable(id):
        pass

    def randomize_chanks(self):
        for i in range(game_config.Config.gl_map_height):
            for j in range(game_config.Config.gl_map_width):
                self.global_map[i, j] = random.randrange(0, 256, 1)

    def generate_map(self):
        pass
