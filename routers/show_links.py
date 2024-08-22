from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from constants.messages_ import WITHOUT_NAME, MANAGMENT_LINKS, WITHOUT_HELLO_MESSAGE
from data.repositories.LinkRepository import LinkRepository
from keyboards.kb_channels import ChannelNavigation, BackChannelList
from keyboards.kb_links import kb_link_choice, LinkChoice, kb_link_manage, LinkNavigation, BackLinkList

router = Router()


@router.callback_query(F.data.contains("managelinks"))
async def managelink_cannel_handler(callback: types.CallbackQuery, state: FSMContext):
    channel_id = callback.data.split("#####")[0]
    await state.update_data(link_channel_id=channel_id)
    links = LinkRepository().get_all(channel_id)
    await callback.message.edit_text(MANAGMENT_LINKS, reply_markup=kb_link_choice(links, current_page=1))


@router.callback_query(LinkNavigation.filter())
async def link_nav(callback: types.CallbackQuery, state: FSMContext):
    page = int(callback.data.split(":")[1])
    await state.update_data(page_link=page)
    data = await state.get_data()
    links = LinkRepository().get_all(data['link_channel_id'])
    await callback.message.edit_text(MANAGMENT_LINKS, reply_markup=kb_link_choice(links, current_page=page))


@router.callback_query(BackLinkList.filter())
async def back_channel_list(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    links = LinkRepository().get_all(data['link_channel_id'])
    await callback.message.edit_text(MANAGMENT_LINKS,
                                     reply_markup=kb_link_choice(links, current_page=data.get('page_link', 1)))


@router.callback_query(LinkChoice.filter())
async def choice_link(callback: types.CallbackQuery):
    link_url = f"https://t.me/{callback.data.split(':')[1]}"
    link = LinkRepository().get_link(link_url)

    users_join = link['users_join']
    content = (f"<b>{link['link_title'] if link['link_title'] is not None else WITHOUT_NAME}</b>\n\n"
               f"{link['hello_message'] if link['hello_message'] is not None else WITHOUT_HELLO_MESSAGE}\n\n"
               f"<b>Користувачів доєдналося</b> {users_join}\n <code>{link['link']}</code>")

    await callback.message.answer(content, reply_markup=kb_link_manage(link))
