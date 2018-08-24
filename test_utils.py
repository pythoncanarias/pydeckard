from unittest.mock import Mock
import pytest
import utils


# testing is_chinesse


def test_all_chars_under_255_must_pass():
    for _ in range(32, 256):
        c = chr(_)
        assert utils.is_chinesse(c) is False


def test_spanish():
    for c in 'áéíóúüñçÁÉÍÓÚÜÑÇ':
        assert utils.is_chinesse(c) is False


def test_french():
    for c in 'áàâéèêëîïóöúûæÆoOçÇ':
        assert utils.is_chinesse(c) is False


def test_german():
    for c in 'äüößÄÖÜẞ':
        assert utils.is_chinesse(c) is False


def test_chinesse_chars():
    sample = '同号电报社群增粉仅毛量大价优可指定群指定筛选条件及速度提'  \
        '供明细报表群发私发社区运营成品账号欢迎项目方交易所洽谈合作'  \
        '诚招全球代理'
    for c in sample:
        assert utils.is_chinesse(c) is True

# testing too_much_chinesse_letters

_VALID_NAMES = [
    'Miguel de Cervantes',
    'Diego Velázquez',
    'Penélope Cruz',
    'Pablo Picasso',
    'Clara Campoamor',
    'Amelia Earhart',
    'Rosa Parks',
    'Gloria Fuertes',
    'Salvador Martí',
    'Kung Fu 方',
    'Bruce Lee',
    ]

@pytest.fixture(scope='module', params=_VALID_NAMES)
def valid_name(request):
    return request.param

def test_names_valid(valid_name):
    assert utils.too_much_chinesse_chars(valid_name) is False


_INVALID_NAMES = [
    'Kung Fu 方方方',
    '电报 社群',
    '[VX.QQ同号253239090]电报社群增粉仅1毛,量大价优,可指定群指定筛选条件',
    '及速度,提供明细报表[群发私发][社区运营][成品账号]欢迎项目方交易所洽',
    '谈合作,诚招全球代理 ALL MARKET BEST PRICE FOR WORLDWIDE REAL',
    ]

@pytest.fixture(scope='module', params=_INVALID_NAMES)
def invalid_name(request):
    return request.param

def test_names_invalid(invalid_name):
    assert utils.too_much_chinesse_chars(invalid_name)


# testing is_bot


def test_is_not_bot():
    user = Mock(first_name='Paul Smith')
    assert not utils.is_bot(user)


def test_is_bot_real_sample():
    name = '[VX.QQ同号253239090]电报社群增粉仅1毛,量大价优,可指定群指定筛选条件'  \
        '及速度,提供明细报表[群发私发][社区运营][成品账号]欢迎项目方交易所洽'  \
        '谈合作,诚招全球代理 ALL MARKET BEST PRICE FOR WORLDWIDE REAL n ACTIVE'  \
        ' TELEGRAM GROUP(CHANNEL) HUMAN MEMBERS,QUALITY AND QUANTITY'  \
        ' GUARANTEED[Telegram:marvelwork/Email:smartelegram at outlook.com]'
    user = Mock(first_name=name)
    assert utils.is_bot(user)


if __name__ == '__main__':
    pytest.main()
