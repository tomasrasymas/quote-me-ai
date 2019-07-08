import os
import requests
import tempfile
import shutil
from src.image_text import ImageText
from config import get_config
import random
import datetime


config = get_config()


class Image:
    def __init__(self, url, fonts_path=config.FONTS_PATH):
        self.url = url
        self.place = config.IMAGE_TEXT_PLACES
        self.fonts = [os.path.abspath(os.path.join(fonts_path, f)) for f in os.listdir(fonts_path) if f.endswith('.ttf')]
        self.xy = config.IMAGE_TEXT_XY_PAIRS
        self.image = self.__get_image_from_url(url=url)

    def __get_image_from_url(self, url):
        tmp_file = tempfile.NamedTemporaryFile()
        response = requests.get(url=url, stream=True)
        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, tmp_file)
        image = ImageText(filename_or_size=tmp_file.name)
        tmp_file.close()

        return image

    def draw_text(self, text):
        xy = random.choice(self.xy)
        font = random.choice(self.fonts)
        self.image.fill_text_box(xy,
                                 text,
                                 box_width=self.image.size[0] - xy[0] - config.IMAGE_TEXT_PAD_WIDTH,
                                 box_height=self.image.size[1] - xy[1] - config.IMAGE_TEXT_PAD_HEIGHT,
                                 font_filename=font,
                                 color=config.IMAGE_TEXT_COLOR,
                                 place=random.choice(self.place))

    def save(self, file_path):
        if not os.path.isdir(file_path):
            os.makedirs(file_path)

        file_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        file_path = os.path.join(file_path, file_name + '.png')
        self.image.save(file_path)
        return file_path


if __name__ == '__main__':
    i = Image(url='https://unsplash.com/photos/OzKgJ5BP5vU/download', fonts_path='../fonts')
    i.draw_text('Labas mano vardas yra Tomas. Kaip jums sekasi? Gal norit isgirsti kokia nors patarle?')
    i.save(file_path='')