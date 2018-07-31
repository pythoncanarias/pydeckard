import random
import config
import re
import telegram
from telegram.ext import Updater, Filters, MessageHandler
from telegram import Bot, Update
from utils import is_bot


def welcome(bot: Bot, update: Update):
    new_member = update.message.new_chat_members[0]
    msg = None

    if new_member.is_bot:
        msg = f"{new_member.name} is a *bot*!! " \
              "-> It could be kindly removed 🗑"
    else:
        if is_bot(new_member):
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


updater = Updater(config.TELEGRAM_BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dp.add_handler(MessageHandler(Filters.group, reply))

updater.start_polling()
updater.idle()
