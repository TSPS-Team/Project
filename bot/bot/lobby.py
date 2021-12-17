#!/usr/bin/env python3

from __future__ import annotations
import random
import uuid
from enum import Enum, auto, unique
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, \
    MessageHandler, Filters

MAX_PLAYERS = 8

@unique
class States(Enum):
    MENU = auto()
    LOBBY = auto()
    GAME = auto()


class LobbyState:
    lobby_choice = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Quit",
                                     callback_data="quit"),
            ]
        ]

)
    host_choice = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Quit",
                                     callback_data="quit"),
                InlineKeyboardButton(text="Start",
                                     callback_data="start")
            ]
        ]
    )

    def __init__(self, player: Player, bot: Bot, lobby_manager):
        self.player = player
        self.bot = bot
        self.lobby_manager = lobby_manager

        lobby = self.player.lobby
        markup = self.host_choice if self.player.lobby.host.id == self.player.id else self.lobby_choice
        self.message = bot.send_message(chat_id=player.id,
                                        text=
                                        'You are connected to {} lobby {}\n'
                                        'Players connected: {}'
                                        '\n{}'
                                        .format(
                                            "public" if lobby.is_open else "private",
                                            lobby.uid,
                                            len(lobby.players),
                                            "\n".join(map(str, self.player.lobby.players.values()))),
                                        reply_markup=markup)


        for player in self.player.lobby.players.values():
            if player.id != self.player.id:
                player.state.update()

    def update(self):
        markup = self.host_choice if self.player.lobby.host.id == self.player.id else self.lobby_choice
        lobby = self.player.lobby
        self.message = self.bot.edit_message_text(
            chat_id=self.message.chat_id, message_id=self.message.message_id,
            text=
            'You are connected to {} lobby {}\n'
            'Players connected: {}'
            '\n{}'
            .format(
                "public" if lobby.is_open else "private",
                lobby.uid,
                len(lobby.players),
                "\n".join(map(str, self.player.lobby.players.values()))),
            reply_markup=markup)

    def start_game(self):
        for player in self.player.lobby.players.values():
            pass

    def callback(self, update, context):
        call_data = update.callback_query.data

        if call_data == "quit":
            lobby = self.player.lobby
            self.player.lobby.leave(self.player)
            self.player.state = MenuState(self.player, self.bot, self.lobby_manager)

            for player in lobby.players.values():
                player.state.update()
        elif call_data == "start":
            pass

    def text_callback(self, update, context):
        pass

    def state(self):
        return States.LOBBY


class MenuState:
    lobby_choice = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Join Public Lobby",
                                     callback_data="public"),
                InlineKeyboardButton(text="Join Private Lobby",
                                     callback_data="private"),
                InlineKeyboardButton(text="Create Lobby",
                                     callback_data="create")
            ]
        ]
    )

    def __init__(self, player, bot: Bot, lobby_manager: LobbyManager):
        self.player = player
        self.bot = bot
        self.lobby_manager = lobby_manager
        self.wait_for_uid = False

        self.menu_message = bot.send_message(
            player.id,
            'Welcome. Your nickname: {}'.format(player.name),
            reply_markup=self.lobby_choice)


    def callback(self, update, context):
        call_data = update.callback_query.data

        if call_data == "public":
            self.player.lobby = self.lobby_manager.connect_any(self.player)
            self.player.state = LobbyState(self.player, self.bot, self.lobby_manager)
        elif call_data == "private":
            self.wait_for_uid = True
            self.bot.send_message(chat_id=self.player.id, text="Enter lobby UID:")
        elif call_data == "create":
            self.player.lobby = self.lobby_manager.new_private(self.player)
            self.player.state = LobbyState(self.player, self.bot, self.lobby_manager)


    def text_callback(self, update: Update, context):
        if self.wait_for_uid:
            try:
                self.lobby_manager.connect_private(self.player, update.message.text)
                self.player.state = LobbyState(self.player, self.bot, self.lobby_manager)
            except:
                update.message.reply_text("No lobby with such uid found.")
                self.wait_for_uid = False
                self.player.state = MenuState(self.player, self.bot, self.lobby_manager)


    def state(self):
        return States.MENU


class GameState:
    def __init__(self, player, update, context):
        pass

    def state(self):
        return States.LOBBY


class Player:
    def __init__(self, name, id) -> None:
        self.name = name
        self.id = id
        self.lobby = None
        self.state = None

    def __str__(self):
        return self.name

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
            lobby = random.choice(self._open_lobbies())
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
