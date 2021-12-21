#!/usr/bin/env python3

from server.server import Interface, Server
from bot.bot.base import Player


class Game:
    players: list[Player]
    tg_game_id: dict
    server: Server
    interface: Interface

    def __init__(self, players: list[Player], server: Server) -> None:
        self.players = players
        self.server = server
        self.interface = server.get_interface()
        self.tg_game_id = dict()

        for i, player in enumerate(players):
            self.tg_game_id[player.id] = i + 1

    def get_player_id(self, player):
        return self.tg_game_id[player.id]

    def get_hero_position(self, player):
        return self.server._game_instance.get_hero_position((self.get_player_id(player), "hero", 0))
