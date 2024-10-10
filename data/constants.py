import json
import os
from dotenv import load_dotenv
from telegram.ext import ConversationHandler

load_dotenv()
with open(os.path.join(os.path.dirname(__file__), '../config.json')) as json_file:
    config = json.load(json_file)

DELETE_DELAY = config['DeleteDelay']
SPECIAL_CHARACTERS = config['SpecialCharacters']
BOT_TOKEN = os.getenv('botToken')
MESSAGES_FROM_BOT = config['messagesFromBot']
LOG_LEVEL = config['logLevel']

CIPHER, LENGTH = range(2)
END = ConversationHandler.END

messagesToDelete = []
