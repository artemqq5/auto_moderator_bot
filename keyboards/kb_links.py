import math

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from data.repositories.UserRepository import UserRepository


class LinkChoice(CallbackData, prefix="LinkChoice"):
    channel_id: str


class LinkNavigation(CallbackData, prefix="LinkNavigation"):
    page: int


def kb_link_choice(links, current_page=1):
    inline_kb = []

    total_pages = math.ceil(len(links) / 10)
    start_index = (current_page - 1) * 10
    end_index = min(start_index + 10, len(links))

    # load from db
    for i in range(start_index, end_index):
        users = UserRepository().get_users_by_channel(links[i]['users_join'])
        inline_kb.append(
            [InlineKeyboardButton(
                text=f"{links[i]['link_title']} | users:{len(users)}",
                callback_data=LinkChoice(channel_id=links[i]['link'].replace("https://t.me/", "")).pack()
            )]
        )

    if len(links) > 10:
        nav = []
        # Navigation buttons
        if current_page > 1:
            nav.append(InlineKeyboardButton(
                text='<',
                callback_data=LinkNavigation(page=current_page - 1).pack()
            ))
        else:
            nav.append(InlineKeyboardButton(
                text='<',
                callback_data="None"
            ))

        nav.append(InlineKeyboardButton(text=f"{current_page}/{total_pages}", callback_data="None"))

        if current_page < total_pages:
            nav.append(InlineKeyboardButton(
                text='>',
                callback_data=LinkNavigation(page=current_page + 1).pack()
            ))
        else:
            nav.append(InlineKeyboardButton(
                text='>',
                callback_data="None"
            ))

        inline_kb.append(nav)

    inline_kb.append(
        [InlineKeyboardButton(text="Назад", callback_data=BackChannel().pack())]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


class BackLinkList(CallbackData, prefix="BackLinkList"):
    pass


class BackChannel(CallbackData, prefix="BackChannel"):
    pass


def kb_link_manage(link):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Видалити", callback_data=f"{link['link']}#####{link['channel_id']}#####deletelink")],
        [InlineKeyboardButton(text="Назад", callback_data=BackLinkList().pack())]
    ])
