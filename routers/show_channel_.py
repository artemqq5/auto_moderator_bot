from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from accesss.check_registered import is_user_registered_admin
from constants.buttons_ import SHOW_CHANNELS
from constants.messages_ import SET_NAME_FOR_LINK, WITHOUT_NAME, MANAGMENT_LINKS, DELETE_CHANNEL, WITHOUT_HELLO_MESSAGE
from data.repositories.ChannelRepository import ChannelRepository
from data.repositories.LinkRepository import LinkRepository
from keyboards.crm_keyboard import kb_skip, kb_delete_channel
from keyboards.kb_channels import kb_channel_choice, ChannelChoice, ChannelNavigation, BackChannelList, \
    kb_channel_manage
from states.StateCreateLink import StateCreateLink
from states.StateDeleteChannel import StateDeleteChannel

router = Router()


@router.message(F.text == SHOW_CHANNELS)
async def show_channel_handler(message: types.Message, bot: Bot):
    if not await is_user_registered_admin(message):
        return

    list_channels = ChannelRepository().get_all_channels()
    await message.answer("Канали", reply_markup=kb_channel_choice(list_channels, current_page=1))


@router.callback_query(ChannelNavigation.filter())
async def channel_nav(callback: types.CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":")[1])
    list_channels = ChannelRepository().get_all_channels()
    await callback.message.edit_text("Канали", reply_markup=kb_channel_choice(list_channels, current_page=page))


@router.callback_query(BackChannelList.filter())
async def back_channel_list(callback: types.CallbackQuery, state: FSMContext):
    list_channels = ChannelRepository().get_all_channels()
    await callback.message.edit_text("Канали", reply_markup=kb_channel_choice(list_channels, current_page=1))


@router.callback_query(ChannelChoice.filter())
async def channel_choice(callback: types.CallbackQuery, state: FSMContext):
    channel_id = callback.data.split(":")[1]
    channel = ChannelRepository().get_channel(channel_id)

    body_message = f"Канал: {channel['title']}\nID: {channel['channel_id']}\nДоданий: {channel['_at']}\n\n"

    links = LinkRepository().get_all(channel['channel_id'])
    users_join = 0

    for link in links:
        users_join += link['users_join']

    body_message += f"<b>Активних посилань: {len(links)}</b>\n"
    body_message += f"<b>Користувачів доєдналося: {users_join}</b>"

    await callback.message.edit_text(body_message, reply_markup=kb_channel_manage(channel))


@router.callback_query(F.data.contains("deletechannel"))
async def delete_cannel_handler(callback: types.CallbackQuery, state: FSMContext):
    channel_id = callback.data.split("#####")[0]
    await state.set_state(StateDeleteChannel.permission)
    await state.update_data(channel_id=channel_id)
    await callback.message.answer(DELETE_CHANNEL, reply_markup=kb_delete_channel.as_markup())
