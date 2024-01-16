import asyncio

import logging

from aiogram import Dispatcher, Router, types


from bot_config import bot
from handlers.callback_handlers import router as callback_router
from handlers.command_handlers import router as command_router
from handlers.message_handlers import router as message_router
from handlers.other_functions import scheduler


dp = Dispatcher()
router = Router()


dp.include_routers(
    callback_router,
    command_router,
    message_router
)


async def main() -> None:
    
    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
        types.BotCommand(command="/favourite", description="Улюблені коктейлі")
    ]
    await bot.set_my_commands(commands)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)





if __name__ == "__main__":
    
    logging.basicConfig(level=logging.INFO)
    
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
    loop.run_until_complete(main())


