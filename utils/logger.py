import logging

from data.constants import LOG_LEVEL

def setup_logging():
	console_handler = logging.StreamHandler()
	console_handler.setLevel(logging.INFO)
	console_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

	console_logger = logging.getLogger('console_logger')
	console_logger.setLevel(LOG_LEVEL)
	console_logger.addHandler(console_handler)

	logging.getLogger("httpx").setLevel(logging.WARNING)
