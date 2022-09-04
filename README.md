# PyDeckard

Telegram Bot made in Python to get Spain light rates.

![bot-pic](tari-luz-esp-bot.jpg) 

Image by [rawpixel.com on Freepik](https://www.freepik.com/free-vector/illustration-light-bulb-icon_3207916.htm).

## Installation

Create the virtualenv for Python3 and install dependencies with:

~~~console
$ pipenv install
~~~

Next step is to set your bot token for development:

~~~console
$ echo 'TELEGRAM_BOT_TOKEN = "<token of your dev bot>"' > .env
~~~

Now you can launch the bot with:

~~~console
$ python bot.py
~~~

## Tests

~~~console
$ pipenv install --dev
$ pytest
~~~
