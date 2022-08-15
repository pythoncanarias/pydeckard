"""
# Tarifa luz bot

Command to get spanish light prices.

## Docs

* API: https://api.preciodelaluz.org
"""

import csv
import datetime
import logging
from os import linesep

import requests
import telegram
from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

import settings
import utils

logger = logging.getLogger('bot')


def __get_price(data: dict) -> str:
    return f"**{data.get('hour', '')}**: {data.get('price', '')} {data.get('units', '')}."


def __get_price_data_from_file(file_reader, message=None) -> [str]:
    if not message:
        message = []

    for row in file_reader:
        message.append(row[0])

    return message


def __update_cache_file_with_cheapest(date_str: str) -> bool:
    number_of_prices = 3
    api_url = f'https://api.preciodelaluz.org/v1/prices/cheapests?zone=PCB&n={number_of_prices}'

    with open('today.csv', 'w') as csvfile:
        file_write = csv.writer(csvfile)
        msg_write = [[date_str]]

        result = requests.get(api_url)
        data_json = result.json()

        for element in data_json:
            msg_write.append([__get_price(element)])

        file_write.writerows(msg_write)
    return True


def command_cheapest(update, context):
    logger.info('Bot asked to execute /cheapest command')
    utc_now = datetime.datetime.utcnow()
    date_str = utc_now.strftime('%d/%m/%Y')

    try:
        with open('today.csv') as csvfile:
            file_read = csv.reader(csvfile)
            file_date = next(file_read)[0]
            msg = [f"**Hoy {file_date}**"]

            if file_date == date_str:
                msg = __get_price_data_from_file(file_reader=file_read)
            else:
                raise FileNotFoundError
    except FileNotFoundError:
        __update_cache_file_with_cheapest(date_str)

        with open('today.csv') as csvfile:
            file_read = csv.reader(csvfile)
            file_date = next(file_read)[0]
            msg = [f"**Hoy {file_date}**"]  # ignore first line
            msg = __get_price_data_from_file(file_reader=file_read, message=msg)

    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f"{linesep}".join(msg),
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def command_help(update, context):
    logger.info('Received command /help')
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Comandos disponibles:\n"
             " - /start - Comienza a interactuar con el bot\n"
             " - /help - Mostrar las interacciones disponibles\n"
             " - /status - Mostrar el estado del bot\n"
    )


def command_start(update, context):
    logger.info('Received command /start')
    context.bot.send_message(chat_id=update.message.chat_id, text=settings.BOT_GREETING)


def command_status(update, context):
    logger.info('bot asked to execute /status command')
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Status is OK, running since {utils.since()}',
    )


def welcome(update: Update, context):
    logger.info('Received new user event')
    new_member = update.message.new_chat_members[0]
    msg = f"Hola {new_member.name}!! " \
          "Escriba /help para ver los comando disponibles." \
          "También puede escribir /cheapest para ver las 3 horas más baratas del día"

    if msg:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=msg,
            parse_mode=telegram.ParseMode.HTML
        )


def reply(update, context):
    if not settings.bot_replies_enabled():
        return

    msg = update.message.text
    reply_spec = utils.triggers_reply(msg) if msg else None
    if reply_spec is not None:
        logger.info(f'bot sends reply {reply_spec.reply}')
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=reply_spec.reply
        )


def main():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
    )
    logger.info('Starting bot...')
    updater = Updater(settings.BOT_TOKEN)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(CommandHandler('help', command_help))
    dp.add_handler(CommandHandler('status', command_status))
    dp.add_handler(CommandHandler('cheapest', command_cheapest))
    # Welcome msg
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                  welcome, run_async=True))
    dp.add_handler(MessageHandler(Filters.chat_type.groups, reply))

    logger.info('Bot is ready')
    updater.start_polling(poll_interval=settings.POLL_INTERVAL)
    updater.idle()


if __name__ == "__main__":
    main()
