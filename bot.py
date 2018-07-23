import random
import config
import re
import telegram
from telegram.ext import Updater, Filters, MessageHandler
from telegram.chat import Chat
from myconfig import TELEGRAM_BOT_TOKEN
from utils import is_bot


def welcome(bot, update):
    new_member = update.message.new_chat_members[0]
    if new_member.is_bot:
        msg = f"{new_member.name} is a *bot*!! " \
               "-> It could be kindly removed 🗑"
    else:
        msg = f"Welcome {new_member.name}!! " \
               "I am a friendly and polite *bot* 🤖"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


def reply(bot, update):
    msg = update.message.text
    for key, value in config.REPLY.items():
        regex = "|".join([fr"\b{x}\b" for x in key])
        if re.search(regex, msg, re.I):
            if random.random() < config.VERBOSITY:
                if not isinstance(value, str):
                    # if value is a list
                    # then pick random string from multiple values
                    value = random.choice(value)
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text=value
                )


def ban_bots(bot, update):
    new_member = update.message.new_chat_members[0]
    if is_bot(new_member):
        msg = f"{new_member.username} has been banned. " \
              f"`Replicants are like any other machine, are either a benefit or a hazard.`"
        bot.kick_chat_member(update.message.chat_id, new_member.id)
        bot.send_message(
            chat_id=update.message.chat_id,
            text=msg,
            parse_mode=telegram.ParseMode.MARKDOWN
        )


updater = Updater(TELEGRAM_BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, ban_bots))
dp.add_handler(MessageHandler(Filters.group, reply))

updater.start_polling()
updater.idle()
