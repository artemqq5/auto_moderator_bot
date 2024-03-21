from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Code, Bold

from constants.messages_ import SKIP, LONG_NAME_FOR_LINK, SET_HELLO_MESSAGE_LINK, CANCELED_SUCCESSFUL, \
    LINK_PREPARE_CAMPLETED, CREATE_LINK_NOW, PREVIEW_HELLO_MESSAGE, PREVIEW_HELLO_MESSAGE_CONSTRUCT, \
    YOU_HASNT_HELLO_MESSAGE, ERROR_LINK_CREATED, SUCCESSFUL_LINK_CREATED, WITHOUT_NAME
from data.repositories.LinkRepository import LinkRepository
from keyboards.crm_keyboard import kb_skip, kb_create_link, kb_crm
from states.StateCreateLink import StateCreateLink

router = Router()


@router.message(StateCreateLink.name_of_link)
async def set_name_link(message: types.Message, state: FSMContext):
    if len(message.text) > 32:
        await message.answer(LONG_NAME_FOR_LINK)
        return

    if message.text != SKIP:
        await state.update_data(name_link=message.text)

    await state.set_state(StateCreateLink.hello_message_from_bot)
    await message.answer(SET_HELLO_MESSAGE_LINK, reply_markup=kb_skip.as_markup())


@router.message(StateCreateLink.hello_message_from_bot)
async def set_hello_message_link(message: types.Message, state: FSMContext):
    if len(message.text) > 2000:
        await message.answer(LONG_NAME_FOR_LINK)
        return

    await state.set_state(StateCreateLink.final_view)

    if message.text != SKIP:
        await state.update_data(hello_message=message.html_text)

    await message.answer(LINK_PREPARE_CAMPLETED, reply_markup=kb_create_link.as_markup())


@router.message(StateCreateLink.final_view, F.text.in_((CREATE_LINK_NOW, PREVIEW_HELLO_MESSAGE)))
async def final_view_link(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    if message.text == PREVIEW_HELLO_MESSAGE:
        if data.get('hello_message', None):
            await message.answer(PREVIEW_HELLO_MESSAGE_CONSTRUCT.format(data['hello_message']),
                                 reply_markup=kb_create_link.as_markup())
        else:
            await message.answer(YOU_HASNT_HELLO_MESSAGE, reply_markup=kb_create_link.as_markup())
        return

    try:

        link_generate = await bot.create_chat_invite_link(data['channel_id'], data.get('name_link', None),
                                                          creates_join_request=True)

        if not LinkRepository().add_link(
                channel_id=data['channel_id'], channel_title=data['channel_title'],
                link_title=link_generate.name, hello_message=data.get('hello_message', None),
                link=link_generate.invite_link, user_id=message.from_user.id
        ):
            raise Exception

        content = Text(SUCCESSFUL_LINK_CREATED,
                       Bold(link_generate.name if link_generate.name is not None else WITHOUT_NAME),
                       "\n",
                       Code(link_generate.invite_link))
        await message.answer(**content.as_kwargs(), reply_markup=kb_crm.as_markup())
        await state.clear()

    except Exception as e:
        print(f"final_view_link: {e}")
        content = Text(ERROR_LINK_CREATED, Code(e))
        await message.answer(**content.as_kwargs())
