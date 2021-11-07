from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from main.config import api_id, api_hash, bot_token

bot = Client("test", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


idMessage = 0


choice = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Log in", callback_data="login"),
                InlineKeyboardButton(text="Sign up", callback_data="signup"),
            ]
        ]
    )


next = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Next", callback_data="next")
            ]
        ]
)


@bot.on_message(filters.command(commands=['start']))
def registration(client, message):
    bot.send_message(message.chat.id, "Welcome to the game. First of all, log in or sign up to the bot"
                     , reply_markup=choice)
    idMessage = message.message_id

# @bot.on_callback_query(group=0)
# def callback_query_handler(client, message, CallbackQuery):
#     log_in = str(CallbackQuery.data)[0]
#     sign_up = str(CallbackQuery.data)[1]


@bot.on_callback_query(group=0)
def login_signin(client, call: CallbackQuery):
    call_data = call.data
    if call_data == "login":
        bot.send_message(call.message.chat.id, "Log in was started. Enter the name and password:", reply_markup=next)
    elif call_data == "signup":
        bot.send_message(call.message.chat.id, "Sign up was started")
    elif call_data == "next":
        print(bot.get_messages(call.message.chat.id, idMessage+1))


bot.run()
