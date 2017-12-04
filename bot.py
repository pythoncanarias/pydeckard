import config
import telegram
from telegram.ext import Updater, Filters, MessageHandler


def welcome(bot, update):
    new_member = update.message.new_chat_members[0]
    if new_member.is_bot and new_member.username != "pydeckard_bot":
        msg = f"{new_member.name} is a *bot*!! " \
               "-> It could be kindly removed 🗑"
    else:
        msg = f"Welcome *{new_member.name}*!! " \
               "I am a friendly and polite bot 🤖"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=msg,
        parse_mode=telegram.ParseMode.MARKDOWN
    )


updater = Updater(config.TELEGRAM_BOT_TOKEN)

updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, welcome)
)


updater.start_polling()
updater.idle()
