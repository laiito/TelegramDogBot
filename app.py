from loader import *

# TODO: add documentation wherever is possible


def send_animal(animal):
    try:
        bot.send_animation(animal.chat.id, animal.active_url,
                           reply_markup=keyboard)
    except telebot.apihelper.ApiTelegramException as e:
        print_log('Error', 'try_send_mp4')
        print_log('Connection error. Reconnecting...',
                  animal.chat.first_name)
        time.sleep(5)
        send_animal(animal)


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
