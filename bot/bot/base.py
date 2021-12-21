#!/usr/bin/env python3

from __future__ import annotations
from server import Interface

from telegram.bot import Bot

class State:
    player: Player
    app_info: 'AppInfo'
    bot: Bot

    def __init__(self, player, app_info) -> None:
        self.player = player
        self.bot = app_info.bot
        self.app_info = app_info

    def callback(self, update, context):
        pass

    def text_callback(self, update, context):
        pass

class Player:
    lobby: 'Lobby'
    state: State
    game: 'Game'
    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id

    def __str__(self):
        return self.name

