"""Contain MemeEngine class."""
from pathlib import Path
from os import mkdir
import random
from textwrap import fill

from PIL import Image, ImageFont, ImageDraw

from .Ingestory import Ingestor
from .Quote_Model import QuoteModel


class MemeEngine:
    """A class dedicated to register new memes to a given directory."""

    def __init__(self, static_folder):
        """Construct a meme generator referencing to an output directory.

        :param static_folder - (Path) directory of
        memes produced by the engine.
        """
        self.dir = Path(static_folder)
        if not self.dir.exists():
            mkdir(path=self.dir)

    @property
    def index(self):
        """Return the current index of the MemeEngine object."""
        with open('./utilities/meme_index') as fp:
            res = int(fp.read())
        with open('./utilities/meme_index', mode='w') as fp:
            fp.write(str(res + 1))
        return res

    def make_meme(self, width=None, text_size=None,
                  path=None, body=None, author=None) -> Path:
        """Generate and save a meme by given parameters.

        Return its filepath.
        Meme can also be made by randomly selecting an image and quote,
        if those are not given.
        :param path: (str) a path to an image file.
        :param body: (str) a body.
        :param author: (str) an author name.
        :param width: (int) width of saved meme.
        :param text_size: (int) text size within saved meme.
        :return: A filepath of the generated meme.
        """
        if text_size is None:
            text_size = 30
        if width is None:
            width = 500
        elif width > 500:
            raise ValueError('Required width must not be greater than 500!')
        if path is None:
            dog_images_dir = Path("./_data/photos/dog/")
            image_file_lst = [item for item in dog_images_dir.glob('*')
                              if item.suffix in ('.jpg', '.png')]
            img_file = random.choice(image_file_lst)
        else:
            img_file = Path(path)

        if body is None:
            quotes_dir = Path('./_data/DogQuotes/')
            quote_file_lst = [item for item in quotes_dir.glob('*')
                              if item.is_file()]
            quote_lst = []
            for file in quote_file_lst:
                try:
                    content = Ingestor.parse(file)
                except TypeError:
                    continue
                quote_lst += content
            quote = random.choice(quote_lst)
        else:
            if author in (None, ''):
                raise TypeError('Author Required if Body is Used')
            quote = QuoteModel(body, author)
        return self.finalize_meme(img_path=img_file, text=quote.body,
                                  author=quote.author, width=width,
                                  text_size=text_size)

    def finalize_meme(self, img_path, text: str,
                      author: str, width, text_size) -> Path:
        """Add a new meme to the directory referenced by the object.

        :param img_path: (str or Path) an image input's filepath.
        :param text: (str) the meme's text content body.
        :param author: (str) the meme's text content author name.
        :param width: (int) meme's width
        :param text_size: (int) meme's text's font size.
        :return: meme's absolute filepath.
        """
        img_path = Path(img_path)
        content = f'{text}\n- {author}'
        filename = f'{self.index}.jpg'
        path = self.dir / filename
        font_path = Path('./_data/Fonts/BerkshireSwash-Regular.ttf')
        with Image.open(fp=img_path) as img:
            output = resize(img, width)
            draw_text(output, font_path, text_size, content)
            output.save(fp=path)
        return path


def resize(img: Image, width):
    """Return a resized image."""
    ratio = width / img.width
    dim = (width, int(img.height * ratio))
    return img.resize(dim)


def draw_text(output: Image, font_path, text_size, content):
    """Draw text On a given image."""
    draw = ImageDraw.Draw(im=output)
    font = ImageFont.truetype(font=str(font_path), size=text_size)
    text_loc = 0, output.height * 5 // 8
    wrapped_text = wrap_text(output, font=font, content=content)
    draw.text(xy=text_loc, font=font, text=wrapped_text)


def wrap_text(img: Image, font: ImageFont.FreeTypeFont, content: str):
    """Wrap text to fit image dimensions."""
    true_text = content.replace('\n', '')
    ttl_length = font.getlength(true_text)
    avg_char_size = ttl_length / len(true_text)
    max_line_len = int((img.width * .9) / avg_char_size)
    return fill(text=content, width=max_line_len)
