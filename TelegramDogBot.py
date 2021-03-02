from __future__ import with_statement
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


class AnimatedAnimal(object):
    BASE_URL = 'http://joyreactor.cc/search/+/{0}?tags=гифки%2C+{1}'
    # ANIMAL_DICT = {
    #    emoji_code: (string_for_url, number_of_pages)
    #   }
    ANIMAL_DICT = {
        u'\U0001F436': ('собака', 100),  # dog
        u'\U0001F431': ('котэ', 100),    # cat
        u'\U0001f99c': ('попугай', 61),  # parrot
        u'\U0001F439': ('хомяк', 29)     # hamster
    }

    def __init__(self, animal, chat):
        self.animal_string = animal[0]
        self.max_pages = animal[1]
        self.chat = chat

    def set_url(self):
        self.page_number = random.randint(1, self.max_pages)
        self.post_number = random.randint(0, 9)
        self.search_page_url = AnimatedAnimal.BASE_URL.format(
            self.page_number, self.animal_string)

        contents = requests.get(self.search_page_url).text
        soup = BeautifulSoup(contents, 'lxml')
        post_list = soup.find_all('div', attrs={'class': 'postContainer'})
        post = post_list[self.post_number]
        try:
            a = post.find('a', attrs={'class': 'video_gif_source'})
            self.gif_url = a.attrs['href']
        except:
            print_log('Error', 'get_gif_url')
            time.sleep(2)
            self.get_url()
        else:
            self.mp4_url = self.gif_url.replace('/post/', '/post/mp4/', 1)
            self.mp4_url = self.mp4_url.replace('.gif', '.mp4')
            self.set_active_url(self.mp4_url)

    def mp4_url_is_valid(self):
        last_slash_pos = self.mp4_url.rfind('/')
        self.mp4_referer = self.mp4_url[:last_slash_pos+1]
        get_headers = {'Referer': self.mp4_referer}
        get_url = requests.head(self.mp4_url, headers=get_headers)
        if get_url.status_code == 200:
            return True
        else:
            return False

    def set_active_url(self, url):
        self.active_url = url

    def send(self):
        try:
            bot.send_animation(self.chat.id, self.active_url,
                               reply_markup=keyboard)
        except telebot.apihelper.ApiTelegramException as e:
            print_log('Error', 'try_send_mp4')
            print_log('Connection error. Reconnecting...',
                      self.chat.first_name)
            time.sleep(5)
            self.send()


def print_log(command, name):
    # TODO: logging to file; adjust columns
    now = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    print(now + '	' + command + '	from	' + name)


bot = telebot.TeleBot(MY_TOKEN)
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row(*AnimatedAnimal.ANIMAL_DICT)


@bot.message_handler(commands=['start'])
def start_message(message):
    unswer = f'Привет, {message.chat.first_name}! Хочешь получить пёсика?'
    print_log('Start', message.chat.first_name)
    bot.send_message(message.chat.id, unswer, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_message(message):
    try:
        animal = AnimatedAnimal.ANIMAL_DICT[message.text]
    except KeyError:
        start_message(message)
    else:
        print_log(animal[0], message.chat.first_name)
        unswer = AnimatedAnimal(animal, message.chat)
        unswer.set_url()
        if not unswer.mp4_url_is_valid():
            unswer.set_active_url(unswer.gif_url)
        unswer.send()
        del unswer


bot.infinity_polling(True)
