#!/usr/bin/env python3

from __future__ import annotations
import random
import uuid
from enum import Enum, auto, unique
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, \
    MessageHandler, Filters
from telegram.message import Message

from bot.bot.app_info import AppInfo
from bot.bot.base import Player
from bot.bot.redis_connect import get_reddis_connection

MAX_PLAYERS = 2


class Lobby:
    def __init__(self, uid, *, is_open=False) -> None:
        self.uid = uid
        self.players = {}
        self.host = None
        self.is_open = is_open
        self.redis_connection = get_reddis_connection()

        self.redis_connection.set(self.uid + ":is_open", int(self.is_open))

    def new_player(self, player: Player):
        assert len(self.players) < MAX_PLAYERS

        if len(self.players) == 0:
            self.host = player
            self.redis_connection.set(self.uid + ":host", player.id)

        self.players[player.id] = player
        self.redis_connection.hset(self.uid + ":" + str(player.id), "name", player.name)
        player.lobby = self

    def leave(self, player):
        assert self.host is not None

        if player.id == self.host.id:
            try:
                self.host = random.choice([*self.players.values()])
                self.redis_connection.set(self.uid + ":host", self.host.id)
            except:
                self.host = None
                self.redis_connection.delete(self.uid + ":host")

        player.lobby = None
        self.players.pop(player.id)
        self.redis_connection.delete(self.uid + ":" + str(player.id))

        if len(self.players) == 0:
            self.is_open = True
            self.redis_connection.set(self.uid + ":is_open", int(True))


class LobbyManager:
    def __init__(self) -> None:
        self.lobbies = {}

    def _open_lobbies(self):
        return [*filter(lambda x: x.is_open, self.lobbies.values())]

    def connect_any(self, player) -> Lobby:
        try:
            lobby = random.choice([*filter(lambda x: len(x.players) < MAX_PLAYERS,
                                           self._open_lobbies())])
        except:
            lobby = self.new_lobby(is_open=True)

        lobby.new_player(player)

        return lobby

    def connect_private(self, player, uid) -> Lobby:
        lobby = self.lobbies[uid]
        lobby.new_player(player)

        return lobby

    def new_private(self, player) -> Lobby:
        lobby = self.new_lobby(is_open=False)
        lobby.new_player(player)
        return lobby

    def new_lobby(self, is_open) -> Lobby:
        uid = str(uuid.uuid4())[:8]
        result = Lobby(uid, is_open=is_open)
        self.lobbies[result.uid] = result

        return result
