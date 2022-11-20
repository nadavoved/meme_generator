"""The main Flask app of the project."""

import subprocess
import os
from datetime import datetime, timedelta

import PIL
import apscheduler.schedulers.background as bg
import requests
from flask import Flask, render_template, request
from flask_cachecontrol import dont_cache

from utilities.MemeEngine import MemeEngine

static = 'default_meme_archive'
temp = 'tmp'
app = Flask(__name__, static_folder=static)
eng = MemeEngine(static)


def rm(path):
    """Remove A file with the specified path."""
    os.remove(path=path)


def get_latest_meme():
    """Return the last generated meme."""
    return f'{static}/{eng.index - 1}.jpg'


@app.route('/')
@dont_cache()
def meme_rand():
    """Generate a random meme.

    NOTE-random memes won't be saved on server,
    and will be deleted shortly after served.
    """
    filename = eng.make_meme()
    sched = bg.BackgroundScheduler()
    ex_time = datetime.now() + timedelta(seconds=5)
    sched.add_job(func=rm, args=[filename], trigger='date',
                  run_date=ex_time)
    sched.start()
    return render_template('meme.html', path=filename)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
@dont_cache()
def meme_post():
    """Create a user defined meme."""
    data = request.form
    tmp_img = './tmp/tmp.jpg'
    try:
        web_img = requests.get(data['image_url']).content
    except requests.exceptions.MissingSchema:
        text = 'Please enter a valid image URL...'
        return render_template('error.html', error_msg=text)
    with open(tmp_img, 'wb') as fp:
        fp.write(web_img)
    try:
        path = eng.make_meme(path=tmp_img, body=data['body'],
                             author=data['author'])
    except PIL.UnidentifiedImageError:
        text = 'Please enter a valid image URL...'
        return render_template('error.html', error_msg=text)
    except TypeError:
        text = 'Please enter author for body...'
        return render_template('error.html', error_msg=text)
    finally:
        os.remove(tmp_img)
    return render_template('meme.html', path=path)


@app.route('/cli')
def meme_cli():
    """Information page about usage of cli.

    Will launch a cmd window, if running on Windows.
    """
    if os.name == 'nt':
        subprocess.run(['start', 'cmd.exe'], shell=True)
    return render_template('cli_info.html')


@app.route('/cli_res')
@dont_cache()
def meme_cli_result():
    """Page for viewing the output of running meme.py in cli."""
    return render_template('meme.html', path=get_latest_meme())


if __name__ == "__main__":
    app.run()
