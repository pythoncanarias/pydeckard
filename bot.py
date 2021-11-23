import logging
from time import sleep

import telegram
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import Update

import config
import utils


logger = logging.getLogger('bot')


def command_start(update, context):
    logger.info('Received command /start')
    context.bot.send_message(chat_id=update.message.chat_id, text=config.BOT_GREETING)


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
    new_member = update.message.new_chat_members[0]

    logger.info(f'Waiting {config.WELCOME_DELAY} seconds until user completes captcha...')
    sleep(config.WELCOME_DELAY)
    membership_info = context.bot.get_chat_member(update.message.chat_id, new_member.id)
    if membership_info['status'] == 'left':
        logger.info(f'Skipping welcome message, user {new_member.name} is no longer in the chat')
        return

    logger.info(f'send welcome message for {new_member.name}')
    msg = None

    if new_member.is_bot:
        msg = f"{new_member.name} is a *bot*!! " \
              "-> It could be kindly removed 🗑"
    else:
        if utils.is_bot(new_member):
            context.bot.delete_message(update.message.chat_id,
                                       update.message.message_id)
            if context.bot.kick_chat_member(update.message.chat_id, new_member.id):
                msg = (f"*{new_member.username}* has been banned because I "
                       "considered it was a bot. ")
        else:
            msg = f"Welcome {new_member.name}!! " \
                   "I am a friendly and polite *bot* 🤖"
    if msg:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=msg,
            parse_mode=telegram.ParseMode.MARKDOWN
        )


def reply(update, context):
    if not config.bot_replies_enabled():
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
        level=config.LOG_LEVEL,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        )
    logger.info('Starting bot...')
    config.log(logger.info)
    updater = Updater(config.TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', command_start))
    dp.add_handler(CommandHandler('help', command_help))
    dp.add_handler(CommandHandler('status', command_status))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members,
                                  welcome, run_async=True))
    dp.add_handler(MessageHandler(Filters.chat_type.groups, reply))

    logger.info('Bot is ready')
    updater.start_polling(poll_interval=config.POLL_INTERVAL)
    updater.idle()


if __name__ == "__main__":
    main()
