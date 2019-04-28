import telegram
from telegram.ext import Updater, Filters, MessageHandler
from telegram import Bot, Update

import config
import utils


def welcome(bot: Bot, update: Update):
    new_member = update.message.new_chat_members[0]
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
        bot.send_message(
            chat_id=update.message.chat_id,
            text=reply_spec.reply
        )


updater = Updater(config.TELEGRAM_BOT_TOKEN)
dp = updater.dispatcher

dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
dp.add_handler(MessageHandler(Filters.group, reply))

updater.start_polling()
updater.idle()
