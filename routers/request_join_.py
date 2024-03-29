from aiogram import Router, types, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.repositories.LinkRepository import LinkRepository

router = Router()


@router.chat_join_request()
async def handle_join_request(chat_join_request: types.ChatJoinRequest, bot: Bot):
    user_id = chat_join_request.from_user.id
    link = chat_join_request.invite_link.invite_link

    link_from_db = LinkRepository().get_link(link)

    try:
        try:
            await chat_join_request.approve()
        except TelegramBadRequest as e:
            if "USER_ALREADY_PARTICIPANT" not in str(e):
                raise Exception

        if not link_from_db:
            raise Exception

        LinkRepository().update_link(user_join=link_from_db['users_join'] + 1, link=link)

        if link_from_db['hello_message']:
            kb_join = InlineKeyboardBuilder(markup=[
                [InlineKeyboardButton(text="Open", url=link_from_db['link'])]
            ])

            await bot.send_message(chat_id=user_id,
                                   text=link_from_db['hello_message'],
                                   reply_markup=kb_join.as_markup())
    except Exception as e:
        print(f"handle_join_request: {e} | @{chat_join_request.from_user.username}")
