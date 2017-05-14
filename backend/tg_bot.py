from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os
from amadlib import read_madlibs

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                        level=logging.WARN)

logger = logging.getLogger(__name__)


def start(bot, update):
    logger.info("Bot Started")
    username = update.message.from_user.first_name
    welcome_message = "Hi %s, welcome to the podcast mad lib bot. Please choose a question: \n" % username
    madlibs = read_madlibs()
    for i, madlib in enumerate(madlibs):
        welcome_message += "%d. Interviewer: %s - Question: %s\n" % (i + 1, madlib["interviewer"],
                                                                     madlib["question"])
    update.message.reply_text(welcome_message)

def get_text_input(bot, update):
    madlibs = read_madlibs()
    if update.message.text.strip().lower() == "hi":
        return start(bot, update)

    if not update.message.text.isdigit() or int(update.message.text) not in range(1, len(madlibs) + 1):
        update.message.reply_text("Please send a number between 1 and %d. I'm a dumb bot" % len(madlibs))
        return
    choosen_madlib = madlibs[int(update.message.text) - 1]
    update.message.reply_text("%s asks: %s?" % (choosen_madlib["interviewer"],
                                                choosen_madlib["question"]))
    audio_url = "http://pdcmadlib.radiocut.fm/media/" + choosen_madlib["parts"][0]["file"].replace(".wav", ".mp3")
    print(audio_url)
    update.message.reply_audio(audio=audio_url)


def error_callback(bot, update, error):
    raise error
##    try:
##        raise error
##    except Unauthorized:
##        # remove update.message.chat_id from conversation list
##    except BadRequest:
##        # handle malformed requests - read more below!
##    except TimedOut:
##        # handle slow connection problems
##    except NetworkError:
##        # handle other connection problems
##    except ChatMigrated as e:
##        # the chat_id of a group has changed, use e.new_chat_id instead
##    except TelegramError:
##        # handle all other telegram related errors


updater = Updater('386607382:AAHFry5WfTyTU2Nhz4kEUm3TulSgFhonxMM')

dp = updater.dispatcher

dp.add_handler(CommandHandler('start', start))
dp.add_handler(MessageHandler(Filters.text, get_text_input))
dp.add_error_handler(error_callback)

updater.start_polling()
updater.idle()

