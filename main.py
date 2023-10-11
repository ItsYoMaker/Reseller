import asyncio
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import dbmanager
import parserkufar
from handlers import router

from bot import bot
from bot import dp

should_run = True
async def main():
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)


    async def run_tasks():
        tasks = [parserkufar.check_for_changes(url) for url in dbmanager.get_list_of_urls()]
        while should_run:
            await asyncio.gather(*tasks)

    await asyncio.gather(
        dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()),
        run_tasks()
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
