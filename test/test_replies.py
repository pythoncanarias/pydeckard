import pytest

import config
import utils


@pytest.fixture()
def always_reply():
    """
    Make sure the bot always wants to reply, so we can test replies reliably
    """
    old_value = config.VERBOSITY
    config.VERBOSITY = 1

    yield

    config.VERBOSITY = old_value


def test_reply_is_on(always_reply):
    for i in range(1000000):
        assert utils.bot_wants_to_reply()


PYTHON_MESSAGES = [
    'Necesito ayuda con python, gracias',
    'Este es el grupo de piton Canarias',
    'Creo que piton esta mal escrito'
]


@pytest.mark.parametrize('python_message', PYTHON_MESSAGES)
def test_reply_with_python(always_reply, python_message):
    reply_spec = utils.triggers_reply(python_message)
    assert reply_spec.trigger in ('python', 'piton', 'piton')
    assert reply_spec.reply in config.THE_ZEN_OF_PYTHON


def test_long_answer(always_reply):
    message = 'He visto cosas'
    reply_spec = utils.triggers_reply(message)
    assert reply_spec.trigger == 'He visto'
    assert 'Es hora de morir' in reply_spec.reply


def test_java_reply(always_reply):
    message = 'Yo antes programaba java pero ya no'
    reply_spec = utils.triggers_reply(message)
    assert reply_spec.trigger == 'java'
    assert 'BIBA JABA' in reply_spec.reply
