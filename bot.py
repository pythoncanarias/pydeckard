import config
from myconfig import TELEGRAM_BOT_TOKEN
import telegram
from telegram.ext import Updater, Filters, MessageHandler
import re


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
            bot.send_message(
                chat_id=update.message.chat_id,
                text=value
            )


updater = Updater(TELEGRAM_BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dp.add_handler(MessageHandler(Filters.group, reply))

updater.start_polling()
updater.idle()
