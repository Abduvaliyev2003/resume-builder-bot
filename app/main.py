import asyncio

from aiogram.types import BotCommand

from app.Domains.Auth.router import router as auth_router
from app.Domains.Resume.router import router as resume_router
from app.Domains.Template.router import router as template_router
from app.Shared.api import api
from app.Shared.bot import bot, dp
from app.Shared.logger import logger


async def main() -> None:
    """Start the Telegram bot in long-polling mode."""

    dp.include_router(auth_router)
    dp.include_router(template_router)
    dp.include_router(resume_router)

    try:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Start bot"),
                BotCommand(command="menu", description="Open main menu"),
                BotCommand(command="resume", description="Open resume menu"),
            ]
        )
        logger.info("Starting Resume Builder Telegram Bot")
        await dp.start_polling(bot)
    finally:
        await api.close()
        await bot.session.close()
        logger.info("Resume Builder Telegram Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
