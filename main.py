from decouple import config
import asyncio

import logging
from aiogram import Bot, Dispatcher, Router, types

from handlers.callback_handlers import router as callback_router
from handlers.command_handlers import router as command_router
from handlers.message_handlers import router as message_router

Bot_token = str(config("TOKEN"))



dp = Dispatcher()
router = Router()


dp.include_routers(
    callback_router,
    command_router
)


async def main() -> None:
    bot = Bot(config("TOKEN"), parse_mode="HTML")
    commands = [
        types.BotCommand(command="/start", description="Start command"),
    ]
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())


