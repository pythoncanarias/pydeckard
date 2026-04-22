#!/usr/bin/env python

import datetime

import pytest
from freezegun import freeze_time

from pydeckard.utils import validate_input, since


@freeze_time("2019-05-16 13:35:16")
def test_since_second():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "1 second"


@freeze_time("2019-05-16 13:35:21")
def test_since_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "6 seconds"


@freeze_time("2019-05-16 13:36:21")
def test_since_minute_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "1 minute 6 seconds"


@freeze_time("2019-05-16 13:37:21")
def test_since_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "2 minutes 6 seconds"


@freeze_time("2019-05-16 14:37:21")
def test_since_hour_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "1 hour 2 minutes 6 seconds"


@freeze_time("2019-05-16 15:37:21")
def test_since_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "2 hours 2 minutes 6 seconds"


@freeze_time("2019-05-17 15:37:21")
def test_since_day_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "1 day 2 hours 2 minutes 6 seconds"


@freeze_time("2019-05-19 15:37:21")
def test_since_days_hours_and_minutes_and_seconds():
    ref = datetime.datetime(2019, 5, 16, 13, 35, 15)
    assert since(ref) == "3 days 2 hours 2 minutes 6 seconds"


def test_tipo_none0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', None, None) is None


def test_tipo_none1(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1')

    assert validate_input('Dato', None, None) is None


def test_tipo_none2(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1.0')

    assert validate_input('Dato', None, None) is None


def test_tipo_none3(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'Texto')

    assert validate_input('Dato', None, None) is None


def test_tipo_texto0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', None, str) is None


def test_tipo_texto1(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1')

    assert validate_input('Dato', None, str) == '1'


def test_tipo_texto2(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1.0')

    assert validate_input('Dato', None, str) == '1.0'


def test_tipo_texto3(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'Texto')

    assert validate_input('Dato', None, str) == 'Texto'


def test_tipo_int0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', None, int) is None


def test_tipo_int1(monkeypatch):
    # Decimal
    monkeypatch.setattr('builtins.input', lambda _: '1')

    assert validate_input('Dato', None, int) == 1


def test_tipo_int2(monkeypatch):
    # Octal
    monkeypatch.setattr('builtins.input', lambda _: '0o10')

    assert validate_input('Dato', None, int) == 8


def test_tipo_int3(monkeypatch):
    # Hexadecimal
    monkeypatch.setattr('builtins.input', lambda _: '0xff')

    assert validate_input('Dato', None, int) == 255


def test_tipo_int4(monkeypatch):
    # Binario
    monkeypatch.setattr('builtins.input', lambda _: '0b11')

    assert validate_input('Dato', None, int) == 3

    def test_tipo_int5(monkeypatch):
    # Separador _
    monkeypatch.setattr('builtins.input', lambda _: '1_000_000')

    assert validate_input('Dato', None, int) == 1000000


def test_tipo_int6(monkeypatch):
    # Cero negativo
    monkeypatch.setattr('builtins.input', lambda _: '-0')

    assert validate_input('Dato', None, int) == 0


def test_tipo_int7(monkeypatch):
    # Decimal con espacios
    monkeypatch.setattr('builtins.input', lambda _: '    10     ')

    assert validate_input('Dato', None, int) == 10

    def test_tipo_int8(monkeypatch):
    # Hexadecimal con espacios
    monkeypatch.setattr('builtins.input', lambda _: '    0xff    ')

    assert validate_input('Dato', None, int) == 255

    
def test_tipo_int15(monkeypatch, capsys):
    # Float
    entradas = iter(['1.0', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', None, int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado == 1


def test_tipo_int16(monkeypatch, capsys):
    # Texto
    entradas = iter(['Texto', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', None, int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado == 1


def test_tipo_float0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', None, float) is None


def test_tipo_float1(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1')

    assert validate_input('Dato', None, float) == 1.0


def test_tipo_float2(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '1.0')

    assert validate_input('Dato', None, float) == 1.0


def test_tipo_float3(monkeypatch, capsys):
    entradas = iter(['Texto', '1.0'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', None, float)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo float' in imprime
    assert resultado == 1.0


def test_tipo_float4(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '-0.0')

    assert validate_input('Dato', None, float) == -0.0


def test_rango_tipo_int0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', (0, 1), int) is None


def test_rango_tipo_int1(monkeypatch):
    # En rango entero
    monkeypatch.setattr('builtins.input', lambda _: '1')

    assert validate_input('Dato', (0, 10), int) == 1


def test_rango_tipo_int2(monkeypatch, capsys):
    # Fuera de rango entero
    entradas = iter(['20', '-2', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', (0, 10), int)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe estar entre 0 y 10' in imprime
    assert resultado == 1


def test_rango_tipo_int3(monkeypatch, capsys):
    # En rango float
    entradas = iter(['5.0', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', (0, 10), int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado == 1


def test_rango_tipo_int4(monkeypatch, capsys):
    # Fuera de rango float
    entradas = iter(['20.0', '-1.0', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', (0, 10), int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado == 1


def test_rango_tipo_int5(monkeypatch, capsys):
    # Texto
    entradas = iter(['texto', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', (0, 10), int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado == 1


def test_rango_tipo_float0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', (0.0, 1.0), float) is None


def test_rango_tipo_float1(monkeypatch):
    # En rango entero
    monkeypatch.setattr('builtins.input', lambda _: '1')

    assert validate_input('Dato', (0.0, 1.0), float) == 1.0


def test_rango_tipo_float2(monkeypatch, capsys):
    # Fuera de rango entero
    entradas = iter(['2', '-2','1.0'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', (0.0, 1.0), float)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe estar entre 0.0 y 1.0' in imprime
    assert resultado == 1.0


def test_rango_tipo_float3(monkeypatch):
    # En rango float
    monkeypatch.setattr('builtins.input', lambda _: '1.0')

    assert validate_input('Dato', (0.0, 1.0), float) == 1.0


def test_rango_tipo_float4(monkeypatch, capsys):
    # Fuera de rango float
    entradas = iter(['2.0', '-1.0', '1.0'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', (0.0, 1.0), float)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe estar entre 0.0 y 1.0' in imprime
    assert resultado == 1.0


def test_rango_tipo_float5(monkeypatch, capsys):
    # Texto
    entradas = iter(['texto', '1.0'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', (0.0, 1.0), float)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo float' in imprime
    assert resultado == 1.0


def test_option_tipo_int0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', [-2, -1, 0, 1, 2, 3], int) is None


def test_option_tipo_int1(monkeypatch):
    # En lista entero
    monkeypatch.setattr('builtins.input', lambda _: '1')

    assert validate_input('Dato', [-2, -1, 0, 1, 2, 3], int) == 1


def test_option_tipo_int2(monkeypatch, capsys):
    # Fuera de lista entero
    entradas = iter(['20', '-23', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', [-2, -1, 0, 1, 2, 3], int)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe ser una de estas opciones: -2/-1/0/1/2/3' in imprime
    assert resultado == 1


def test_option_tipo_int4(monkeypatch, capsys):
    # Fuera de lista float
    entradas = iter(['20.0', '-10.0', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', [-2, -1, 0, 1, 2, 3], int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado == 1


def test_option_tipo_int5(monkeypatch, capsys):
    # Texto
    entradas = iter(['texto', '1'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', [-2, -1, 0, 1, 2, 3], int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado == 1


def test_option_tipo_int6(monkeypatch, capsys):
    # En lista vacia entero
    entradas = iter(['texto', ''])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', [], int)
    imprime = capsys.readouterr().out

    assert 'El valor debe ser de tipo int' in imprime
    assert resultado is None


def test_option_tipo_texto0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '')

    assert validate_input('Dato', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str) is None


def test_option_tipo_texto1(monkeypatch, capsys):
    # Entero
    entradas = iter(['20', 'DEBUG'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe ser una de estas opciones: DEBUG/INFO/WARNING/ERROR' in imprime
    assert resultado == 'DEBUG'


def test_option_tipo_texto2(monkeypatch, capsys):
    # float
    entradas = iter(['20.0', 'DEBUG'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe ser una de estas opciones: DEBUG/INFO/WARNING/ERROR' in imprime
    assert resultado == 'DEBUG'


def test_option_tipo_texto3(monkeypatch, capsys):
    # Fuera de lista texto
    entradas = iter(['HOLA', 'DEBUG'])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe ser una de estas opciones: DEBUG/INFO/WARNING/ERROR' in imprime
    assert resultado == 'DEBUG'


def test_option_tipo_texto4(monkeypatch):
    # Texto
    monkeypatch.setattr('builtins.input', lambda _: 'DEBUG')

    assert validate_input('Dato', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str) == 'DEBUG'


def test_option_tipo_texto5(monkeypatch):
    # Texto minúscula
    monkeypatch.setattr('builtins.input', lambda _: 'debug')

    assert validate_input('Dato', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str) == 'DEBUG'


def test_option_tipo_texto6(monkeypatch):
    # Texto mezcla minúsculas
    monkeypatch.setattr('builtins.input', lambda _: 'DebuG')

    assert validate_input('Dato', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], str) == 'DEBUG'


def test_option_tipo_texto7(monkeypatch, capsys):
    # En lista vacia texto
    entradas = iter(['texto', ''])
    monkeypatch.setattr("builtins.input", lambda _: next(entradas))

    resultado = validate_input('Dato', [], str)
    imprime = capsys.readouterr().out

    assert 'Error: El valor debe ser una de estas opciones: ' in imprime
    assert resultado is None


def test_tipo_raro0(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'texto')

    assert validate_input('Dato', None, bool) is None


def test_tipo_raro1(monkeypatch):
    # Tipo no callable
    monkeypatch.setattr('builtins.input', lambda _: 'texto')

    assert validate_input('Dato', None, object()) is None


if __name__ == "__main__":
    pytest.main()
