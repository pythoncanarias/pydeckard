import config
from telegram.ext import Updater, Filters, MessageHandler


def welcome(bot, update):
    new_member = update.message.new_chat_members[0]
    if new_member.is_bot:
        msg = f"@{new_member.username} is a bot!! -> Remove it ❌"
    else:
        msg = f"Welcome {new_member.name}!! 😀"
    bot.send_message(chat_id=update.message.chat_id, text=msg)


updater = Updater(config.TELEGRAM_BOT_TOKEN)

updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, welcome)
)


updater.start_polling()
updater.idle()
