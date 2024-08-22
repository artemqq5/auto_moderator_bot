from aiogram import Router, types, F, Bot
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import TelegramForbiddenError

from accesss.check_registered import is_user_registered_admin
from constants.buttons_ import ADD_CHANNEL
from constants.messages_ import HOW_TO_ADD_CHANNEL, BOT_IS_NO_ADMIN_THAT_CHANNEL, CHANNEL_ALREADY_ADDED_TO_YOU, \
    CHANNEL_ERROR_ADD, CHANNEL_JUST_ADDED
from data.repositories.ChannelRepository import ChannelRepository

router = Router()


@router.message(F.text == ADD_CHANNEL)
async def add_channel_handler(message: types.Message):
    if not await is_user_registered_admin(message):
        return

    await message.answer(HOW_TO_ADD_CHANNEL)


@router.message(F.forward_from_chat.type == 'channel')
async def forward_message_handler(message: types.Message, bot: Bot):
    if not await is_user_registered_admin(message):
        return

    id_channel = message.forward_from_chat.id
    title_channel = message.forward_from_chat.title

    try:
        status_bot = await bot.get_chat_member(chat_id=id_channel, user_id=bot.id)
        if status_bot.status != ChatMemberStatus.ADMINISTRATOR:
            raise TelegramForbiddenError
    except TelegramForbiddenError as _:
        await message.answer(BOT_IS_NO_ADMIN_THAT_CHANNEL)
        return

    if ChannelRepository().get_channel(id_channel):
        await message.answer(CHANNEL_ALREADY_ADDED_TO_YOU)
        return

    if not ChannelRepository().add_channel(id_channel, title_channel, message.from_user.id):
        await message.answer(CHANNEL_ERROR_ADD)
        return

    await message.answer(CHANNEL_JUST_ADDED)
