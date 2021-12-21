#!/usr/bin/env python3
from __future__ import annotations
from .states import GlobalState, ServerState
from .db_map import *
from .renderer import TilesetRenderer
from .game_instance import *
from PIL import Image
import numpy as np

class Interface:
    def __init__(self, server : Server):
        self.server = server

    def begin(self):
        return self.server.begin()

    def get_teams(self) -> set[int]:
        return self.server.get_teams();

    def move(self, player_id, direction):
        self.server.move(player_id, direction)

    def end_move(self, player_id):
        self.server.end_move(player_id)

    def get_image(self, position, player_id) -> Image.Image:
        return self.server.get_image(position, player_id)

class Server:
    def __init__(self, m: DBMap, unit_data):
        self.game_map = self._load_map(m)
        self.state = ServerState(GlobalState.Uninitialized)

        self.renderer = TilesetRenderer(self.game_map.json["tilesets"], self.game_map.json["width"]
                                        , self.game_map.json["height"])
        self._game_instance = GameInstance(m)


        # Prepare template image
        layers = []
        for layer in self.game_map.json["layers"]:
            if "data" in layer:
                layers.append([x if x != 0 else 0 for x in layer["data"]])

        self.renderer.template = self.renderer.draw(layers)


    def begin(self):
        self.state = self._game_instance.next_day()

    def _load_map(self, m : DBMap):
        #NOTE Just for prototype
        return m

    def get_teams(self) -> set[int]:
        return self._game_instance._config.playable_teams

    def get_interface(self) -> Interface:
        return Interface(self)

    def get_image(self, position, player_id):
        #NOTE Just for prototype

        base = self.renderer.template.copy()

        bbox = (position[0] - 9, position[1] - 9,
                position[0] + 10, position[1] + 10)

        tilewidth = self.renderer.tilesets[0].tilewidth
        tileheight = self.renderer.tilesets[0].tileheight

        def is_in_fog(x, y):
            coord = self._game_instance._global_map.board_coord((x, y))
            return not self._game_instance._global_map.global_map_fog[player_id, coord[1], coord[0]]

        for x in range(bbox[0], bbox[2]):
            for y in range(bbox[1], bbox[3]):
                if is_in_fog(x, y):
                    self.renderer.apply_image(base, x, y, self.renderer.fog)

        gid_dic = {
            "rampart": 339,
            "castle": 337,
            "hero": 13 + 625
        }

        colors = {
            0: (255, 255, 255, 200),
            1: (0, 255, 255, 155),
            2: (255, 0, 255, 155),
            3: (255, 255, 0, 155),
            4: (0, 255, 0, 155)
        }

        for layer in range(2):
            for x in range(bbox[0], bbox[2]):
                for y in range(bbox[1], bbox[3]):
                    if not is_in_fog(x, y):
                        backcall = self._game_instance._global_map.global_map_object_backcall[layer, y, x]
                        if backcall is not None:
                            self.renderer.put(base, x, y,
                                              gid_dic[backcall.object_type],
                                              colors[backcall.team])


        base = base.crop((bbox[0] * tilewidth, bbox[1] * tileheight,
                          bbox[2] * tilewidth, bbox[3] * tileheight))

        maxsize = (1028, 1028)
        base = base.resize(maxsize, Image.NEAREST)

        return base

    def move(self, player_id, direction):
        #NOTE Just for prototype
        self.player_pos = (self.player_pos[0] + direction[0],
                           self.player_pos[1] + direction[1])
