from telegram import Update
from telegram.ext import ContextTypes

from data.constants import messagesToDelete, MESSAGES_FROM_BOT, CIPHER, LENGTH, END
from utils.cipher import calculateCipher
from handlers.commands import scheduleDeletion


async def collectCipher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	text = update.message.text
	messagesToDelete.append([context, update.message])

	if not (4 <= len(text) <= 30):
		message = await update.message.reply_text(MESSAGES_FROM_BOT[context.user_data['language']]["invalidCypher"])
		messagesToDelete.append([context, message])
		return CIPHER

	context.user_data['cipher'] = text
	message = await update.message.reply_text(MESSAGES_FROM_BOT[context.user_data['language']]["provideLength"])

	messagesToDelete.append([context, message])
	return LENGTH


async def collectLength(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
	messagesToDelete.append([context, update.message])

	try:
		value = int(update.message.text)
	except ValueError:
		message = await update.message.reply_text(MESSAGES_FROM_BOT[context.user_data['language']]["invalidLength"])
		messagesToDelete.append([context, message])
		return LENGTH

	if not (15 <= value <= 45):
		message = await update.message.reply_text(MESSAGES_FROM_BOT[context.user_data['language']]["invalidLength"])
		messagesToDelete.append([context, message])
		return LENGTH

	context.user_data['length'] = value
	finalHash = calculateCipher(context.user_data, update.effective_user)

	message = await update.message.reply_text(text=finalHash)
	messagesToDelete.append([context, message])
	await scheduleDeletion(update.message.chat_id, context)
	return END
