from PIL import Image, ImageDraw, ImageFont, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageText(object):
    def __init__(self, filename_or_size, mode='RGBA', background=(0, 0, 0, 0),
                 encoding='utf8'):
        if isinstance(filename_or_size, str):
            self.filename = filename_or_size
            self.image = Image.open(self.filename)
            self.initial_image = Image.open(self.filename)
            self.size = self.image.size
        elif isinstance(filename_or_size, (list, tuple)):
            self.size = filename_or_size
            self.image = Image.new(mode, self.size, color=background)
            self.initial_image = Image.new(mode, self.size, color=background)
            self.filename = None
        self.image = self.add_overlay(image=self.image)
        self.initial_image = self.add_overlay(image=self.initial_image)
        self.draw = ImageDraw.Draw(self.image)
        self.encoding = encoding

    def add_overlay(self, image, color=(0,0,0), alpha=0.4):
        overlay = Image.new(image.mode, image.size, color=color)
        overlay.convert(mode='RGBA')
        image.convert(mode='RGBA')

        blended = Image.blend(image, overlay, alpha=alpha)

        blended.convert(mode='RGB')

        return blended

    def reset_image(self):
        self.image = self.initial_image
        self.draw = ImageDraw.Draw(self.image)

    def save(self, filename=None):
        self.image.save(filename or self.filename)

    def get_image(self):
        return self.image

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
                (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                             text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
                    (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, xy, text, font_filename, font_size=11,
                   color=(0, 0, 0), max_width=None, max_height=None):
        x, y = xy
        if isinstance(text, str):
            try:
                text = text.decode(self.encoding)
            except Exception as e:
                pass
        if font_size == 'fill' and \
                (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def fill_text_box(self, xy, text, box_width, box_height, font_filename,
                      start_font_size=1, color=(0, 0, 0), place='left', lower_font_by=10):
        font_size = start_font_size
        while True:
            width, height, box_width = self.write_text_box(xy, text, box_width,
                                                           font_filename, font_size, color, place)

            if (width >= box_width) or (height >= box_height):
                font_size -= lower_font_by
                self.reset_image()
                self.write_text_box(xy, text, box_width,
                                    font_filename, font_size, color, place)
                break

            font_size += 1

        return (box_width, box_height)

    def write_text_box(self, xy, text, box_width, font_filename,
                       font_size=11, color=(0, 0, 0), place='left',
                       justify_last_line=False):
        x, y = xy

        lines = []
        line = []
        words = text.split()
        for word in words:
            new_line = ' '.join(line + [word])
            size = self.get_text_size(font_filename, font_size, new_line)
            text_height = size[1]
            if size[0] <= box_width:
                line.append(word)
            else:
                lines.append(line)
                line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines if line]

        height = y
        for index, line in enumerate(lines):
            if place == 'left':
                total_size = self.get_text_size(font_filename, font_size, line)
                self.write_text((x, height), line, font_filename, font_size,
                                color)
            elif place == 'right':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            elif place == 'center':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text((x_left, height), line, font_filename,
                                font_size, color)
            elif place == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or \
                        len(words) == 1:
                    self.write_text((x, height), line, font_filename, font_size,
                                    color)
                    continue
                line_without_spaces = ''.join(words)
                total_size = self.get_text_size(font_filename, font_size,
                                                line_without_spaces)
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text((start_x, height), word, font_filename,
                                    font_size, color)
                    word_size = self.get_text_size(font_filename, font_size,
                                                   word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size,
                                                    words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text((last_word_x, height), words[-1], font_filename,
                                font_size, color)
            height += text_height
        return (total_size[0], height - y, box_width)