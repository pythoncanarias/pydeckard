# PyDeckard

Telegram Bot made in Python to automate different tasks of [Python Canarias](http://pythoncanarias.es).

![RickDeckard](rick-deckard.jpg) 

> "I've seen things you people wouldn't believe"  
> In honour of Rick Deckard from Blade Runner.

## Installation

Create a virtualenv for Python3 and install bot.

~~~console
$ python3 -m venv /path/to/new/virtual/environment
$ cd /path/to/new/virtual/environment
$ source ./bin/activate
$ ./bin/pip3 install git+https://github.com/pythoncanarias/pydeckard.git
~~~

As a developer, you must install it in this other way:

~~~console
$ git clone https://github.com/pythoncanarias/pydeckard.git
$ cd pydeckard
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip3 install -e .[dev]
~~~

Next step is to set your bot token for development.
In the same directory where bot.py lives, you must create the .env file using the following command:

~~~console
$ echo 'TELEGRAM_BOT_TOKEN = "<token of your dev bot>"' > .env
~~~

Now you can launch the bot with:

~~~console
$ python3 bot.py
~~~

You can use the flag `--verbose` (or `-v') to get more information in rhe console:

~~~console
$ python3 bot.py --verbose
~~~


## Tests

Use pytest:

~~~console
$ python3 -m pytest
~~~
