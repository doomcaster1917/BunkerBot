import random
from vkbottle.bot import Bot, Message
from vkbottle.user import User
from vkbottle import UserAuth
from vkbottle import PhotoMessageUploader
import configparser
import json
import re
import asyncio

config = configparser.ConfigParser()

raw_images = {
    'general_carousel': ['raw_pictures/general_carousel/1.jpg', 'raw_pictures/general_carousel/2.jpg',
                         'raw_pictures/general_carousel/3.jpg'],
    'zalgo_settings': ['raw_pictures/zalgo_settings/1.jpg', 'raw_pictures/zalgo_settings/2.jpg',
                       'raw_pictures/zalgo_settings/3.jpg'],
    'pictures': ['raw_pictures/pictures/1.jpg', 'raw_pictures/pictures/2.jpg', 'raw_pictures/pictures/3.jpg', 'raw_pictures/pictures/4.jpg',
                 'raw_pictures/pictures/5.jpg', 'raw_pictures/pictures/6.jpg']
}

async def make_config():
    group_token = input("Введите токен паблика")
    while True:
        try:

            bot = Bot(token=group_token)

            for part, images in raw_images.items():

                with open(f"carousels/{part}.json", "r") as jsonFile:
                    data = json.load(jsonFile)

                    print(part, data['elements'][0]["photo_id"])
                    for num, item in enumerate(data['elements']):

                        item["photo_id"] = re.sub('photo', '', await PhotoMessageUploader(bot.api).upload(images[num]))

                with open(f"carousels/{part}.json", "w") as jsonFile:
                    json.dump(data, jsonFile)

                config['GROUP']['Token'] = group_token
                with open('config.ini', 'w') as configfile:

                    config.write(configfile)
                break
        except:
            time.sleep(5)
            print('Токен от группы невалидный. Возможно, в настройках группы для токена вы забыли что-то указать.'
                  'Прочитайте инструкцию заново и попробуйте создать новый токен.')

async def other_settings():
    while True:
        print("Вы можете ввести ввести логин/пароль своей дополнительной страницы. Она будет указана в поле <<Связаться с создателем>>, "
                         "от неё на вашу страницу будут приходить уведомления об ошибках. Этот метод бота не безопасен: vk.com запрещает использование"
                         "ботами обычных страниц: страница должна быть фейковая, потому что, попросту говоря, её могут забанить.")
        decision = input('Введите Да или Нет.')
        if decision == "Да":
            user_login = input("Введите логин. Чтобы отказаться, введите: Отказаться.")
            if user_login.lower() == 'Отказаться'.lower():
                break
            user_password = input("Введите id вашей страницы, на которую дополнительная страница будет слать уведомления."
                                  "Чтобы отказаться, введите: Отказаться.")
            if user_password.lower() == 'Отказаться'.lower():
                break
            admin_id = input("Введите пароль. Чтобы отказаться, введите: Отказаться.")
            if admin_id.lower() == 'Отказаться'.lower():
                break
            try:
                user_token = await UserAuth().get_token(user_login, user_password)
                user = User(token=user_token)
                await user.api.messages.send(peer_id=int(admin_id), message='Тестовое сообщение от бота',  random_id=random.randrange(100000000000000000))
                config['USER']['Token'] = user_token
                config['USER']['Login'] = user_login
                config['USER']['Password'] = user_password
                config['ADMIN']['Admin_id'] = admin_id
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                print('Авторизация прошла успешно.')
                break
            except:
                print('Логин или пароль неверные, либо боту не удалось написать вам, потому что у вас на главной странице закрыты сообщения.')

async def main():
    await make_config()
    await other_settings()


asyncio.run(main())

