from telebot import TeleBot
from telebot import types
from random import randint

# TODO
token = ('7311140144:AAEm9neycQaXR9pBnPNXWsYnZd1fHw2zTWs')
bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def initialize_bot(message):
    # TODO
    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    bot.send_message(message.chat.id, text="Привет, {0.first_name} 👋".format(message.from_user))
    getcard_button = types.KeyboardButton("Watch the movie")
    collection_button = types.KeyboardButton("Collection")
    toontrovestd_button = types.KeyboardButton("Toon Trove studio")
    main_markup.add(getcard_button, collection_button, toontrovestd_button)
    bot.send_message(message.chat.id, text="Воспользуйся кнопками", reply_markup=main_markup)


@bot.message_handler(content_types=['text'])
def main_btn_ans(message):
    if (message.text == "Watch the movie"):
        bot.send_message(message.chat.id, text=f"вы получили карточку под номером {randint(1, 100)}")
        bot.send_message(message.chat.id, text="Шанс ее выпадения 1%")

    elif (message.text == "Collection"):
        bot.send_message(message.chat.id, text="#TODO")

    elif (message.text == "Toon Trove studio"):
        std_markup = types.InlineKeyboardMarkup()
        std_markup.add(types.InlineKeyboardButton(text="Influence", callback_data='influence'))
        std_markup.add(types.InlineKeyboardButton(text="My account", callback_data='my_account'))
        std_markup.add(types.InlineKeyboardButton(text="Squads", callback_data='squads'))
        std_markup.add(types.InlineKeyboardButton(text="Quiz", callback_data='quiz'))
        std_markup.add(types.InlineKeyboardButton(text="Bet", callback_data='bet'))
        std_markup.add(types.InlineKeyboardButton(text="Shop", callback_data='shop'))
        std_markup.add(types.InlineKeyboardButton(text="Pass", callback_data='pass'))
        std_markup.add(types.InlineKeyboardButton(text="Trade", callback_data='trade'))
        std_markup.add(types.InlineKeyboardButton(text="Donat", callback_data='donat'))


        bot.send_message(message.chat.id, text = "Еще больше кнопок", reply_markup=std_markup)



    else:
        # TODO
        bot.send_message(message.chat.id, text="Error 404 тинкер для геев")



@bot.callback_query_handler(func=lambda callback: True)
def ttstd_ans(callback):
    if callback.message:
        if (callback.data == "influence"):
            bot.send_message(callback.message.chat.id, text="Топ игроков")
            bot.send_message(callback.message.chat.id, text="1) Pav 9999999999999999999\n2) Ivn 9999999999999999998")


def initialize_bot():
    pass

def start_bot():
    bot.polling(none_stop=True, interval=0)



start_bot()
