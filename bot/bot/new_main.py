from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, \
    MessageHandler, Filters
from .config import bot_token
from .resources_manager.sql import sqlite_3_add_user, sqlite_3_select_identity_name

import server
import json

interface = None
count_1 = 0
ready_1 = False
players = {}

from .lobby import LobbyManager, LobbyState, MenuState, Player
from .app_info import AppInfo
app_info = AppInfo()
app_info.lobby_manager = LobbyManager()


DEV_TEST = True

LOGGEDIN, LOGIN, SIGNUP, LOBBY, WAITROOM, GAME = range(6)


choice_start = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Log in",
                                     callback_data="login"),
                InlineKeyboardButton(text="Sign up",
                                     callback_data="signup"),
            ]
        ]
)


choice_signup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Log in",
                                     callback_data="loginnew"),
                InlineKeyboardButton(text="Try again",
                                     callback_data='tryagain'),
            ]
        ]
)


choice_lobby = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Lobby#1",
                                     callback_data="lobby1"),
            ]
        ]
)


choice_waitroom = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ready?",
                                     callback_data="ready")
            ],
            [
                InlineKeyboardButton(text="Leave the lobby",
                                     callback_data="leave")
            ]
        ]
)


choice_move = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Left",
                                     callback_data="left"),
                InlineKeyboardButton(text="Right",
                                     callback_data="right"),
                InlineKeyboardButton(text="Up",
                                     callback_data="up"),
                InlineKeyboardButton(text="Down",
                                     callback_data="down"),
            ]
        ]
)

choice_main_menu = InlineKeyboardMarkup(
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

class Handler:

    def start_handler(update: Update, context: CallbackContext):
        update.message.reply_text('Welcome to the game. First of all, log in or sign up to the bot',
                                  reply_markup=choice_start)

    def login_handler(update: Update, context: CallbackContext):
        id = update.message.chat.id
        text = update.message.text
        info = text.split()
        info.append(id)
        # print(info)

        ls = sqlite_3_select_identity_name(info[0])
        # print(ls)
        if not ls:
            sqlite_3_add_user(info[0], info[1], int(info[2]))
            update.message.reply_text("You log in successful. Enter the command /lobby")
            del id, text, info
            return LOBBY
        else:
            update.message.reply_text(f"Name '{info[0]}' is exist. Enter another name")
            del id, text, info
            return LOGIN

    def signup_handler(update: Update, context: CallbackContext):
        id = update.message.chat.id
        text = update.message.text
        info = text.split()
        info.append(id)
        # print(info)

        ls = sqlite_3_select_identity_name(info[0])
        # print(ls)
        if not ls:
            update.message.reply_text("This account doesn't exist. You can log in or try again",
                                      reply_markup=choice_signup)
            return SIGNUP
        elif info[0] == ls[1] and info[1] == ls[2]:
            update.message.reply_text("You sign up successful. Enter the command /lobby")
            return LOBBY
        else:
            update.message.reply_text("Name or password doesn't correctly write. Try again")
            return SIGNUP

    def lobby_handler(update: Update, context: CallbackContext):
        update.message.reply_text("Choose the lobby:", reply_markup=choice_lobby)

    def waitroom_handler(update: Update, context: CallbackContext):
        global ready_1
        update.message.reply_text("You're in wait room. Wait for other players to start the game "
                                  "(the counter will be updated every 5 seconds)", reply_markup=choice_waitroom)
        # msg = update.message.reply_text(f"Count of players: {count_1}/4")
        # while ready_1 is False:
        #     time.sleep(5)
        #     context.bot.delete_message(chat_id=update.message.chat_id,
        #                                message_id=msg.message_id)
        #     msg = update.message.reply_text(f"Count of players: {count_1}/4")

    def game_handler(update: Update, context: CallbackContext):
        s = None
        with open(r"D:\map1.json") as m:
            with open(r"D:\SP-Tileset.json") as t:
                with open(r"D:\AllAssetsPreview.json") as e:
                    with open(r"D:\SP-Tileset.png", "rb") as i:
                        with open(r"D:\AllAssetsPreview.png", "rb") as ei:
                            m = server.DBMap(json.load(m),
                                    server.Tileset(json.load(e),
                                            ei.read()),
                                    server.Tileset(json.load(t),
                                            i.read()))
        s = server.Server(m)

        global interface
        interface = s.get_interface()
        image = interface.get_view(1)
        image.save("out.png")

        update.message.reply_photo(open("out.png", 'rb'), reply_markup=choice_move)
        return GAME

    def cancel_handler(update: Update, context: CallbackContext):
        update.message.reply_text("Cancel of operation, please, press /start")
        return ConversationHandler.END


class CallbackQuery:
    def callback_query_start_handler(update: Update, context: CallbackContext):
        call_data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id

        if call_data == "login":
            update.callback_query.bot.send_message(chat_id=chat_id,
                                                   text="Log in was started. Enter the name and password:")
            return LOGIN
        elif call_data == "signup":
            update.callback_query.bot.send_message(chat_id=chat_id,
                                                   text="Sign up was started. Enter the name and password:")
            return SIGNUP

    def callback_query_signup_handler(update: Update, context: CallbackContext):
        call_data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id

        if call_data == "loginnew":
            update.callback_query.bot.send_message(chat_id=chat_id,
                                                   text="Log in was started. Enter the name and password:")
            return LOGIN
        elif call_data == "tryagain":
            update.callback_query.bot.send_message(chat_id=chat_id,
                                                   text="Sign up was started. Enter the name and password:")
            return SIGNUP

    def callback_query_lobby_handler(update: Update, context: CallbackContext):
        call_data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id

        if call_data == "lobby1":
            global count_1
            global ready_1
            if count_1 == 4:
                update.callback_query.bot.send_message(chat_id=chat_id,
                                                       text="Lobby#1 is full, choose another free lobby")
                return LOBBY
            count_1 += 1
            # print(count_1)
            players[f"player {count_1}"] = chat_id
            if len(players.keys()) == 1:
                ready_1 = True
            # print(players[f"player {count_1}"])
            update.callback_query.bot.send_message(chat_id=chat_id,
                                                   text="Enter command /waitroom and wait another players")

            return WAITROOM

    def callback_query_waitroom_handler(update: Update, context: CallbackContext):
        call_data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id

        if call_data == "ready":
            if ready_1:
                update.callback_query.bot.send_message(chat_id=chat_id,
                                                       text="Lobby is full, enter command /game to start")

                return GAME
            else:
                update.callback_query.bot.send_message(chat_id=chat_id,
                                                       text=f"Count of players: {count_1}/4, wait for other players")

            return WAITROOM

    def callback_query_game_handler(update: Update, context: CallbackContext):
        call_data = update.callback_query.data
        chat_id = update.callback_query.message.chat.id

        if call_data == "left":
            interface.move(1, (-1, 0))

        if call_data == "right":
            interface.move(1, (1, 0))

        if call_data == "up":
            interface.move(1, (0, -1))

        if call_data == "down":
            interface.move(1, (0, 1))

        image = interface.get_view(1)
        image.save("out.png")

        update.callback_query.bot.send_photo(chat_id=chat_id, photo=open("out.png", 'rb'), reply_markup=choice_move)
        return GAME


def logged_in_callback(update: Update, context: CallbackContext):
    player = players[update.effective_user.id]
    return player.state.callback(update, context)

def logged_in_text_callback(update: Update, context: CallbackContext):
    player = players[update.effective_user.id]
    return player.state.text_callback(update, context)


def dev_start_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    player = Player(user.first_name, user.id)
    players[player.id] = player
    player.state = MenuState(player, context.bot, app_info)

    return LOGGEDIN


def main():

    bot = Bot(token=bot_token)
    updater = Updater(bot=bot)


    if not DEV_TEST:
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', Handler.start_handler),
            ],
            states={
                LOGIN: [
                    MessageHandler(Filters.all, Handler.login_handler)
                ],
                SIGNUP: [
                    MessageHandler(Filters.all, Handler.signup_handler),
                    CallbackQueryHandler(CallbackQuery.callback_query_signup_handler)
                ],
                LOBBY: [
                    CommandHandler('lobby', Handler.lobby_handler),
                    CallbackQueryHandler(CallbackQuery.callback_query_lobby_handler)
                ],
                WAITROOM: [
                    CommandHandler('waitroom', Handler.waitroom_handler),
                    CallbackQueryHandler(CallbackQuery.callback_query_waitroom_handler)
                ],
                GAME: [
                    CommandHandler('game', Handler.game_handler),
                    CallbackQueryHandler(CallbackQuery.callback_query_game_handler)
                ],
            },
            fallbacks=[
                CommandHandler('cancel', Handler.cancel_handler),
            ],
        )
    else:
        conv_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', dev_start_handler),
            ],
            states={
                LOGGEDIN: [
                    CallbackQueryHandler(logged_in_callback),
                    MessageHandler(Filters.text, logged_in_text_callback)
                ]
            },
            fallbacks=[
                CommandHandler('cancel', Handler.cancel_handler),
            ]
        )

    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
