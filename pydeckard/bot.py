#!/usr/bin/enb python3
from datetime import datetime as DateTime
import itertools
import argparse
import logging
import sys
import time

import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, filters, MessageHandler, CommandHandler, ContextTypes
from telegram.constants import ParseMode


from pydeckard import utils
from pydeckard import config


class DeckardBot():

    def __init__(self):
        self.get_options()
        self.set_logger()
        self.started_at = DateTime.now()
    
    def get_options(self):
        parser = argparse.ArgumentParser(
            prog='bot',
            description='PyDeckard Bot',
            epilog='Text at the bottom of help',
            )
        parser.add_argument('--setup', action='store_true', help='Start the setup wizard')
        args = parser.parse_args()
        if args.setup:
            utils.setup_bot()


    def set_logger(self):
        self.logger = logging.getLogger('bot')

        console_handler = logging.StreamHandler()
        logging.basicConfig(
                level=logging.DEBUG,  # Pone el nivel de todos los logger a WARNING
                format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
                handlers=[console_handler],
                force=True
                )

        # Ajustamos el nivel del logger bot
        self.logger.setLevel(config.LOG_LEVEL)
        config.log(self.logger.info)

    def trace(self, msg):
        self.logger.info(msg)


    async def command_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.trace('Received command: /status')
        python_version = sys.version.split(maxsplit=1)[0]
        text = '\n'.join([
            config.BOT_GREETING,
            f'Status is <b>OK</b>, running since {utils.since(self.started_at)}',
            f'Python version is {python_version}',
            ])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            )
        self.trace(text)

    async def command_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.trace('Received command: /start')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=config.BOT_GREETING,
            parse_mode=ParseMode.HTML,
            )

    async def command_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.trace('Received command: /help')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "Available commands:\n\n"
                "<code>/start</code> : start intereaction with the bot\n"
                "<code>/help</code> : Show commands\n"
                "<code>/status</code> : Show status and alive time\n"
                "<code>/config</code> : See (some) config parameters\n"
                "<code>/zen</code> : Show the Zen of Python\n"
                ),
            parse_mode=ParseMode.HTML,
            )

    async def command_zen(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.trace('Received command: /zen')
        text = '\n'.join(config.THE_ZEN_OF_PYTHON)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            )

    async def command_config(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.trace('Received command: /config')
        buff = [
            f'Probabilidad de responder: {config.VERBOSITY:.2f}',
            'Disparadores:',
            ]
        trigger_words = sorted(list(itertools.chain(*config.REPLIES.keys())))
        for word in trigger_words:
            buff.append(f' - {word}')
        text = '\n'.join(buff)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=text,
            parse_mode=ParseMode.HTML,
            )

    async def welcome(self, update: Update, context):
        self.trace('Received new user event')
        new_member = update.message.new_chat_members[0]

        self.trace(f'Waiting {config.WELCOME_DELAY} seconds until user completes captcha...')
        time.sleep(config.WELCOME_DELAY)
        membership_info = await context.bot.get_chat_member(update.message.chat_id, new_member.id)
        if membership_info['status'] == 'left':
            self.trace(f'Skipping welcome message, user {new_member.name} is no longer in the chat')
            return

        self.trace(f'Send welcome message for {new_member.name}')
        msg = None

        if new_member.is_bot:
            msg = f"{new_member.name} is a *bot*\\!\\! " \
                  "-> It could be kindly removed 🗑"
        else:
            if utils.is_bot(new_member):
                await context.bot.delete_message(update.message.chat_id,
                                           update.message.message_id)
                if await context.bot.kick_chat_member(update.message.chat_id, new_member.id):
                    msg = (f"*{new_member.username}* has been banned because I "
                           "considered it was a bot. ")
            else:
                msg = f"Welcome {new_member.name}\\!\\! " \
                       "I am a friendly and polite *bot* 🤖"
        if msg:
            await update.message.reply_text(msg, parse_mode=telegram.constants.ParseMode('MarkdownV2'))

    async def reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if config.bot_replies_enabled():
            msg = update.message.text
            reply_spec = utils.triggers_reply(msg) if msg else None
            if reply_spec is not None:
                self.trace(f'Sending reply: {reply_spec.reply}')
                await update.message.reply_text(reply_spec.reply)

    def run(self):
        self.trace('Starting bot')
        application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
        start_handler = CommandHandler('start', self.command_start)
        application.add_handler(start_handler)
        help_handler = CommandHandler('help', self.command_help)
        application.add_handler(help_handler)
        status_handler = CommandHandler('status', self.command_status)
        application.add_handler(status_handler)

        # Zen Command
        application.add_handler(CommandHandler('zen', self.command_zen))

        # Config Command
        application.add_handler(CommandHandler('config', self.command_config))

        welcome_handler = MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            self.welcome,
            )
        application.add_handler(welcome_handler)
        reply_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND),
            self.reply,
            )
        application.add_handler(reply_handler)
        self.trace('Bot is ready')
        application.run_polling(poll_interval=config.POLL_INTERVAL)


def main():
    bot = DeckardBot()
    bot.run()

if __name__ == "__main__":
    main()
