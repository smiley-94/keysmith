import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.error import BadRequest
from telegram.ext import ContextTypes, CallbackContext

from data.constants import messagesToDelete, MESSAGES_FROM_BOT, CIPHER, END, DELETE_DELAY
from utils.cipher import calculateRandomCipher


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.language_code:
        context.user_data['language'] = update.effective_user.language_code[:2]

    if context.user_data['language'] not in ["it", "en", "pt"]:
        context.user_data['language'] = "en"

    chat_id = update.message.chat_id
    await sendInitialInlineButton(context, chat_id)
    messagesToDelete.append([context, update.message])


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message = await update.message.reply_text("Operation stopped.")
    messagesToDelete.append([context, message])
    return END


async def button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'start_cipher':
        if query.from_user.language_code:
            context.user_data['language'] = query.from_user.language_code[:2]

        if context.user_data['language'] not in ["it", "en", "pt"]:
            context.user_data['language'] = "en"

        message = await query.message.reply_text(MESSAGES_FROM_BOT[context.user_data['language']]["provideCypher"])
        messagesToDelete.append([context, message])
        context.job_queue.run_once(deleteMessage, 0, chat_id=query.message.chat_id, data=query.message.message_id)
        return CIPHER

    elif query.data == 'random':
        message = await query.message.reply_text(calculateRandomCipher())
        messagesToDelete.append([context, message])
        await scheduleDeletion(query.message.chat_id, context)
        context.job_queue.run_once(deleteMessage, 0, chat_id=query.message.chat_id, data=query.message.message_id)
        return END


async def sendInitialInlineButton(context: CallbackContext, chat_id: int):
    keyboard = [
        [InlineKeyboardButton("Start", callback_data='start_cipher')],
        [InlineKeyboardButton("Random", callback_data='random')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id,
                                   text=MESSAGES_FROM_BOT[context.user_data['language']]["welcomeMessage"],
                                   reply_markup=reply_markup)
    # messagesToDelete.append([context, message])


async def deleteMessage(context: CallbackContext) -> None:
    job = context.job
    try:
        await context.bot.delete_message(chat_id=job.chat_id, message_id=job.data)
    except Exception as e:
        logging.error(f"Error deleting message: {e}")


async def scheduleDeletion(chat_id: int, context: CallbackContext):
    for message in messagesToDelete:
        context, msg = message
        context.job_queue.run_once(deleteMessage, DELETE_DELAY, chat_id=msg.chat_id, data=msg.message_id)

    messagesToDelete.clear()
    context.job_queue.run_once(lambda _: sendInitialInlineButton(context, chat_id), DELETE_DELAY + 1)
