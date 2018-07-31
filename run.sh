#!/bin/bash
# Master script.

cd "$(dirname "$0")"
exec pipenv run python bot.py
