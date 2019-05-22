import logging
import datetime

import telegram
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from telegram import Bot, Update

import config
import utils
import dba

logger = logging.getLogger('bot')


def command_start(bot, update):
    logger.info('Received command /start')
    chat = update.message.chat
    is_new = dba.save_chat(chat.id, chat.type, chat.title)
    if is_new:
        bot.send_message(
            chat_id=update.message.chat_id,
            text=config.BOT_GREETING,
            parse_mode='Markdown',
            )


def command_help(bot, update):
    logger.info('Received command /help')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='\n'.join([
            "Available commands:",
            " - `/start` - start intereaction with the bot",
            " - `/help` - Show commands",
            " - `/status` - Show status and alive time",
            " - `/settings` - Show current settings",
            " - `/debug` - Show debug information for developers",
            ]),
        parse_mode='Markdown',
        )


def command_status(bot, update):
    logger.info('bot asked to execute /status commamd')
    bot.send_message(
        chat_id=update.message.chat_id,
        text=f'Status is **OK**, running since {utils.since()}',
        parse_mode='Markdown',
        )


def command_settings(bot, update):
    logger.info('Received command /settings')
    chat = update.message.chat
    if config.VERBOSITY < 1.0:
        verbosity_level = f'{round(config.VERBOSITY*100.0, 2)}%'
    else:
        verbosity_level = 'Palicoso'
    bot.send_message(
        chat_id=update.message.chat_id,
        text="\n".join([
            f"Settings for {chat.title}:",
            f" - Database: `{config.DB_NAME}`",
            f" - Verbosity level: `{verbosity_level}`",
            f" - Log level: `{config.LOG_LEVEL}`",
            f" - Poll interval time (in seconds): **{config.POLL_INTERVAL}**",
            f" - Repos (**0**)",
            ]),
        parse_mode='Markdown',
        )


def command_debug(bot, update):
    logger.info('Received command /debug')
    chat = update.message.chat
    conn = dba.get_connection()
    all_chats = dba.get_rows(conn, 'SELECT * FROM chat')
    buff = [
        "Chat:",
        f" - id: {chat.id}",
        f" - type: {chat.type}",
        f" - title: {chat.title}",
        f" - Chats: ({len(all_chats)})",
    ]
    for c in all_chats:
        buff.append(f'    - {c.title}')
    bot.send_message(
        chat_id=update.message.chat_id,
        text='\n'.join(buff),
        parse_mode='Markdown',
        )


def welcome(bot: Bot, update: Update):
    logger.info('Received new user event')
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
    if not config.bot_replies_enabled():
        return

    msg = update.message.text
    reply_spec = utils.triggers_reply(msg)
    if reply_spec is not None:
        logger.info(f'bot sends reply {reply_spec.reply}')
        bot.send_message(
            chat_id=update.message.chat_id,
            text=reply_spec.reply,
            parse_mode='Markdown',
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
    dp.add_handler(CommandHandler('settings', command_settings))
    dp.add_handler(CommandHandler('debug', command_debug))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dp.add_handler(MessageHandler(Filters.group, reply))

    logger.info('Bot is ready')
    updater.start_polling(poll_interval=config.POLL_INTERVAL)
    updater.idle()


if __name__ == "__main__":
    main()
