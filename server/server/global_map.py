import numpy as np
import math

from .db_map import DBMap
from . import game_config
from . import object_wrapper
from . import castle
from . import hero
from . import object_pathlike
from . import unit_dictionary
import random


class GlobalMap:
    def __init__(self, config: game_config.Config, db_map : DBMap, unit_dict=None ):
        self.config = config
        self.global_map_first = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)          # biomes
        self.global_map_second = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)         # terrain like mountains roads
        self.global_map_objects = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)        # barraks, castles, etc.
        self.global_map_armies = np.zeros((config.gl_map_height, config.gl_map_width), dtype=np.uint16)         # heroes and items
        self.global_map_passable = np.full((config.gl_map_height, config.gl_map_width), True, dtype=np.bool_)

        self.global_map_fog = np.full((config.player_amount + 1, config.gl_map_height, config.gl_map_width), False, dtype=np.bool_)

        if unit_dict is None:
            self.unit_dict = unit_dictionary.UnitDictionary().stat_dictionary
        else:
            self.unit_dict = unit_dict

        self.global_map_object_backcall = np.full((2, config.gl_map_height, config.gl_map_width), None, dtype=np.object_)       # [0] castle; [1] hero
        self.players_castle_hero = self.create_players_castle_hero()                                                # list of objects that belong to players: neutral[0]; player1[1]...
        self.global_map_object_items = np.full((config.gl_map_height, config.gl_map_width), None, dtype=np.object_)             # items


    def create_players_castle_hero(self) -> list:
        castles_heroes = []
        for player_id in range(self.config.player_amount+1):
            castle_type = "rampart"
            default_castle = castle.Castle(self.unit_dict, castle_type)
            default_hero = hero.Hero(player_id=player_id)
            temp_castle_coord = (10*player_id, 10*player_id)
            temp_hero_coord = (10*player_id, 10*player_id+1)
            self.update_global_map_fog(temp_hero_coord, player_id)
            object_castle_hero = object_wrapper.ObjectWrapper(default_castle, temp_castle_coord, default_hero, temp_hero_coord)
            castles_heroes.append(object_castle_hero)
            object_path_castle = object_pathlike.ObjectPathlike(player_id, "castle", 0)
            self.global_map_object_backcall[self.coord_parse(0, temp_castle_coord)] = object_path_castle
            object_path_hero = object_pathlike.ObjectPathlike(player_id, "hero", 0)
            self.global_map_object_backcall[self.coord_parse(1, temp_hero_coord)] = object_path_hero

        return castles_heroes

    def move_hero(self, object_id: tuple, direction: str) -> int:               # object_id[0] - player, object_id[1] - object_type, object_id[2] - object_id
        player = object_id[0]
        object_id_local = object_id[2]
        delta_coord = self.direction_parse(direction)
        current_coord = self.players_castle_hero[player].heroes_coord[object_id_local]
        if self.global_map_passable[current_coord[1]+delta_coord[1],current_coord[0]+delta_coord[0]] and self.players_castle_hero[player].heroes[object_id_local].able_to_move():
            self.global_map_armies[current_coord[1]+delta_coord[1], current_coord[0]+delta_coord[0]] = self.global_map_armies[current_coord[1], current_coord[0]]
            self.global_map_armies[current_coord[1], current_coord[0]] = 0
            self.global_map_object_backcall[1, current_coord[1]+delta_coord[1], current_coord[0]+delta_coord[0]] = self.global_map_object_backcall[1, current_coord[1], current_coord[0]]
            self.global_map_object_backcall[1, current_coord[1], current_coord[0]] = None
            self.players_castle_hero[player].heroes_coord[object_id_local] = (current_coord[0]+delta_coord[0], current_coord[1]+delta_coord[1])

            self.global_map_passable[current_coord[1], current_coord[0]] = True
            self.global_map_passable[current_coord[1]+delta_coord[1], current_coord[0]+delta_coord[0]] = False
            self.update_global_map_fog((current_coord[0]+delta_coord[0], current_coord[1]+delta_coord[1]), player)

            self.players_castle_hero[player].heroes[object_id_local].moving()
            return 0
        return -1

    def start_of_day(self):
        pass

    def start_of_week(self):
        pass

    def check_can_move_simultaneously(self) -> bool:
        pass

    def update_global_map_fog(self, coord: tuple, player_id: int, visibility_radius: int=7):
        for i in range(-visibility_radius, visibility_radius+1):
            for j in range(-visibility_radius, visibility_radius+1):
                if math.floor(math.sqrt(i*i+j*j)) <= visibility_radius:
                    fog_coord = self.board_coord((coord[0]+j, coord[1]+i))
                    self.global_map_fog[player_id, fog_coord[1], fog_coord[0]] = True

    def board_coord(self, coord: tuple) -> tuple:
        x = coord[0]
        y = coord[1]
        if x < 0: x = 0
        if x >= self.config.gl_map_width: x = self.config.gl_map_width-1
        if y < 0: y = 0
        if y >= self.config.gl_map_height: y = self.config.gl_map_height-1
        return x, y

    def update_passable(self):
        for i in range(self.config.gl_map_height):
            for j in range(self.config.gl_map_width):
                if (self.get_passable(self.global_map_first[i, j])) and (self.get_passable(self.global_map_second[i, j])) and \
                        (self.get_passable(self.global_map_objects[i, j])) and (self.get_passable(self.global_map_armies[i, j])):
                    self.global_map_passable[i, j] = True
                else:
                    self.global_map_passable[i, j] = False

    def change_map_chunk(self, x_coord: int, y_coord: int, layer: int, new_id: int):
        if layer == 0:
            self.global_map_first[y_coord, x_coord] = new_id
        elif layer == 1:
            self.global_map_second[y_coord, x_coord] = new_id
        elif layer == 2:
            self.global_map_objects[y_coord, x_coord] = new_id
        else:
            self.global_map_armies[y_coord, x_coord] = new_id

    def get_hero_stamina(self, object_id) -> int:
        return self.players_castle_hero[object_id[0]].heroes[object_id[2]].get_stamina()

    def get_hero_position(self, object_id) -> tuple:
        return self.players_castle_hero[object_id[0]].heroes_coord[object_id[2]]

    @staticmethod
    def direction_parse(direction: str) -> tuple:
        delta_x = 0
        delta_y = 0
        if "u" in direction:
            delta_y = -1
        if "d" in direction:
            delta_y = 1
        if "l" in direction:
            delta_x = -1
        if "r" in direction:
            delta_x = 1
        return delta_x, delta_y

    @staticmethod
    def coord_parse(layer: int, coords: tuple) -> tuple:
        return layer, coords[1], coords[0]

    @staticmethod
    def get_passable(chunk_id) -> bool:
        pass

    def randomize_chunks(self):
        for i in range(self.config.gl_map_height):
            for j in range(self.config.gl_map_width):
                self.global_map[i, j] = random.randrange(0, 256, 1)

    def generate_map(self):
        pass
