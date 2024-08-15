# PyDeckard

Telegram Bot made in Python to automate different tasks of [Python Canarias](http://pythoncanarias.es).

![RickDeckard](rick-deckard.jpg) 

> "I've seen things you people wouldn't believe"  
> In honour of Rick Deckard from Blade Runner.

## Installation

Create a virtualenv for Python3 and install dependencies. In this
example we are using pyenv:

~~~console
$ pyenv virtualenv 3.12.4 pydeckard
$ pyenv activate pydeckard
$ pip install -r requirements.txt
~~~

A developer needs to install a few more packages:

~~~console
$ pip install -r dev-requirements.txt
~~~

Next step is to set your bot token for development:

~~~console
$ echo 'TELEGRAM_BOT_TOKEN = "<token of your dev bot>"' > .env
~~~

Now you can launch the bot with:

~~~console
$ python bot.py
~~~

You can use the flag `--verbose` (or `-v') to get more information in rhe console:

~~~console
$ python bot.py --verbose
~~~


## Tests

Use pytest:

~~~console
$ python -m pytest
~~~
