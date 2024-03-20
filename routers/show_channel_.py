from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from accesss.check_registered import is_user_registered
from constants.buttons_ import SHOW_CHANNELS
from constants.messages_ import LIST_CHANNELS_EMPTY
from data.repositories.ChannelRepository import ChannelRepository

router = Router()


@router.message(F.text == SHOW_CHANNELS)
async def show_channel_handler(message: types.Message):
    if not await is_user_registered(message):
        return

    list_channels = ChannelRepository().get_all_channels(message.from_user.id)

    if not list_channels:
        await message.answer(LIST_CHANNELS_EMPTY)
        return

    for channel in list_channels:
        body_message = f"Канал: {channel['title']}\nID: {channel['channel_id']}\nДоданий: {channel['_at']}"
        kb = [
            [InlineKeyboardButton(text="Видалити канал", callback_data=f"{channel['channel_id']}_delete")],
            [InlineKeyboardButton(text="Управляти посиланнями", callback_data=f"{channel['channel_id']}_managelinks")]
        ]
        await message.answer(body_message, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))


@router.callback_query(F.data.contains("delete"))
async def delete_cannel_handler(callback: types.CallbackQuery):
    print(callback.data)


@router.callback_query(F.data.contains("managelinks"))
async def managelink_cannel_handler(callback: types.CallbackQuery):
    print(callback.data)
