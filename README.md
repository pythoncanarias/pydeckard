# PyDeckard

Telegram Bot made in Python to automate different tasks of [Python Canarias](http://pythoncanarias.es).

![RickDeckard](http://www.fantascienza.com/imgbank/thumb200/NEWS/rick-deckard.jpg) 

> "I've seen things you people wouldn't believe"  
> In honour of Rick Deckard from Blade Runner.

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
