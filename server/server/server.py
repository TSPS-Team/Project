#!/usr/bin/env python3
from .db_map import *
from PIL import Image

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
    def _load_map(self, m : DBMap):
        pass

    def __init__(self, m : DBMap):
        self.game_map = self._load_map(m)

    def get_interface(self) -> Interface:
        return Interface(self)

    def get_view(self, player_id):
        pass

    def move(self, player_id, direction):
        pass
