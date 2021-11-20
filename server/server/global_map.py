import numpy as np
from . import game_config
from . import object_wrapper
from . import castle
import random


class GlobalMap:
    def __init__(self, config: game_config.Config):
        self.config = config
        self.global_map_first = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)        # biomes
        self.global_map_second = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)       # terrain like mountains roads
        self.global_map_objects = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)      # barraks, castles, etc.
        self.global_map_armies = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)       # heroes and items
        self.global_map_passable = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.bool_)

        self.global_fog_map = np.zeros((config.player_amount, config.gl_map_height, config.gl_map_width), dtype=np.uint8)

        self.castle_hero = self.create_castle_hero()

    def create_castle_hero(self) -> list:
        castles_heroes = []
        for i in range(self.config.player_amount+1):
            pass

    def change_map_chunk(self, x_coord: int, y_coord: int, layer: int, new_id: int):
        if layer == 0:
            self.global_map_first[y_coord, x_coord] = new_id
        elif layer == 1:
            self.global_map_second[y_coord, x_coord] = new_id
        elif layer == 2:
            self.global_map_objects[y_coord, x_coord] = new_id
        else:
            self.global_map_armies[y_coord, x_coord] = new_id

    def update_passable(self):
        for i in range(self.config.gl_map_height):
            for j in range(self.config.gl_map_width):
                if (self.get_passable(self.global_map_first[i, j])) and (self.get_passable(self.global_map_second[i, j])) and \
                        (self.get_passable(self.global_map_objects[i, j])) and (self.get_passable(self.global_map_armies[i, j])):
                    self.global_map_passable[i, j] = True
                else:
                    self.global_map_passable[i, j] = False

    @staticmethod
    def get_passable(chunk_id) -> bool:
        pass

    def randomize_chunks(self):
        for i in range(self.config.gl_map_height):
            for j in range(self.config.gl_map_width):
                self.global_map[i, j] = random.randrange(0, 256, 1)

    def generate_map(self):
        pass
