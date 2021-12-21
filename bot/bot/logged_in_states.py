from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from bot.bot.app_info import AppInfo
from bot.bot.base import *
from bot.bot.game_states import CameraState

class LobbyState(State):
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

    def __init__(self, player: Player, app_info: AppInfo):
        super().__init__(player, app_info)

        lobby = self.player.lobby
        markup = self.host_choice if self.player.lobby.host.id == self.player.id else self.lobby_choice
        self.message = self.bot.send_message(chat_id=player.id,
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
                assert(isinstance(player.state, LobbyState))
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

    def callback(self, update, context):
        call_data = update.callback_query.data

        lobby = self.player.lobby
        if call_data == "quit":
            self.player.lobby.leave(self.player)
            self.player.state = MenuState(self.player, self.app_info)

            for player in lobby.players.values():
                player.state.update()
        elif call_data == "start":
            assert (self.player.id == self.player.lobby.host.id)

            self.app_info.new_game(self.player.lobby.uid, *lobby.players.values())

    def text_callback(self, update, context):
        pass


class MenuState(State):
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

    def __init__(self, player, app_info: AppInfo):
        super().__init__(player, app_info)

        self.wait_for_uid = False

        self.menu_message = self.bot.send_message(
            player.id,
            'Welcome. Your nickname: {}'.format(player.name),
            reply_markup=self.lobby_choice)


    def callback(self, update, context):
        call_data = update.callback_query.data

        if call_data == "public":
            self.player.lobby = self.app_info.lobby_manager.connect_any(self.player)
            self.player.state = LobbyState(self.player, self.app_info)
        elif call_data == "private":
            self.wait_for_uid = True
            self.bot.send_message(chat_id=self.player.id, text="Enter lobby UID:")
        elif call_data == "create":
            self.player.lobby = self.app_info.lobby_manager.new_private(self.player)
            self.player.state = LobbyState(self.player, self.app_info)


    def text_callback(self, update: Update, context):
        if self.wait_for_uid:
            try:
                self.app_info.lobby_manager.connect_private(self.player, update.message.text)
                self.player.state = LobbyState(self.player, self.app_info)
            except:
                update.message.reply_text("No lobby with such uid found.")
                self.wait_for_uid = False
                self.player.state = MenuState(self.player, self.app_info)
