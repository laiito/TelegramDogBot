from aiogram.types.message import Message
import requests
import random
import time
from bs4 import BeautifulSoup

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


class AnimatedAnimal(object):

    def __init__(self, animal, message: Message):
        self.animal_string = animal[0]
        self.max_pages = animal[1]
        self.message = message
        self.set_url()

    def set_url(self):
        self.page_number = random.randint(1, self.max_pages)
        self.post_number = random.randint(0, 9)
        self.search_page_url = BASE_URL.format(
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
            if self.mp4_url_is_valid():
                self.active_url = self.mp4_url
            else:
                self.active_url = self.gif_url

    def mp4_url_is_valid(self):
        last_slash_pos = self.mp4_url.rfind('/')
        self.mp4_referer = self.mp4_url[:last_slash_pos+1]
        get_headers = {'Referer': self.mp4_referer}
        get_url = requests.head(self.mp4_url, headers=get_headers)
        if get_url.status_code == 200:
            return True
        else:
            return False


def print_log(command, name):
    # TODO: logging to file; adjust columns
    now = time.strftime("%d-%m-%Y %H:%M:%S", time.localtime())
    print(now + '	' + command + '	from	' + name)
