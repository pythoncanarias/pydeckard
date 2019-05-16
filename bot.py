import logging
import datetime

import telegram
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import Bot, Update

import config
import utils


def get_logger(name=__name__):
    if get_logger.logger is None:
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=config.LOG_LEVEL,
            )
        get_logger.logger = logging.getLogger(name)
    return get_logger.logger

get_logger.logger = None


def welcome(bot: Bot, update: Update):
    logger = get_logger()
    new_member = update.message.new_chat_members[0]
    logger.info(f'send welcome message for {new_member.name}')
    msg = None

    if new_member.is_bot:
        msg = f"{new_member.name} is a *bot*!! " \
              "-> It could be kindly removed 🗑"
    else:
        if utils.is_bot(new_member):
            bot.delete_message(update.message.chat_id,
                               update.message.message_id)
            if bot.kick_chat_member(update.message.chat_id, new_member.id):
                msg = (f"*{new_member.username}* has been banned because I "
                       "considered it was a bot. ")
        else:
            msg = f"Welcome {new_member.name}!! " \
                   "I am a friendly and polite *bot* 🤖"
    if msg:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=msg,
            parse_mode=telegram.ParseMode.MARKDOWN
        )


def reply(bot, update):
    logger = get_logger()
    if not config.bot_replies_enabled():
        return

    msg = update.message.text
    reply_spec = utils.triggers_reply(msg)
    if reply_spec is not None:
        logger.info(f'bot sends reply {reply_spec.reply}')
        bot.send_message(
            chat_id=update.message.chat_id,
            text=reply_spec.reply
        )


def since(reference=datetime.datetime.now()):
    now = datetime.datetime.now()
    delta = now - reference
    buff = []
    if delta.days:
        buff.append('{} days'.format(delta.days))
    hours = delta.seconds // 3600
    if hours > 0:
        buff.append('{} hours'.format(hours))
    minutes = delta.seconds // 60
    if minutes > 0:
        buff.append('{} minutes'.format(minutes))
    seconds = delta.seconds % 60
    buff.append('{} seconds'.format(seconds))
    return ' '.join(buff)


def status(bot, update):
    logger = get_logger()
    logger.info('bot asked to execute status commamd')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='Status is OK, running since {}'.format(since())
    )


def main():
    logger = get_logger()
    logger.info('Starting bot...')
    updater = Updater(config.TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.group, reply))
    dp.add_handler(CommandHandler('status', status))

    logger.info('Bot is ready')
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
