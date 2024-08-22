import math

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.repositories.LinkRepository import LinkRepository
from data.repositories.UserRepository import UserRepository


class ChannelChoice(CallbackData, prefix="ChannelChoice"):
    channel_id: str


class ChannelNavigation(CallbackData, prefix="ChannelNavigation"):
    page: int


def kb_channel_choice(channels, current_page=1):
    inline_kb = []

    total_pages = math.ceil(len(channels) / 10)
    start_index = (current_page - 1) * 10
    end_index = min(start_index + 10, len(channels))

    # load from db
    for i in range(start_index, end_index):
        links = LinkRepository().get_all(channels[i]['channel_id'])
        users = UserRepository().get_users_by_channel(channels[i]['channel_id'])
        inline_kb.append(
            [InlineKeyboardButton(
                text=f"{channels[i]['title']} | links:{len(links)} | users:{len(users)}",
                callback_data=ChannelChoice(channel_id=channels[i]['channel_id']).pack()
            )]
        )

    if len(channels) > 10:
        nav = []
        # Navigation buttons
        if current_page > 1:
            nav.append(InlineKeyboardButton(
                text='<',
                callback_data=ChannelNavigation(page=current_page - 1).pack()
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
                callback_data=ChannelNavigation(page=current_page + 1).pack()
            ))
        else:
            nav.append(InlineKeyboardButton(
                text='>',
                callback_data="None"
            ))

        inline_kb.append(nav)

    return InlineKeyboardMarkup(inline_keyboard=inline_kb)


class BackChannelList(CallbackData, prefix="BackChannelList"):
    pass


def kb_channel_manage(channel):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Видалити канал", callback_data=f"{channel['channel_id']}#####deletechannel")],
        [InlineKeyboardButton(text="Створити посилання",
                              callback_data=f"{channel['channel_id']}#####{channel['title']}#####createlink")],
        [InlineKeyboardButton(text="Управляти посиланнями",
                              callback_data=f"{channel['channel_id']}#####managelinks")],
        [InlineKeyboardButton(text="Назад", callback_data=BackChannelList().pack())]
    ])
