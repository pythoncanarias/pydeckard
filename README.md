# PyDeckard

Telegram Bot made in Python to automate different tasks of [Python Canarias](http://pythoncanarias.es).

![RickDeckard](rick-deckard.jpg) 

> "I've seen things you people wouldn't believe"  
> In honour of Rick Deckard from Blade Runner.

## Installation

Create a virtualenv for Python3 and install dependencies. In this
example we are using python -m venv:

~~~console
$ python -m venv pydeckard
$ cd pydeckard
$ source ./bin/activate
$ ./bin/pip install git+https://github.com/misanram/pydeckard.git@Instalar-desde-GitHub
~~~

A developer needs to install a few more packages:

~~~console
$ ./bin/pip install git+https://github.com/misanram/pydeckard.git@Instalar-desde-GitHub[dev]
~~~

Next step is to set your bot token for development:

~~~console
$ echo 'TELEGRAM_BOT_TOKEN = "<token of your dev bot>"' > .env
~~~

Now you can launch the bot with:

~~~console
$ python3 bot.py
~~~

~~~systemd





You can use the flag `--verbose` (or `-v') to get more information in the console:

~~~console
$ python3 bot.py --verbose
~~~


## Tests

Use pytest:

~~~console
$ python3 -m pytest
~~~
