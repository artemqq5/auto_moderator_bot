import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from routers import register_, add_channel_, show_channel_, request_join_

storage = MemoryStorage()
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=BOT_TOKEN, default=default_properties)
dp = Dispatcher(storage=storage)
dp.include_routers(register_.register_router, add_channel_.router, show_channel_.router)


async def main():
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        print(f"start bot: {e}")


if __name__ == '__main__':
    asyncio.run(main())
