import logging
from time import sleep

import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, filters, MessageHandler, CommandHandler, ContextTypes

import config
import utils


async def command_start(update, context):
    logger.info('Received command /start')
    await update.message.reply_text(config.BOT_GREETING)


async def command_help(update, context):
    logger.info('Received command /help')
    await update.message.reply_text("Available commands:\n"
                                    " - /start - start intereaction with the bot\n"


async def command_status(update, context):
    logger.info('bot asked to execute /status commamd')
    await update.message.reply_text(f'Status is OK, running since {utils.since()}',)


async def welcome(update: Update, context):
    logger.info('Received new user event')
    new_member = update.message.new_chat_members[0]

    logger.info(f'Waiting {config.WELCOME_DELAY} seconds until user completes captcha...')
    sleep(config.WELCOME_DELAY)
    membership_info = await context.bot.get_chat_member(update.message.chat_id, new_member.id)
    if membership_info['status'] == 'left':
        logger.info(f'Skipping welcome message, user {new_member.name} is no longer in the chat')
        return

    logger.info(f'send welcome message for {new_member.name}')
    msg = None

    if new_member.is_bot:
        msg = f"{new_member.name} is a *bot*\!\! " \
              "-> It could be kindly removed 🗑"
    else:
        if utils.is_bot(new_member):
            await context.bot.delete_message(update.message.chat_id,
                                       update.message.message_id)
            if await context.bot.kick_chat_member(update.message.chat_id, new_member.id):
                msg = (f"*{new_member.username}* has been banned because I "
                       "considered it was a bot. ")
        else:
            msg = f"Welcome {new_member.name}\!\! " \
                   "I am a friendly and polite *bot* 🤖"
    if msg:
        await update.message.reply_text(msg, parse_mode=telegram.constants.ParseMode('MarkdownV2'))


async def reply(update, _context):
    if not config.bot_replies_enabled():
        return

    msg = update.message.text
    reply_spec = utils.triggers_reply(msg) if msg else None
    if reply_spec is not None:
        logger.info(f'bot sends reply {reply_spec.reply}')
        await update.message.reply_text(reply_spec.reply)
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
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler('start', command_start))
    app.add_handler(CommandHandler('help', command_help))
    app.add_handler(CommandHandler('status', command_status))
    app.add_handler(MessageHandler(
        filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.ChatType.GROUPS, reply))

    logger.info('Bot is ready')
    app.run_polling(allowed_updates=Update.ALL_TYPES,
                    poll_interval=config.POLL_INTERVAL)


if __name__ == "__main__":
    main()
