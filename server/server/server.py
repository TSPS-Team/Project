#!/usr/bin/env python3
from .db_map import *
from .renderer import TilesetRenderer
from PIL import Image
import numpy as np

class Interface:
    def __init__(self, server):
        self.server = server

    def move(self, player_id, direction):
        self.server.move(player_id, direction)

    def end_move(self, player_id):
        self.server.end_move(player_id)

    def get_view(self, player_id) -> Image.Image:
        return self.server.get_view(player_id)

class Server:
    def __init__(self, m : DBMap):
        self.game_map = self._load_map(m)

        #NOTE Just for prototype
        self.player_pos = (20, 20)
        self.renderer = TilesetRenderer(self.game_map.tilesets[0])

    def _load_map(self, m : DBMap):
        #NOTE Just for prototype
        return m

    def get_interface(self) -> Interface:
        return Interface(self)

    def get_view(self, player_id):
        #NOTE Just for prototype
        layers = []
        for layer in self.game_map._json["layers"]:
            if "data" in layer:
                layers.append([x - 1 if x != 0 else 0 for x in layer["data"]])

        view = self.renderer.draw(layers, self.game_map._json["width"],
                                  self.game_map._json["height"])

        view.paste(self.game_map.entities_tileset.get(13),
                   (self.player_pos[0] * 16, self.player_pos[1] * 16),
                   self.game_map.entities_tileset.get(13)
                   )

        for layer in self.game_map._json["layers"]:
            if "objects" in layer:
                for obj in layer["objects"]:
                    view.paste(self.game_map.tilesets[0].get(obj["gid"] - 1),
                               (obj["x"], obj["y"] - self.game_map.tilesets[0].tileheight),
                               self.game_map.tilesets[0].get(obj["gid"] - 1))

        return view

    def move(self, player_id, direction):
        #NOTE Just for prototype
        self.player_pos = (self.player_pos[0] + direction[0],
                           self.player_pos[1] + direction[1])
