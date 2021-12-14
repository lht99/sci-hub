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
persistence = PicklePersistence('./db', store_user_data = True)

def start(update, context):
    update.message.reply_text('Xin chào, mình lập Bot này để hỗ trợ mọi người tải file pdf từ sci-hub')
def sci(update, context):
    ids = update.message.message_id
    chat_id =  update.message.chat_id
    url = update.message.text
    sci_url = 'https://sci-hub.se/' + url
    update.message.reply_text("Retrieving: " + sci_url)
    html_text = requests.get(sci_url).text
    soup = bs(html_text, 'html.parser')
    link = soup.findAll('button')[0]["onclick"].split("'")[1]
    update.message.reply_text("Link: " + link)
    if link[:2] == "//":
        link2 = link.replace("//", "http://")
        update.message.reply_text("Link2if: " + link2)
    else:
        link2 = link
        update.message.reply_text("Link2else: " + link2)
    link3 = soup.findAll('i')
    update.message.reply_text("Link3: ")
    
    if len(link3) == 0:
        link4 = "your file.pdf"
        update.message.reply_text("Link4: " + link4)
    else: 
        link4 = link3[0].text + ".pdf"
        update.message.reply_text("Link5: " + link4)
    response = requests.get(link2)
    with open(link4, 'wb') as f:
                              f.write(response.content)
    f.close()
    update.message.reply_text("Your output file: \n")
    context.bot.send_document(chat_id, open(link4, 'rb'),  reply_to_message_id = ids)                        
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

    # log all errors
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN, webhook_url="https://sci-letuan.herokuapp.com/" + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
