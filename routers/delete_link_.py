from aiogram import Router, F, types, Bot
from aiogram.utils.formatting import Text, Code

from constants.messages_ import SUCCESSFUL_LINK_DELTED, ERROR_LINK_DELETED_FROM_TG, \
    ERROR_LINK_DELETED_FROM_DATA_BASE
from data.repositories.LinkRepository import LinkRepository

router = Router()


@router.callback_query(F.data.contains('deletelink'))
async def delete_link_handler(callback: types.CallbackQuery, bot: Bot):
    link = callback.data.split("#####")[0]
    channel_id = callback.data.split("#####")[1]
    try:
        await bot.revoke_chat_invite_link(channel_id, link)

        if not LinkRepository().delete_link(link):
            await callback.message.answer(ERROR_LINK_DELETED_FROM_DATA_BASE)
            return

        await callback.message.answer(SUCCESSFUL_LINK_DELTED)
    except Exception as e:
        print(f"delete_link_handler: {e}")
        content = Text(ERROR_LINK_DELETED_FROM_TG, "\n", Code(e))
        await callback.message.answer(**content.as_kwargs())

