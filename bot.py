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

PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = "5028841551:AAHzMiqba6h6G1WcrGeNN08Jk2juiwNj_ss"
persistence = PicklePersistence('./db', store_user_data=True)


def nothing(update, context):
    update.message.reply_text('Xin chào, nhập link để tải nhé')


def start(update, context):
    update.message.reply_text(
        'Xin chào, mình lập Bot này để hỗ trợ mọi người tải file pdf từ sci-hub')


def sci(update, context):
    ids = update.message.message_id
    chat_id = update.message.chat_id
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.57'}
    ur = update.message.text
    sci_url = 'https://sci-hub.ru/' + str(ur)
    session = requests.Session()
    html_text = session.get(sci_url, headers = headers).text
    soup = bs(html_text, 'html.parser')
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
            text = str(requests.request('GET', sci_url, headers=headers).status_code) + " ERROR CODE. From_user: " + str(update.message.from_user['username'])
            update.message.reply_text("Look like link is not found Or Wrong Link")
            context.bot.send_message('-624406509', text)
            
    except IndexError:
        update.message.reply_text("__ERROR__")


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
        PORT), url_path=TOKEN, webhook_url="https://sci-letuan.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
