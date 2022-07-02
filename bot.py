import requests
from bs4 import BeautifulSoup as bs
import logging
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    PicklePersistence,
)
import os
import time
import random
import re

PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #your telegram bot token
persistence = PicklePersistence('./db', store_user_data=True)


def nothing(update, context):
    update.message.reply_text('Xin chào, nhập link để tải nhé')


def start(update, context):
    update.message.reply_text(
        'Xin chào, mình lập Bot này để hỗ trợ mọi người tải file pdf từ sci-hub')


def sci(update, context):
    ids = update.message.message_id
    chat_id = update.message.chat_id
    ur = update.message.text
    u = 'https://sci-hub.st/'
    response = requests.get('https://spys.me/socks.txt')
    proxies = response.text
    pattern = re.compile("\\d{1,3}(?:\\.\\d{1,3}){3}(?::\\d{1,5})?")
    matcher = re.findall(pattern, proxies)
    px = []
    px = matcher[:10]
    for i in px:
        proxies = {'socks':i}
        sci_url = 'https://sci-hub.st/' + ur
        req1 = requests.get('https://ifconfig.me/',timeout = 1)
        req2 = requests.get(sci_url, proxies = proxies, timeout = 10)
        if req2.status_code == 200 and req1.status_code == 200:
            res = req2.text
            soup = bs(res, 'html.parser')
            link = soup.findAll("button")
            title = soup.findAll('i')
            try:
                if len(link) != 0:
                    link1 = link[0]["onclick"].split("'")[1]
                    if link1[:2] == "//":
                        link6 = "https:" + link1
                        update.message.reply_text(link6)
                    else:
                        link6 = link1
                        update.message.reply_text(link6)
                    if len(title) != 0:
                        title1 = title[0].text.split(".")[0]
                        title2 = title1 + ".pdf"
                    else:
                        title2 = "your_file.pdf"
                    response = requests.get(link6)
                    with open(title2, 'wb') as f:
                        f.write(response.content)
                    file_size = os.path.getsize(title2)
                    if file_size < 50000000:
                        update.message.reply_text("Your output file: \n")
                        context.bot.send_document(chat_id, open(
                            title2, 'rb'),  reply_to_message_id=ids)
                    else:
                        update.message.reply_text(
                            "Your file is too big \nClick link to down load")
                        update.message.reply_text(link6)
                else:
                    text = 'Lỗi: ' + str(req2.status_code)
                    update.message.reply_text(
                        "Look like link is not found Or Wrong Link")
                    context.bot.send_message('-624406509', text)

            except IndexError:
                update.message.reply_text("__ERROR__")
        break


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True, persistence=persistence)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.regex('^(http|https|www).*$'), sci))
    dp.add_handler(MessageHandler(
        ~(Filters.command | Filters.regex('^(http|https|www).*$')), nothing))

    # log all errors
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=int(
        PORT), url_path=TOKEN, webhook_url="https://your-heroku-app.herokuapp.com/" + TOKEN) 
    #change your your-heroku-app
    #updater.idle()


if __name__ == '__main__':
    main()
