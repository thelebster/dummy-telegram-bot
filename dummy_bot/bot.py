import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
BOT_RUN_MODE = os.getenv('BOT_RUN_MODE', 'polling')

# Used within `webhook` mode.
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '127.0.0.1')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', os.getenv('PORT', 80)))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'http:/%s:%s/' % (WEBHOOK_HOST, WEBHOOK_PORT))


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text("Hello cruel world do you know that you're killing me?")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("My dear cruel world do you ever think about me?")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    if BOT_RUN_MODE == 'webhook':
        updater.start_webhook(listen=WEBHOOK_HOST, port=WEBHOOK_PORT, url_path=TELEGRAM_API_TOKEN)
        updater.bot.set_webhook(WEBHOOK_URL + TELEGRAM_API_TOKEN)
    else:
        updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
