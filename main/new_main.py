from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update, PhotoSize
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, ConversationHandler, \
    MessageHandler, Filters
from config import bot_token
from resources_manager.sql import sqlite_3_add_user, sqlite_3_select_identity_name
import server.server
import json

interface = None

LOGIN, SIGNUP, GAME = range(3)


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


def start_handler(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome to the game. First of all, log in or sign up to the bot',
                              reply_markup=choice_start)


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
        return SIGNUP


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
        update.message.reply_text("You log in successful. You'll be redirect to game lobby")
        del id, text, info
        return GAME
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
    elif info[0] == ls[0] and info[1] == ls[1]:
        update.message.reply_text("You sign up successful. You'll be redirect to game lobby")
        return GAME
    else:
        update.message.reply_text("Name or password doesn't correctly write. Try again")
        return SIGNUP


def game_handler(update: Update, context: CallbackContext):
    s = None
    with open(r"D:\map1.json") as m:
        with open(r"D:\SP-Tileset.json") as t:
            with open(r"D:\AllAssetsPreview.json") as e:
                with open(r"D:\SP-Tileset.png", "rb") as i:
                    with open(r"D:\AllAssetsPreview.png", "rb") as ei:
                        m = server.server.DBMap(json.load(m),
                                  server.server.Tileset(json.load(e),
                                          ei.read()),
                                  server.server.Tileset(json.load(t),
                                          i.read()))
    s = server.server.Server(m)

    global interface
    interface = s.get_interface()
    image = interface.get_view(1)
    image.save("out.png")

    update.message.reply_photo(open("out.png", 'rb'), reply_markup=choice_move)
    return GAME


def cancel_handler(update: Update, context: CallbackContext):
    update.message.reply_text("Cancel of operation, please, press /start")
    return ConversationHandler.END


def main():
    bot = Bot(token=bot_token)
    updater = Updater(bot=bot)

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start_handler),
            CallbackQueryHandler(callback_query_start_handler)
        ],
        states={
            LOGIN: [
                MessageHandler(Filters.all, login_handler)
            ],
            SIGNUP: [
                MessageHandler(Filters.all, signup_handler),
                CallbackQueryHandler(callback_query_signup_handler)
            ],
            GAME: [
                MessageHandler(Filters.all, game_handler),
                CallbackQueryHandler(callback_query_game_handler)
            ],
        },
        fallbacks=[
            CommandHandler('cancel', cancel_handler),
        ],
    )

    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
