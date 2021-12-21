#!/usr/bin/env python3

import io
from typing import IO
import telegram
from telegram.bot import Bot
from telegram.error import BadRequest
from telegram.files.inputmedia import InputMediaPhoto
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.message import Message
from telegram.replymarkup import ReplyMarkup
from bot.bot.base import Player, State

class MapState(State):
    def __init__(self, player, app_info) -> None:
        super().__init__(player, app_info)

    def update(self):
        pass

def add(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return (a[0] + b[0], a[1] + b[1])

def str_to_coord(s: str) -> tuple[int, int]:
    result = (0, 0)
    if "l" in s:
        result = add(result, (-1, 0))
    if "u" in s:
        result = add(result, (0, -1))
    if "d" in s:
        result = add(result, (0, 1))
    if "r" in s:
        result = add(result, (1, 0))
    return result

class CameraState(MapState):
    position: tuple[int, int]

    def __init__(self, player: Player, app_info: 'AppInfo', old_message_id: int=None):
        super().__init__(player, app_info)

        self.position = (player.game.get_hero_position(player))

        if old_message_id is None:
            self.message_id = self.bot.send_photo(
                **self.get_message_data(new=True)).message_id
        else:
            self.message_id = old_message_id
            self.update()


    def get_message_data(self, new=False):
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Camera", callback_data="c"),
                    InlineKeyboardButton(text="Hero", callback_data="h")
                ],
                [
                    InlineKeyboardButton(text="↖",
                                         callback_data="camera_lu"),
                    InlineKeyboardButton(text="⬆",
                                         callback_data="camera_u"),
                    InlineKeyboardButton(text="↗",
                                         callback_data="camera_ru"),

                        InlineKeyboardButton(text="↖",
                                             callback_data="hero_lu"),
                    InlineKeyboardButton(text="⬆",
                                         callback_data="hero_u"),
                    InlineKeyboardButton(text="↗",
                                         callback_data="hero_ru"),
                ],
                [
                    InlineKeyboardButton(text="⬅",
                                         callback_data="camera_l"),
                    InlineKeyboardButton(text="⏹",
                                         callback_data="camera_center"),
                    InlineKeyboardButton(text="➡",
                                         callback_data="camera_r"),

                        InlineKeyboardButton(text="⬅",
                                             callback_data="hero_l"),
                    InlineKeyboardButton(text="⏹",
                                         callback_data="hero_center"),
                    InlineKeyboardButton(text="➡",
                                         callback_data="hero_r"),
                ],
                [
                    InlineKeyboardButton(text="↙",
                                         callback_data="camera_ld"),
                    InlineKeyboardButton(text="⬇",
                                         callback_data="camera_d"),
                    InlineKeyboardButton(text="↘",
                                         callback_data="camera_rd"),

                        InlineKeyboardButton(text="↙",
                                             callback_data="hero_ld"),
                    InlineKeyboardButton(text="⬇",
                                         callback_data="hero_d"),
                    InlineKeyboardButton(text="↘",
                                         callback_data="hero_rd"),
                ]
            ]
        )

        image = self.player.game.interface.get_image(self.position, self.player.game.get_player_id(self.player))
        image_bytes = io.BytesIO()
        image.convert("RGB").save(image_bytes, format="jpeg", optimize=True, quality=50)
        if new:
            return {
                "reply_markup": reply_markup,
                "photo": image_bytes.getvalue(),
                "chat_id": self.player.id,
                "caption": "",
            }
        else:
            return {
                "reply_markup": reply_markup,
                "media": InputMediaPhoto(image_bytes.getvalue()),
                "chat_id": self.player.id,
                "message_id": self.message_id,
            }

    def callback(self, update, context):
        call_data = update.callback_query.data
        call_data = call_data.split("_")

        if call_data[0] == "camera":
            if call_data[1] != "center":
                coord = str_to_coord(call_data[1])
                self.position = add(self.position, coord)
                self.update()
        elif call_data[0] == "hero":
            if call_data[1] != "center":
                id = self.player.game.get_player_id(self.player)
                self.player.game.server._game_instance.move_hero((id, "hero", 0), call_data[1])

                for player in self.player.game.players:
                    player.state.update()

    def text_callback(self, update, context):
        pass

    def update(self):
        try:
            self.bot.edit_message_media(**self.get_message_data())
        except BadRequest:
            pass
