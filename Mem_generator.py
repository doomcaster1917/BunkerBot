import textwrap
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import math

def makingMemes(image_content, top_text = '',bottom_text = ''):

    image = Image.open(BytesIO(image_content))
    draw = ImageDraw.Draw(image)
    image_width = image.size[0]
    image_height = image.size[1]
    pix = image.load()

    if len(bottom_text+top_text) > 22:
        bottom_area = 0.2*(image_height*image_width)
        letter_area = bottom_area/len(bottom_text+top_text)
        size = math.sqrt(1.9*letter_area)
    else:
        size = image_height/10

    font = ImageFont.truetype('impact/Impact.ttf', size=round(size))
    char_width, char_height = font.getsize('A')
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(top_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(bottom_text, width=chars_per_line)



    y = 10
    for line in top_lines:
        print(line)
        line_width, line_height = font.getsize(line)
        print(font.getsize(line))
        x = (image_width - line_width) / 2
        draw.text((x, y), line, stroke_width=3, stroke_fill='black', font=font)
        y += line_height

    y = image_height - char_height * len(bottom_lines) - 32

    for line in bottom_lines:
        line_width, line_height = font.getsize(line)

        x = (image_width - line_width) / 2
        draw.text((x, y), line, stroke_width=3, stroke_fill='black', font=font)
        y += line_height

    finished_image_content = BytesIO()

    image.save(finished_image_content, format='JPEG')


    finished_image_content.seek(0)
    finished_image_content.name = (
        '/home/barbus/Изображения/Снимки экрана/Снимок экрана от 2022-07-17 23-55-24.png'
    )


    return finished_image_content





