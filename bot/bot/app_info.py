#!/usr/bin/env python3
from pymongo import mongo_client
from pymongo.mongo_client import MongoClient
from server.server import Interface, Server
from telegram.bot import Bot
from bot.bot.base import Player
from bot.bot.game import Game
from bot.bot.game_states import CameraState
from bot.bot.mongodb_connect import Connect

class AppInfo:
    lobby_manager: 'LobbyManager'
    bot: Bot
    running_games: dict[str, Game]
    mongodb_connection: MongoClient
    def __init__(self):
        self.mongodb_connection = Connect.get_connection()
        self.running_games = dict()

    def new_game(self, uid: str, *players: Player):

        m = Connect.get_random_map()
        data = Connect.get_unit_data()

        serv = Server(m, data)

        game = Game([*players], serv)
        self.running_games[uid] = game

        for player in players:
            player.game = game
            player.state = CameraState(player, self)
