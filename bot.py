import csv
import datetime
import logging
from os import linesep

import telegram
from telegram import Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler

import scraper
import settings
import utils

logger = logging.getLogger('bot')


def command_start(update, context):
    logger.info('Received command /start')
    context.bot.send_message(chat_id=update.message.chat_id, text=settings.BOT_GREETING)


def command_help(update, context):
    logger.info('Received command /help')
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Available commands:\n"
        " - /start - start intereaction with the bot\n"
        " - /help - Show commands\n"
        " - /status - Show status and alive time\n"
        )


def command_status(update, context):
    logger.info('bot asked to execute /status commamd')
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Status is OK, running since {utils.since()}',
    )


def welcome(update: Update, context):
    logger.info('Received new user event')
    # new_member = update.message.new_chat_members[0]
    # msg = f"Welcome {new_member.name}!! " \
    #        "I am a friendly and polite *bot* 🤖"
    # msg = 'sefdgsdgf'

    # if msg:
    msg = []
    try:
        with open('today.csv') as csvfile:
            file_read = csv.reader(csvfile)
            for row in file_read:
                msg.append(','.join(row))
        # print(msg)
    except FileNotFoundError:
        pass
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN
    )

    with open('today.csv', 'w') as csvfile:
        file_write = csv.writer(csvfile, delimiter=linesep)
        utc_now = datetime.datetime.utcnow()
        file_write.writerow([
            utc_now.strftime('%Y/%m/%d'),
            utc_now.strftime('%H:%M:%S')
        ])

    # msg = scraper.sample()
    # print(msg)

    # context.bot.send_message(
    #     chat_id=update.message.chat_id,
    #     text=msg,
    #     parse_mode=telegram.ParseMode.HTML
    # )


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

    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(CommandHandler('help', command_help))
    dp.add_handler(CommandHandler('status', command_status))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                  welcome, run_async=True))
    dp.add_handler(MessageHandler(Filters.chat_type.groups, reply))

    logger.info('Bot is ready')
    updater.start_polling(poll_interval=settings.POLL_INTERVAL)
    updater.idle()


if __name__ == "__main__":
    # main()
    welcome(None, None)
