# -*- coding: utf-8 -*-
import random
import datetime
import zalgo_hard
import json
import Mem_generator
import requests
import re
import configparser
from vkbottle.bot import Bot, Message
from vkbottle.user import User
import logging
from vkbottle.dispatch.rules.base import AttachmentTypeRule
from vkbottle.tools import PhotoMessageUploader
from vkbottle import UserAuth, VKAPIError
import threading
import asyncio
import concurrent.futures

config = configparser.ConfigParser()
config.read('config.ini')
group_token = config['GROUP']['Token']
if 'USER' in config and 'ADMIN' in config:
    user_token = config['USER']['Token']
    user_login = config['USER']['Login']
    user_password = config['USER']['Password']
    admin_id = config['ADMIN']['Admin_id']
    user = User(token=user_token)
else:
    user_token = None
    user_login = None
    user_password = None
    admin_id = None

bot = Bot(token=group_token)




@bot.on.message(AttachmentTypeRule("photo"))
async def take_picture(message: Message):
    try:
        start_time = datetime.datetime.now()
        photos = message.get_photo_attachments()
        photo_url = await taking_photo(photos)
        finished_photo = await make_mem(photo_url=photo_url, message=message.text)
        print(finished_photo)
        await message.answer(message='Готовый мем', attachment=finished_photo)

        delta = datetime.datetime.now() - start_time
        logger_info.info("\n" + f"Time of mem operation was {str(delta.microseconds)} and threading quantity are {threading.active_count()}")

        if int(delta.seconds) > 13:
            await message.answer(message='Возможно, сервер загружен. Мемы отправляются медленно.')
    except Exception as err:
        print(err)
        logger_errors.error(f'Произошла ошибка АПИ ВК {err}')
        await reply_of_author(admin_id, err)

@bot.on.message()
async def message_handler(message: Message):
        carousel_general, what_can_i_do_keyboard, zalgo_settings, \
        image_sizes, text_botton_and_top, zalgo_doesnt_work, zalgo_low, zalgo_mid, zalgo_high = carousels_and_keyboards()
        print(image_sizes, text_botton_and_top, zalgo_doesnt_work, zalgo_low, zalgo_mid, zalgo_high)

    # try:
        msg = message.text
        if msg == 'Что я умею?' or msg == 'Начать' or msg == 'начать':

            await message.answer(message = 'Пожалуйста', template= carousel_general)

        elif msg == 'Расширенные настройки zalgo':

            await message.answer(message = 'Пожалуйста', template=zalgo_settings)

        elif msg == 'Почему не работает zalgo?':

            await message.answer(message='Zalgo в сообщениях vk видно только с компьютера. Если бот прислал вам'
                                                 'текст, как на картинке, то, верноятно,'
                                                 'вы сидите с телефона или у вас операционная система Linux/Mac OS',
                                 attachment= zalgo_doesnt_work)

        elif msg == 'Текст сверху и снизу':

            await message.answer(message='Чтобы нарисовать текст сверху и снизу, введите текст в формате '
                                                                  '~Верх: текст сверху Низ: текст снизу~ , как это сделано на фото ниже',
                                        attachment= text_botton_and_top)

        elif msg == 'Ещё подробнее(low)':

            await message.answer(message= 'Введите, как в примере', attachment=zalgo_low)

        elif msg == 'Ещё подробнее(mid)':

            await message.answer(message= 'Введите, как в примере', attachment=zalgo_mid)

        elif msg == 'Ещё подробнее(high)':

            await message.answer(message= 'Введите, как в примере', attachment=zalgo_high)

        elif msg == 'Размер текста меняется?':

            await message.answer(message= 'Чем больше текста вы пишете боту, тем меньше становится размер шрифта.'
                                                 'Это позволяет делать мемы с большими текстами. Стоит упомянуть, что '
                                                 'также текст автоматически разбивается на строки. Ниже пример:',
                       attachment=image_sizes)

        elif msg == 'Связаться с создателем':
            if user_token:
                try:
                    await reply_of_author(message.peer_id, 'Приветствую вас, я создатель бота. '
                                                           'Напишите свой вопрос, а я отвечу вам, когда буду в сети.')
                    await message.answer(message= 'Создатель прислал вам сообщение, вы можете найти его ссылку в диалогах')
                except:
                    await message.answer(message='Возможно, что в настройках вашей страницы запрещены входящие сообщения. '
                                                           'Попробуйте разрешить сообщения и нажмите кнопку заново')
            else:
                await message.answer(message='Администратор пользователя не указал при установке бота страницу для связи.'
                                             'Страница же разработчика бота: https://vk.com/id661706483')
        else:
            zalgo_msg = await zalgo_handler(msg)
            await message.answer(message=zalgo_msg, keyboard=what_can_i_do_keyboard)

    # except Exception as err:
    #
    #     logger_errors.error(f'Error occurred{err}')
    #     await message.answer(message= 'У меня произошла ошибка. Ой, всё. Я ухожу и у меня месячные',
    #                keyboard= what_can_i_do_keyboard)




async def make_mem(photo_url, message):
    loop = asyncio.get_running_loop()
    image_content = requests.get(photo_url).content

    msg = message.upper()
    exp = r'ВЕРХ:'
    result_l = re.sub(exp, '', msg)
    exp = r'НИЗ:'
    result = re.split(exp, result_l)
    if len(result) == 2:
        top_text = result[0]
        bottom_text = result[1]
        with concurrent.futures.ThreadPoolExecutor() as pool:
            image = await loop.run_in_executor(pool,Mem_generator.makingMemes, *(image_content, top_text, bottom_text))


    else:

        with concurrent.futures.ThreadPoolExecutor() as pool:
            image = await loop.run_in_executor(pool, Mem_generator.makingMemes, *(image_content, '', result[0]))

    return await PhotoMessageUploader(bot.api).upload(image)


async def taking_photo(items: list):

    try:
        photos = items[0].sizes
        array_of_sizes = []
        for photo_num in range(len(photos)):
            size = photos[photo_num].height
            array_of_sizes.append(size)

        number = array_of_sizes.index(max(array_of_sizes))
        photo_url = photos[number].url


        return photo_url

    except:
        ...


def carousels_and_keyboards():
    with open('carousels/general_carousel.json') as car:
        carousel_general = car.read()#json.dumps(json.load(car))

    with open('carousels/zalgo_settings.json') as car:
        zalgo_settings = car.read() #json.dumps(json.load(car))

    with open('carousels/pictures.json') as pic:
        data = json.load(pic)
        image_sizes = f"photo{data['elements'][0]['photo_id']}"
        text_botton_and_top = f"photo{data['elements'][1]['photo_id']}"
        zalgo_doesnt_work = f"photo{data['elements'][2]['photo_id']}"
        zalgo_low = f"photo{data['elements'][3]['photo_id']}"
        zalgo_mid = f"photo{data['elements'][4]['photo_id']}"
        zalgo_high = f"photo{data['elements'][5]['photo_id']}"


    what_can_i_do_keyboard = {

   "buttons":[[
         {
            "action":{
               "type":"text",

               "label":"Что я умею?"
            },
            "color":"primary"
         }


      ]
   ]
}
    what_can_i_do_keyboard = json.dumps(what_can_i_do_keyboard)

    return carousel_general, what_can_i_do_keyboard, zalgo_settings, image_sizes, text_botton_and_top, zalgo_doesnt_work,\
           zalgo_low, zalgo_mid, zalgo_high


async def zalgo_handler(msg):


    msg = msg.lower()

    # Перебираем поступившее сообщение по регуляркам, вырезаем нужную регулярку
    arr_exp = [r'интенсивность низкая:', r'интенсивность средняя:', r'интенсивность высокая:']
    result_first = []
    for exp in arr_exp:
        result_first.append(re.findall(exp, msg))


    filtered_msg = []
    for exp in arr_exp:
        filtered_msg.append(re.sub(exp, '', msg))


    lenz = []
    for i in filtered_msg:
        lenz.append(len(i))
    filtered_msg = filtered_msg[lenz.index(min(lenz))]


    zalgo_intencity_msg = []
    for i in result_first:
        if i == []:
            continue
        else:
            zalgo_intencity_msg.append(i)


    isNotEmpty = []
    for i in result_first:
        if i:
            isNotEmpty.append(i)
        else:
            continue


    if isNotEmpty:
        if zalgo_intencity_msg[0][0] == 'интенсивность низкая:':
            zalgo_intencity = zalgo_hard.low_lvl
        elif zalgo_intencity_msg[0][0] == 'интенсивность средняя:':
            zalgo_intencity = zalgo_hard.midle_lvl
        elif zalgo_intencity_msg[0][0] == 'интенсивность высокая:':
            zalgo_intencity = zalgo_hard.hard_lvl
        else:
            zalgo_intencity = zalgo_hard.midle_lvl
    else:
        zalgo_intencity = zalgo_hard.midle_lvl

    zalgo_msg = zalgo_hard.zalgo_hard(filtered_msg, zalgo_intencity)

    if len(zalgo_msg) < 5107:
        return zalgo_msg
    else:
        too_many_chars_reply = ['придушить питона', 'купить молока', 'задеть индейку',
                                'обматерить программиста',
                                'избить батон', 'признать Соловьёва журналистом, но не испытать уныния']
        zalgo_msg = 'Вероятно, сообщение слишком длинное. Попробуйте {}, а затем уменьшите длину текста. ' \
                    'Учитывайте, что VK не принимает сообщения больше 5 тысяч знаков, а сообщения бота очень тяжеловесные'.format(
            random.choice(too_many_chars_reply))
        return zalgo_msg

async def reply_of_author(id, message):
    if user_token:
        try:
            await user.api.messages.send(peer_id=id, message=message, random_id=random.randrange(10000000000000000000000000000000))
        except VKAPIError as error:
            if error.code == 5:
                new_token = await UserAuth().get_token(login=user_login, password=user_password)
                usr = User(token=new_token)
                await usr.api.messages.send(peer_id=id, message=message,
                                             random_id=random.randrange(10000000000000000000000000000000))
                config['USER']['Token'] = user_token
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                logger_errors.error(f"Произошла ошибка авторизации {error}. Бот перелогинился.")
    else:
        pass

def write_logs(filename, name, level) -> logging.Logger:
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(filename)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


logger_errors = write_logs('bot_errors.log', 'errors', logging.ERROR)
logger_info = write_logs('bot_capacity.log', 'info', logging.INFO)



bot.run_forever()
