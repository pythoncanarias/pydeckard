#!/bin/bash
# Master script.

cd "$(dirname "$0")"
source ~/.pyenv/versions/3.12.4/envs/pydeckard/bin/activate
exec python bot.py
