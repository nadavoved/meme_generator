"""Meme generation module to be run from a cli.

For additional information, run python meme.py -h or --help.
"""
import argparse
from utilities import MemeEngine


def get_description() -> str:
    """Return the project's description."""
    with open('README.md') as fp:
        return fp.read()


me = MemeEngine.MemeEngine('default_meme_archive')
parser = argparse.ArgumentParser(
    description=get_description(),
    formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--path', help='Path to a resource image file.'
                    ' Default is random.')
parser.add_argument('--body', help="Text content body."
                    " Default is random.")
parser.add_argument('--author', help='Text content author.'
                    ' Required if body is specified.Default is random.')
parser.add_argument('--width', help='Meme\'s width.'
                    ' Height will be in proportion to it.'
                    ' Default is 500px.')
parser.add_argument('--text_size', help='Meme\'s text content font size.'
                    ' Default is 30.')
args = parser.parse_args().__dict__
me.make_meme(**args)
