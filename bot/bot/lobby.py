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

MAX_PLAYERS = 2


class Lobby:
    def __init__(self, uid, *, is_open=False) -> None:
        self.uid = uid
        self.players = {}
        self.host = None
        self.is_open = is_open

    def new_player(self, player: Player):
        assert len(self.players) < MAX_PLAYERS

        if len(self.players) == 0:
            self.host = player

        self.players[player.id] = player
        player.lobby = self

    def leave(self, player):
        assert self.host is not None

        if player.id == self.host.id:
            try:
                self.host = random.choice([*self.players.values()])
            except:
                self.host = None

        player.lobby = None
        self.players.pop(player.id)

        if len(self.players) == 0:
            self.is_open = True


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
