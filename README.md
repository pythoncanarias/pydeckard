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

After installation, the next step is to create the .env configuration file and the file for automatic program 
startup. 
During the process, you will be asked to enter your Telegram token and will be prompted with other 
configuration-related questions. The only required item is the Telegram token.
To do this, run:

~~~console
$ python3 --setup
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
