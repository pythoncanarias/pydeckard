#!/bin/bash
# Master script.

cd "$(dirname "$0")"
source ~/.virtualenvs/pydeckard/bin/activate
exec python bot.py
