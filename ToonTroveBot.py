from telebot import TeleBot
from telebot import types
import time
import math

from ToonTroveBotService import ToonTroveBotService
from ToonTroveDatabase import ToonTroveDatabase


token = ('7311140144:AAEm9neycQaXR9pBnPNXWsYnZd1fHw2zTWs')
bot = TeleBot(token)

main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
std_markup = types.InlineKeyboardMarkup()
shop_markup_list = []

toonTroveBotService = ToonTroveBotService()
toonTroveDataBase = ToonTroveDatabase()

shop_data = toonTroveBotService.get_shop_data()

dict_rarity = {"1": "common", "2": "rare", "3": "specific", "4": "legendary"}
dict_ttc_getcard = {"1": "1", "2": "5", "3": "15", "4": "50"}
dict_points_getcard = {"1": "10", "2": "50", "3": "100", "4": "1000"}

username = ""
attempt_time = 180

def initialize_bot_markup():
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

    for i in range(len(shop_data)):
        shop_markup = types.InlineKeyboardMarkup()
        shop_markup.add(types.InlineKeyboardButton(text=f"{shop_data[i][2]} TTC", callback_data="offer1"))
        shop_markup.add(types.InlineKeyboardButton(text="<<", callback_data=f"<<{i}"), types.InlineKeyboardButton(text=f"{i+1}/{len(shop_data)}", callback_data="9/9"), types.InlineKeyboardButton(text=">>", callback_data=f">>{i}"))


        shop_markup_list.append(shop_markup)


def initialize_bot_dbconnection():
    toonTroveDataBase.connect(toonTroveDataBase.load_config())



@bot.message_handler(commands=['start'])
def start_bot(message):
    toonTroveDataBase.select_user_info(message.from_user.username)
    if not toonTroveDataBase.check_user(message.from_user.username):
        toonTroveDataBase.insert_new_user(message.from_user.username)

    bot.send_message(message.chat.id, text="Привет, {0.first_name} 👋".format(message.from_user),
                     reply_markup=main_markup)





@bot.message_handler(content_types=['text'])
def main_btn_ans(message):
    if (message.text == "Watch the movie"):
        card_name = toonTroveBotService.get_card()
        attempts = toonTroveDataBase.get_attempts(message.from_user.username)
        attempts += toonTroveDataBase.check_attempt(message.from_user.username, int(time.time()), attempt_time)
        if attempts > 0:
            #Добавление попыток
            toonTroveDataBase.update_ttc_points(message.from_user.username, int(dict_ttc_getcard[card_name[0]]), int(dict_points_getcard[card_name[0]]))

            user_data = toonTroveDataBase.select_user_info(message.from_user.username)[0]
            bot.send_photo(message.chat.id, caption=f"Бро, лови свою карточку \n \nРедкость: {dict_rarity[card_name[0]]} \nTTC: +{dict_ttc_getcard[card_name[0]]} \nPoints: +{dict_points_getcard[card_name[0]]}\n\nTTC за все время: {user_data[1]}\nPoints за все время: {user_data[2]}", photo=open(card_name, 'rb'))
            toonTroveDataBase.update_getcard(message.from_user.username, attempts, int(time.time()))
            print(toonTroveDataBase.select_user_info(message.from_user.username))
        else:
            time_getcard = toonTroveDataBase.get_time_getcard(message.from_user.username)
            bot.send_message(message.chat.id, f"Следующая попытка будет доступна через {(attempt_time - (int(time.time()) - time_getcard)) // 3600} ч {math.ceil((attempt_time - (int(time.time()) - time_getcard)) / 60)} мин")
    elif (message.text == "Collection"):
        bot.send_message(message.chat.id, text="#TODO")
    elif (message.text == "Toon Trove studio"):
        bot.send_message(message.chat.id, text="Еще больше кнопок", reply_markup=std_markup)
    else:
        # TODO
        bot.send_message(message.chat.id, text="Error 404 такой команды нет")


@bot.callback_query_handler(func=lambda callback: True)
def ttstd_ans(callback):
    if callback.message:
        if callback.data == "influence":
            bot.send_message(callback.message.chat.id, text="Топ игроков")
            bot.send_message(callback.message.chat.id,
                             text="1) Pav 9999999999999999999\n2) Ivn 9999999999999999998")
        elif callback.data == "my_account":
            bot.send_message(callback.message.chat.id, text="Reading from db")
        elif callback.data == "shop":
            bot.send_photo(callback.message.chat.id, caption=shop_data[0][1], photo=open(shop_data[0][0], "rb"),
                           reply_markup=shop_markup_list[0])
            print(toonTroveBotService.get_shop_data())
        elif callback.data == ">>0":
            change_shop_offer(1, callback)
        elif callback.data == ">>1":
            change_shop_offer(2, callback)
        elif callback.data == ">>2":
            change_shop_offer(0, callback)
        elif callback.data == "<<0":
            change_shop_offer(2, callback)
        elif callback.data == "<<1":
            change_shop_offer(0, callback)
        elif callback.data == "<<2":
            change_shop_offer(1, callback)

def change_shop_offer(offer_number, callback):
    bot.edit_message_media(media=types.InputMediaPhoto(open(shop_data[offer_number][0], "rb")),
                           chat_id=callback.message.chat.id, message_id=callback.message.message_id,
                           reply_markup=shop_markup_list[offer_number])
    bot.edit_message_caption(caption=shop_data[offer_number][1], chat_id=callback.message.chat.id,
                             message_id=callback.message.message_id,
                             reply_markup=shop_markup_list[offer_number])

def start_bot():
    bot.polling(none_stop=True, interval=0)


initialize_bot_markup()
initialize_bot_dbconnection()
start_bot()
