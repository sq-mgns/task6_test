import os
import time

import telebot


token = os.getenv("TELEGRAM_TOKEN")

if not token:
    raise RuntimeError("TELEGRAM_TOKEN is not set")

bot = telebot.TeleBot(token, threaded=False)

start_text = (
    "Бот умеет:\n"
    "- распознавать текст с картинок;\n"
    "- генерировать голосовые сообщения из текста;\n"
    "- переводить голосовые сообщения в текст."
)

voice_text = "тест тест раз два три проверка"
photo_text = "доброе утро\n\nгде"


@bot.message_handler(commands=["start", "help"])
def send_start(message):
    bot.send_message(message.chat.id, start_text)


@bot.message_handler(content_types=["voice"])
def send_voice_result(message):
    bot.send_message(message.chat.id, voice_text)


@bot.message_handler(content_types=["photo"])
def send_photo_result(message):
    bot.send_message(message.chat.id, photo_text)


@bot.message_handler(func=lambda message: True)
def send_default(message):
    bot.send_message(message.chat.id, "Сообщение получено")


while True:
    try:
        print("Bot is running")
        bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
    except Exception as error:
        print(error)
        time.sleep(3)
