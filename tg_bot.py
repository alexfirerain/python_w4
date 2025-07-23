# бот на Aiogram (см. статью)
# токен обычно идёт из другого файла
token = "7623744358:AAGDl6HJVlo7L9q58kqu7woFaRJ8f-XnTiw"

import telebot
from telebot import types

bot = telebot.TeleBot(token)
kb = types.ReplyKeyboardMarkup(row_width=2)
btn1 = types.KeyboardButton('/url')
btn2 = types.KeyboardButton('/help')
btn3 = types.KeyboardButton('как дела?')
kb.add(btn1, btn2, btn3)


@bot.message_handler(commands=['start'])
def start_message(message):
    print(message.chat.id)
    bot.send_message(message.chat.id,
                     'Привет, я запущен и буду попугайничать',
                     reply_markup=kb
                     )


@bot.message_handler(content_types=['text'])
def carrot(message):
    bot.send_message(message.chat.id, message.text)


# @bot.message_handler(content_types=['text'])
# def autoreply(message):
#     if message.text == 'Привет'.lower():
#         bot.send_message(message.chat.id, 'Здорово!')
#     elif message.text == 'Пока':
#         bot.send_message(message.chat.id, 'До скорого')
#     else:
#         bot.send_message(message.chat.id, 'Такие дела...')


# виды клавиатуры: inline kelyboard да reply keyboard

@bot.message_handler(commands=['help'])
def help_mes(message):
    bot.send_message(message.chat.id, "очень простой автоответчик")


@bot.message_handler(commands=['ulr'])
def url_mes(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="сайтец Яндекса", url="https://ya.ru")
    markup.add(btn)
    bot.send_message(message.chat.id, "сайтик", reply_markup=markup)

# теперь колбэк
@bot.callback_query_handler(content_types=['text'])
def callback_handler(message):
    if message.text == 'Привет'.lower():
        bot.send_message(message.chat.id, 'Здорово!')
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'До скорого')
    elif message.text == 'Как дела?'.lower():
        # bot.send_message(message.chat.id, '👍')
        answer = types.InlineKeyboardMarkup(row_width=2)
        btn_good = types.InlineKeyboardButton(text="Ништяк!", callback_data="good")
        btn_bad = types.InlineKeyboardButton(text="Ацтой!", callback_data="bad")
        answer.add(btn_good, btn_bad)
        bot.send_message(message.chat.id, "У меня нормас, а у тебя?", reply_markup=answer)

    else:
        bot.send_message(message.chat.id, 'Такие дела... ' + message.text)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "good":
        bot.send_message(call.message.chat.id, '👍 рад за тебя')
    elif call.data == "bad":
        bot.send_message(call.message.chat.id, '👎 собственно не переживай')

# итак, как же отправить в этого бота весточку с сайта?


bot.infinity_polling(none_stop=True)
