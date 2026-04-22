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

As a developer, you must install it in this other way:

~~~console
$ ./bin/pip install git+https://github.com/misanram/pydeckard.git@Instalar-desde-GitHub[dev]
~~~

After installation, the next step is to create the .env configuration file and
the file for automatic program startup. 

During the process, you will be asked to enter your Telegram token and
will be prompted with other configuration-related questions. The only required
item is the Telegram token.

To do this, activate the virtual environment and run:

~~~console
$ pydeckard --setup
~~~

You can now launch the bot, activating the virtual environment and running::

~~~console
$ pydeckard
~~~

.. or delegate the startup of the application to your operating system
using the instructions that setup has provided.

You can view the bot log using:

~~~console
$ journalctl -u pydeckard.service -f systemd
~~~

You can use the flag `--verbose` (or `-v') to get more information in the console:

~~~console
$ python3 bot.py --verbose
~~~


## Tests

Use pytest:

~~~console
$ python3 -m pytest
~~~