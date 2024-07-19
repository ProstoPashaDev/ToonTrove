from telebot import TeleBot
from telebot import types
from random import randint

from ToonTroveBotService import ToonTroveBotService

# TODO
token = ('7311140144:AAEm9neycQaXR9pBnPNXWsYnZd1fHw2zTWs')
bot = TeleBot(token)

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
std_markup = types.InlineKeyboardMarkup()

toonTroveBotService = ToonTroveBotService()

dict_rarity = {"1": "common", "2": "rare", "3": "specific", "4": "legendary"}
dict_ttc = {"1": "1", "2": "5", "3": "15", "4": "50"}
dict_points = {"1": "10", "2": "50", "3": "100", "4": "1000"}

username = ""


def initialize_bot():
    main_markup.add(types.KeyboardButton(text="Watch the movie"), types.KeyboardButton(text="Collection"),
                    types.KeyboardButton(text="Toon Trove studio"))

    std_markup.add(types.InlineKeyboardButton(text="Influence", callback_data='influence'))
    std_markup.add(types.InlineKeyboardButton(text="My account", callback_data='my_account'))
    std_markup.add(types.InlineKeyboardButton(text="Squads", callback_data='squads'))
    std_markup.add(types.InlineKeyboardButton(text="Quiz", callback_data='quiz'))
    std_markup.add(types.InlineKeyboardButton(text="Bet", callback_data='bet'))
    std_markup.add(types.InlineKeyboardButton(text="Shop", callback_data='shop'))
    std_markup.add(types.InlineKeyboardButton(text="Pass", callback_data='pass'))
    std_markup.add(types.InlineKeyboardButton(text="Trade", callback_data='trade'))
    std_markup.add(types.InlineKeyboardButton(text="Donat", callback_data='donat'))


@bot.message_handler(commands=['start'])
def start_bot(message):
    # TODO
    bot.send_message(message.chat.id, text="Привет, {0.first_name} 👋".format(message.from_user),
                     reply_markup=main_markup)




@bot.message_handler(content_types=['text'])
def main_btn_ans(message):
    if (message.text == "Watch the movie"):
        card_name = toonTroveBotService.get_card()
        #print(card_name)
        #print(f"Бро, лови свою карточку \n \n Редкость: {dict_rarity[card_name[0]]} \nTTC: +{dict_ttc[card_name[0]]} \nPoints: +{dict_points[card_name[0]]}")
        bot.send_photo(message.chat.id, caption=f"Бро, лови свою карточку \n \nРедкость: {dict_rarity[card_name[0]]} \nTTC: +{dict_ttc[card_name[0]]} \nPoints: +{dict_points[card_name[0]]}", photo=open(card_name, 'rb'))



    elif (message.text == "Collection"):
        bot.send_message(message.chat.id, text="#TODO")

    elif (message.text == "Toon Trove studio"):
        bot.send_message(message.chat.id, text="Еще больше кнопок", reply_markup=std_markup)



    else:
        # TODO
        bot.send_message(message.chat.id, text="Error 404 тинкер для геев")


@bot.callback_query_handler(func=lambda callback: True)
def ttstd_ans(callback):
    if callback.message:
        if (callback.data == "influence"):
            bot.send_message(callback.message.chat.id, text="Топ игроков")
            bot.send_message(callback.message.chat.id, text="1) Pav 9999999999999999999\n2) Ivn 9999999999999999998")
        elif (callback.data == "my_account"):
            bot.send_message(callback.message.chat.id, text="Reading from db")


def start_bot():
    bot.polling(none_stop=True, interval=0)


initialize_bot()
start_bot()
