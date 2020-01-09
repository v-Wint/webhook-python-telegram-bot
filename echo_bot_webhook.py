#!/usr/bin/python3.8
from requirements import TOKEN, USERNAME # telegram token and username of pythonanywhere account
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher, MessageHandler, Filters
import json

# handlers
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

	
app = Flask(__name__)
def main():
    # add dispatcher
    bot = Bot(TOKEN)
    dp = Dispatcher(bot, None, workers=0, use_context=True)
    # add handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_))
    dp.add_handler(MessageHandler(Filters.text, echo))
    # start webhook
    bot.delete_webhook()
    url = f"https://{USERNAME}.pythonanywhere.com/{TOKEN}"
    bot.set_webhook(url=url)
    
    # process updates
    @app.route('/' + TOKEN, methods=['POST'])
    def webhook():
        json_string = request.stream.read().decode('utf-8')
        update = Update.de_json(json.loads(json_string), bot)
        dp.process_update(update)
        return 'ok', 200

# make sure you've inserted your app.py name
if __name__ == "main":
    main()
