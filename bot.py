import config
from telegram.ext import Updater, Filters, MessageHandler


def check_bots(bot, update):
    new_member = update.message.new_chat_members[0]
    if new_member.is_bot:
        msg = f"@{new_member.username} is a bot!! -> Remove it ❌"
        bot.send_message(chat_id=update.message.chat_id, text=msg)


updater = Updater(config.TELEGRAM_BOT_TOKEN)

updater.dispatcher.add_handler(
    MessageHandler(Filters.status_update.new_chat_members, check_bots)
)


updater.start_polling()
updater.idle()
