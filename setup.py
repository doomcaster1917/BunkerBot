from setuptools import setup
import asyncio
import configparser
import json
import re

config = configparser.ConfigParser()
config.read('config.ini')
group_token = config['GROUP']['Token']

setup(
   name='vk public bot',
   version='1.0',
   description='Make mems and zalgo-text from sent messages',
   author='Doomcaster1917',
   author_email='webtalestoday@gmail.com',
   #packages=['vk_searching_bot'],  #same as name
   install_requires=['vkbottle'], #external packages as dependencies
)

from vkbottle.bot import Bot

from vkbottle import PhotoMessageUploader
bot = Bot(token=group_token)

raw_images = {
    'general_carousel': ['raw_pictures/general_carousel/1.jpg', 'raw_pictures/general_carousel/2.jpg',
                         'raw_pictures/general_carousel/3.jpg'],
    'zalgo_settings': ['raw_pictures/zalgo_settings/1.jpg', 'raw_pictures/zalgo_settings/2.jpg',
                       'raw_pictures/zalgo_settings/3.jpg'],
    'pictures': ['raw_pictures/pictures/1.jpg', 'raw_pictures/pictures/2.jpg', 'raw_pictures/pictures/3.jpg', 'raw_pictures/pictures/4.jpg',
                 'raw_pictures/pictures/5.jpg', 'raw_pictures/pictures/6.jpg']
}

async def change():
    for part, images in raw_images.items():

        with open(f"carousels/{part}.json", "r") as jsonFile:
            data = json.load(jsonFile)

            print(part, data['elements'][0]["photo_id"])
            for num, item in enumerate(data['elements']):

                item["photo_id"] = re.sub('photo', '', await PhotoMessageUploader(bot.api).upload(images[num]))

        with open(f"carousels/{part}.json", "w") as jsonFile:
            json.dump(data, jsonFile)



asyncio.run(change())




