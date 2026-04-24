import os
from random import choice
from telebot import TeleBot, types

TOKEN = '8122530905:AAHGeg-V29pc8lziHoxoa61kip2sSZHWZ7o'
bot = TeleBot(TOKEN)


@bot.message_handler(commands=['meme'])
def start(message):
    file = choice(os.listdir('images'))
    with open(f'images/{file}', 'rb') as f:
        bot.send_photo(message.chat.id, photo=f)


if __name__ == '__main__':
    bot.polling(none_stop=True)
