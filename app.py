from aiogram import executor, types
from aiogram.dispatcher.filters import CommandStart
from aiogram.types.message import ContentTypes
from aiogram.utils.exceptions import TelegramAPIError
from loader import bot, dp, keyboard
from animals import AnimatedAnimal, ANIMAL_DICT, print_log
import time

# TODO: add documentation wherever is possible


async def send_animal(animal: AnimatedAnimal):
    try:
        await animal.message.answer_animation(animal.active_url, reply_markup=keyboard)

    except TelegramAPIError as e:
        print_log('Error', 'try_send_mp4')
        print_log('Connection error. Reconnecting...',
                  animal.chat.first_name)
        time.sleep(5)
        send_animal(animal)


@dp.message_handler(CommandStart())
async def start_message(message: types.Message):
    unswer = f'Привет, {message.chat.first_name}! Хочешь получить пёсика?'
    print_log('Start', message.chat.first_name)
    await message.answer(unswer, reply_markup=keyboard)


@dp.message_handler(content_types=ContentTypes.TEXT)
async def get_message(message: types.Message):
    try:
        animal_type = ANIMAL_DICT[message.text]
    except KeyError:
        await start_message(message)
    else:
        print_log(animal_type[0], message.chat.first_name)
        unswer = AnimatedAnimal(animal_type, message)
        await send_animal(unswer)
        del unswer

if __name__ == '__main__':
    executor.start_polling(dp)
