# OVERVIEW

This app is aimed at integrating images and text sources as internet memes
to be presented to users, as well as to be saved on the server.
___________________________________________________________________________

# USER GUIDE

## INSTALLATION
Start by running `./venv/Scripts/activate` in cli from project root.
This will activate the project's virtual environment.
Then, run `pip install -r requirements.txt` from project root.
___________________________________________________________________________

## RUNNING

Start by running `python app.py` from project root.
The server will then be up and running.

#### There are multiple ways to generate a meme:
*Browser Form*:

URI - `localhost:5000/create`

The user can choose an image of their own by specifying its URL, 
as well as manually typing meme text and author.
---------------------------------------------------------------------------
*Command Line Interface*:

URI - `localhost:5000/cli`

The user can run the app from a cli, either by manually typing arguments, 
or letting the app to randomly choose an image and text, or a combination of both. 
For more information about available options, type
meme.py -h or meme.py --help from project root directory.
---------------------------------------------------------------------------
*Random*:

URI - `localhost:5000/`

The user can simply open the browser with the URI given above and generate a random meme, 
made from images and texts saved in _data.
---------------------------------------------------------------------------