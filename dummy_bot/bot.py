import os
import html
import json
import logging
import traceback

from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# The token you got from @botfather when you created the bot
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# This can be your own ID, or one for a developer group/channel.
# You can use the /start command of this bot to see your chat id.
DEVELOPER_CHAT_ID = os.getenv('DEVELOPER_CHAT_ID')

BOT_RUN_MODE = os.getenv('BOT_RUN_MODE', 'polling')

# Used within `webhook` mode.
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', '127.0.0.1')
WEBHOOK_PORT = int(os.getenv('WEBHOOK_PORT', os.getenv('PORT', 80)))
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'http:/%s:%s/' % (WEBHOOK_HOST, WEBHOOK_PORT))


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.effective_message.reply_html(
        'Use /bad_command to cause an error.\n\n'
        f'Your chat id is <code>{update.effective_chat.id}</code>.'
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("My dear cruel world do you ever think about me?")


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def bad_command(update: Update, context: CallbackContext) -> None:
    """Raise an error to trigger the error handler."""
    raise Exception("Something went wrong, please try again later.")


def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error or/and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update.to_dict(), indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    chat_id = DEVELOPER_CHAT_ID
    if chat_id is None:
        # Send error message back to current chat.
        chat_id = update.effective_chat.id

    # Finally, send the message
    context.bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)


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
    dispatcher.add_handler(CommandHandler('bad_command', bad_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Register the error handler.
    dispatcher.add_error_handler(error_handler)

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
