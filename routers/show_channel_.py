from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.formatting import Text, Bold, Code
from aiogram.utils.keyboard import InlineKeyboardBuilder

from accesss.check_registered import is_user_registered_admin
from constants.buttons_ import SHOW_CHANNELS
from constants.messages_ import LIST_CHANNELS_EMPTY, SET_NAME_FOR_LINK, LIST_LINKS_EMPTY, WITHOUT_NAME, MAX_20_LINKS, \
    MANAGMENT_LINKS, DELETE_CHANNEL
from data.repositories.ChannelRepository import ChannelRepository
from data.repositories.LinkRepository import LinkRepository
from keyboards.crm_keyboard import kb_skip, kb_cencel, kb_delete_channel
from states.StateCreateLink import StateCreateLink
from states.StateDeleteChannel import StateDeleteChannel

router = Router()


@router.message(F.text == SHOW_CHANNELS)
async def show_channel_handler(message: types.Message, bot: Bot):
    if not await is_user_registered_admin(message):
        return

    list_channels = ChannelRepository().get_all_channels(message.from_user.id)

    if not list_channels:
        await message.answer(LIST_CHANNELS_EMPTY)
        return

    for channel in list_channels:
        body_message = f"Канал: {channel['title']}\nID: {channel['channel_id']}\nДоданий: {channel['_at']}\n\n"

        links = LinkRepository().get_all(channel['channel_id'])
        users_join = 0

        for link in links:
            users_join += link['users_join']

        body_message += f"<b>Активних посилань: {len(links)}</b>\n"
        body_message += f"<b>Користувачів доєдналося: {users_join}</b>"

        kb = [
            [InlineKeyboardButton(text="Видалити канал", callback_data=f"{channel['channel_id']}#####deletechannel")],
            [InlineKeyboardButton(text="Створити посилання",
                                  callback_data=f"{channel['channel_id']}#####{channel['title']}#####createlink")],
            [InlineKeyboardButton(text="Управляти посиланнями", callback_data=f"{channel['channel_id']}#####managelinks")]
        ]
        await message.answer(body_message, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb))


@router.callback_query(F.data.contains("deletechannel"))
async def delete_cannel_handler(callback: types.CallbackQuery, state: FSMContext):
    channel_id = callback.data.split("#####")[0]
    await state.set_state(StateDeleteChannel.permission)
    await state.update_data(channel_id=channel_id)
    await callback.message.answer(DELETE_CHANNEL, reply_markup=kb_delete_channel.as_markup())


@router.callback_query(F.data.contains("managelinks"))
async def managelink_cannel_handler(callback: types.CallbackQuery):
    channel_id = callback.data.split("#####")[0]
    links = LinkRepository().get_all(channel_id)

    for link in links:
        users_join = 0
        users_join += link['users_join']
        content = Text(
            Bold(link['link_title'] if link['link_title'] is not None else WITHOUT_NAME), "\n\n",
            Bold(f"Користувачів доєдналося {users_join}"), "\n", Code(link['link'])
        )
        kb = InlineKeyboardBuilder([[InlineKeyboardButton(text="Видалити", callback_data=f"{link['link']}#####{channel_id}#####deletelink")]])
        await callback.message.answer(**content.as_kwargs(), reply_markup=kb.as_markup())

    await callback.message.answer(MANAGMENT_LINKS)


@router.callback_query(F.data.contains("createlink"))
async def createlink_cannel_handler(callback: types.CallbackQuery, state: FSMContext):
    channel_id = callback.data.split("#####")[0]
    channel_title = callback.data.split("#####")[1]

    if len(LinkRepository().get_all(channel_id)) >= 20:
        await callback.message.answer(MAX_20_LINKS)
        return

    await state.set_state(StateCreateLink.name_of_link)
    await state.update_data(channel_id=channel_id)
    await state.update_data(channel_title=channel_title)

    await callback.message.answer(SET_NAME_FOR_LINK, reply_markup=kb_skip.as_markup())
