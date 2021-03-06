from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import urllib.request
import uuid
import logging
import os
from amadlib import read_madlibs, generate_output

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                        level=logging.WARN)

logger = logging.getLogger(__name__)

user_madlib = {}

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
    audio_url = "https://pdcmadlib.radiocut.fm/media/" + choosen_madlib["parts"][0]["file"].replace(".wav", ".mp3")

    print(audio_url)
    update.message.reply_audio(audio=audio_url)
    user_madlib[update.message.from_user.id] = choosen_madlib

def get_audio_input(bot, update):
    user_id = update.message.from_user.id
    if not user_id in user_madlib:
        update.message.reply_text("Please say 'Hi' first and choose a question")
        return
    audio_file = bot.get_file(update.message.voice.file_id)
    audio_fd = urllib.request.urlopen(audio_file.file_path)
    task_id = str(uuid.uuid4())
    input_filename = "user_input/%s%s" % (task_id, audio_file.file_path.split(".")[-1])
    open(input_filename, "wb").write(audio_fd.read())
    generate_output(user_madlib[user_id]["key"], input_filename, task_id)
    audio_url = "https://pdcmadlib.radiocut.fm/output/%s.mp3" % task_id
    update.message.reply_audio(audio=audio_url)

#
#ipdb> update.message.voice.file_id
#'AwADAQADUQADvyLARI99_YckuzqzAg'
#ipdb> bot.get_file(update.message.voice.file_id)
#<telegram.file.File object at 0x7fd100d4aba8>
#ipdb> f = bot.get_file(update.message.voice.file_id)
#ipdb> f.file_path
#'https://api.telegram.org/file/bot386607382:AAHFry5WfTyTU2Nhz4kEUm3TulSgFhonxMM/voice/4953997793841643601.oga'


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
dp.add_handler(MessageHandler(Filters.audio | Filters.voice, get_audio_input))
dp.add_error_handler(error_callback)

updater.start_polling()
updater.idle()

