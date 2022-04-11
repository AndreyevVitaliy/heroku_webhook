import pprint

import telebot
import telebot.types as types
import os
from flask import Flask, request
import logging
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
#
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
# from googleapiclient.discovery import build

token = '5178608519:AAFJdqk18jIXJp7TOe7gHmnDu74Fc8AmDbY'
bot = telebot.TeleBot(token)

@bot.message_handler(commands='start')
def start_message(message):
    bot.send_message(message.chat.id, 'Привет ' + message.from_user.first_name + ' Как дела?')
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton("Начать работу")
    # markup.add(item1)

@bot.message_handler(content_types='text')
def text_message(message):
    bot.send_message(message.chat.id, 'Функция пока не работает')
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # item1 = types.KeyboardButton("Начать работу")
    # markup.add(item1)

# @bot.message_handler(commands=['button'])
# def button_message(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("Кнопка")
#     markup.add(item1)
#     bot.send_message(message.chat.id,'' , reply_markup=markup)
#
#
# @bot.chosen_inline_handler(func=lambda chosen_inline_result: True)
# def test_chosen(chosen_inline_result):
#     pass
#     # Process all chosen_inline_result.

# @bot.inline_handler(lambda query: query.query == 'text')
# def query_text(inline_query):
#     try:
#         r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
#         r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
#         bot.answer_inline_query(inline_query.id, [r, r2])
#     except Exception as e:
#         print(e)


# @bot.message_handler(content_types='text')
# def text_message(message):
#     bot.send_message(message.chat_id, "Да")


# @bot.message_handler(content_types='photo')
# def download_photo(message):
#     bot.send_message(message.chat_id, "Пока не работает функция")
#


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://andv-webhook.herokuapp.com/") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)

