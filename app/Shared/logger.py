from loguru import logger
import sys

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
)

logger.add(
    "logs/bot.log",
    rotation="10 MB",
    retention="5 days",
    level="INFO",
)