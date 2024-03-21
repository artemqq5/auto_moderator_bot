import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from constants.messages_ import CANCEL_, CANCELED_SUCCESSFUL
from keyboards.crm_keyboard import kb_crm
from routers import register_, add_channel_, show_channel_, request_join_, create_link_, delete_link_, delete_channel_

storage = MemoryStorage()
default_properties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot = Bot(token=BOT_TOKEN, default=default_properties)
dp = Dispatcher(storage=storage)
dp.include_routers(
    register_.register_router,
    add_channel_.router,
    show_channel_.router,
    create_link_.router,
    delete_link_.router,
    delete_channel_.router,
    request_join_.router
)


@dp.message(F.text == CANCEL_)
async def cancel_(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(CANCELED_SUCCESSFUL, reply_markup=kb_crm.as_markup())


async def main():
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        print(f"start bot: {e}")


if __name__ == '__main__':
    asyncio.run(main())
