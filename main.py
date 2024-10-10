from telegram import Update
from telegram.ext import Application, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, filters

from data.constants import BOT_TOKEN, CIPHER, LENGTH
from handlers.commands import start, stop, button
from handlers.conversation import collectCipher, collectLength
from utils.logger import setup_logging


def main() -> None:
	setup_logging()
	application = Application.builder().token(BOT_TOKEN).build()

	conv_handler = ConversationHandler(
		entry_points=[CallbackQueryHandler(button, pattern='^(start_cipher|random)$')],
		states={
			CIPHER: [MessageHandler(filters.TEXT & ~filters.COMMAND, collectCipher)],
			LENGTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, collectLength)],
		},
		fallbacks=[CommandHandler("stop", stop)]
	)

	application.add_handler(CommandHandler("start", start))
	application.add_handler(conv_handler)
	application.add_handler(CallbackQueryHandler(button, pattern='^(start_cipher|random)$'))

	application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
	main()
