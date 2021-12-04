import numpy as np

from .db_map import DBMap
from . import game_config
from . import object_wrapper
from . import castle
from . import hero
from . import object_pathlike
from . import unit_dictionary
import random


class GlobalMap:
    def __init__(self, config: game_config.Config, db_map : DBMap):
        self.config = config
        self.global_map_first = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)          # biomes
        self.global_map_second = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)         # terrain like mountains roads
        self.global_map_objects = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)        # barraks, castles, etc.
        self.global_map_armies = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)         # heroes and items
        self.global_map_passable = np.full((config.gl_map_height, config.gl_map_width), True, dtype=np.bool_)

        self.global_fog_map = np.zeros((config.player_amount, config.gl_map_height, config.gl_map_width), dtype=np.uint8)

        self.global_map_object_backcall = np.full((2, config.gl_map_height, config.gl_map_width), None, dtype=np.object_)       # [0] castle; [1] player
        self.players_castle_hero = self.create_players_castle_hero()                                                # list of objects that belong to players: neutral[0]; player1[1]...
        self.global_map_object_items = np.full((config.gl_map_height, config.gl_map_width), None, dtype=np.object_)             # items

        self.unit_dict = unit_dictionary.UnitDictionary()

    def create_players_castle_hero(self) -> list:
        castles_heroes = []
        for i in range(self.config.player_amount+1):
            castle_type = "rampart"
            default_castle = castle.Castle(self.unit_dict, castle_type)
            default_hero = hero.Hero(player_id=i)
            temp_castle_coord = [10*i, 10*i]
            temp_hero_coord = [10*i, 10*i]
            object_castle_hero = object_wrapper.ObjectWrapper(default_castle, temp_castle_coord, default_hero, temp_hero_coord)
            castles_heroes.append(object_castle_hero)
            object_path_castle = object_pathlike.ObjectPathlike(i, "castle", 0)
            self.global_map_object_backcall[self.coord_parse(0, temp_castle_coord)] = object_path_castle
            object_path_hero = object_pathlike.ObjectPathlike(i, "hero", 0)
            self.global_map_object_backcall[self.coord_parse(1, temp_hero_coord)] = object_path_hero

        return castles_heroes

    def move_hero(self, player_id, hero_id, direction):
        pass

    def start_of_week(self):
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
    def coord_parse(layer, coords):
        return layer, coords[0], coords[1]

    @staticmethod
    def get_passable(chunk_id) -> bool:
        pass

    def randomize_chunks(self):
        for i in range(self.config.gl_map_height):
            for j in range(self.config.gl_map_width):
                self.global_map[i, j] = random.randrange(0, 256, 1)

    def generate_map(self):
        pass
