# -*- coding: utf-8 -*-

from settings import TELEGRAM_TOKEN
from telebot import TeleBot, types
from database import Database

bot = TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    user_markup = types.ReplyKeyboardMarkup(True, False, True)
    itembtn1 = types.KeyboardButton('/start_btc')
    itembtn2 = types.KeyboardButton('/stop')
    user_markup.add(itembtn1, itembtn2)
    answer = '/start_btc Включить уведомления о цене btc на binance.com\n\n' \
             '/stop Отключить оповещения'
    bot.send_message(message.from_user.id, answer, reply_markup=user_markup)


@bot.message_handler(commands=['start_btc'])
def handle_start(message):
    db = Database()
    db.write_chat_id(message.chat.id)
    db.close()

    user_markup = types.ReplyKeyboardMarkup(True, False, True)
    itembtn1 = types.KeyboardButton('/start')
    itembtn2 = types.KeyboardButton('/stop')
    user_markup.add(itembtn1, itembtn2)
    answer = 'Уведомления включены'
    bot.send_message(message.from_user.id, answer, reply_markup=user_markup)


@bot.message_handler(commands=['stop'])
def handle_start(message):
    db = Database()
    db.delete_chat_id(message.chat.id)
    db.close()

    user_markup = types.ReplyKeyboardMarkup(True, False, True)
    itembtn1 = types.KeyboardButton('/start')
    itembtn2 = types.KeyboardButton('/start_btc')
    user_markup.add(itembtn1, itembtn2)
    answer = 'Уведомления отключены'
    bot.send_message(message.from_user.id, answer, reply_markup=user_markup)


if __name__ == '__main__':

    try:
        bot.polling(none_stop=False, interval=0, timeout=30)
    except KeyboardInterrupt:
        bot.stop_polling()
        exit()
