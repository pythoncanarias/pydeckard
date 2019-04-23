from unittest.mock import Mock
import pytest
import utils


# testing is_chinese

@pytest.mark.parametrize('char_num', range(32, 256))
def test_all_chars_under_255_must_pass(char_num):
        char = chr(char_num)
        assert not utils.is_chinese(char)


@pytest.mark.parametrize('spanish_char', 'áéíóúüñçÁÉÍÓÚÜÑÇ')
def test_spanish_chars(spanish_char):
    assert not utils.is_chinese(spanish_char)


@pytest.mark.parametrize('french_char', 'áàâéèêëîïóöúûæÆoOçÇ')
def test_french_chars(french_char):
    assert not utils.is_chinese(french_char)


@pytest.mark.parametrize('german_char', 'äüößÄÖÜẞ')
def test_german_chars(german_char):
    assert not utils.is_chinese(german_char)


@pytest.mark.parametrize('chinese_char', '同号电报社群增粉仅毛量大价优可指定群指定筛选条件及速度提'
                                         '供明细报表群发私发社区运营成品账号欢迎项目方交易所洽谈合作'
                                         '诚招全球代理')
def test_chinese_chars(chinese_char):
    assert utils.is_chinese(chinese_char)

# testing too_much_chinese_letters


VALID_NAMES = [
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


@pytest.mark.parametrize('valid_name', VALID_NAMES)
def test_names_without_many_chinese_chars(valid_name):
    assert not utils.too_much_chinese_chars(valid_name)


INVALID_NAMES = [
    'Kung Fu 方方方',
    '电报 社群',
    '[VX.QQ同号253239090]电报社群增粉仅1毛,量大价优,可指定群指定筛选条件',
    '及速度,提供明细报表[群发私发][社区运营][成品账号]欢迎项目方交易所洽',
    '谈合作,诚招全球代理 ALL MARKET BEST PRICE FOR WORLDWIDE REAL',
    ]


@pytest.mark.parametrize('invalid_name', INVALID_NAMES)
def test_names_with_too_many_chinese_chars(invalid_name):
    assert utils.too_much_chinese_chars(invalid_name)


# testing is_bot


def test_is_not_bot():
    user = Mock(first_name='Paul Smith')
    assert not utils.is_bot(user)


def test_is_bot_real_sample():
    name = ('[VX.QQ同号253239090]电报社群增粉仅1毛,量大价优,可指定群指定筛选条件'
            '及速度,提供明细报表[群发私发][社区运营][成品账号]欢迎项目方交易所洽'
            '谈合作,诚招全球代理 ALL MARKET BEST PRICE FOR WORLDWIDE REAL n ACTIVE'
            ' TELEGRAM GROUP(CHANNEL) HUMAN MEMBERS,QUALITY AND QUANTITY'
            ' GUARANTEED[Telegram:marvelwork/Email:smartelegram at outlook.com]')
    user = Mock(first_name=name)
    assert utils.is_bot(user)


# Testing is_tgmember_sect
TG_MEMBER_SECT_NAMES = [
    'tgMember.com +989216973112',
    'Random String tgmember.com',
    ]


@pytest.mark.parametrize('tgmember_name', TG_MEMBER_SECT_NAMES)
def test_is_tgmember_sect(tgmember_name):
    assert utils.is_tgmember_sect(tgmember_name)


@pytest.mark.parametrize('tgmember_name', TG_MEMBER_SECT_NAMES)
def test_is_tgmember_sect_real(tgmember_name):
    user = Mock(first_name=tgmember_name)
    assert utils.is_bot(user)


if __name__ == '__main__':
    pytest.main()
