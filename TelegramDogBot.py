import telebot
import requests
import random
import time
from bs4 import BeautifulSoup
from mytoken import MY_TOKEN
"""
    Create 'mytoken.py' with your HTTP API access token, e.g.:
        MY_TOKEN = 'PLACE_YOUR_TOKEN_HERE'
"""
# TODO: add documentation wherever is possible

BASE_URL = ('http://joyreactor.cc/search/+/', '?tags=гифки%2C+')
ANIMAL_DICT = {
    'Хочу пёсу!': 'собака',
    'Хочу коту!': 'котэ'
    # TODO: add parrot
}


def get_mp4_url(animal):
    page_number = random.randint(1, 100)
    post_number = random.randint(0, 9)
    url = BASE_URL[0] + str(page_number) + BASE_URL[1] + animal
    contents = requests.get(url).text
    soup = BeautifulSoup(contents, 'lxml')
    post_list = soup.find_all('div', attrs={'class': 'postContainer'})
    post = post_list[post_number]
    a = post.find('a', attrs={'class': 'video_gif_source'})
    try:
        gif_link = a.attrs['href']
        mp4_link = gif_link.replace('/post/', '/post/mp4/', 1)
        mp4_link = mp4_link.replace('.gif', '.mp4')
        return mp4_link
    except:
        time.sleep(2)
        return get_mp4_url(animal)


def try_send(func, chat, unswer, keyboard):
    try:
        func_dict[func](chat.id, unswer, reply_markup=keyboard)
    except:
        print_log('Connection error. Reconnecting...', chat.first_name)
        time.sleep(5)
        try_send(func, chat, unswer, keyboard)


def print_log(command, name):
    # TODO: logging to file; adjust columns
    now = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    print(now + '	' + command + '	from	' + name)


bot = telebot.TeleBot(MY_TOKEN)
# TODO: Use 'types.InlineKeyboardMarkup' instead
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row(*ANIMAL_DICT)

func_dict = {
    'message': bot.send_message,
    'mp4': bot.send_animation,
    'photo': bot.send_photo  # not currently in use, left as an example
}


@bot.message_handler(commands=['start'])
def start_message(message):
    unswer = f'Привет, {message.chat.first_name}! Хочешь получить пёсика?'
    print_log('Start', message.chat.first_name)
    try_send('message', message.chat, unswer, keyboard)


@bot.message_handler(content_types=['text'])
def get_message(message):
    try:
        command = ANIMAL_DICT[message.text]
        url = get_mp4_url(command)
        print_log(command, message.chat.first_name)
        try_send('mp4', message.chat, url, keyboard)
    except KeyError:
        start_message(message)


bot.infinity_polling(True)
