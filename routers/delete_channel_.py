from aiogram import Router, types, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text, Code

from constants.messages_ import YES, NO, DELETE_CHANNEL_CHANCEL, DELETE_CHANNEL_SUCCESSFUL, DELETE_CHANNEL_FAIL
from data.repositories.ChannelRepository import ChannelRepository
from keyboards.crm_keyboard import kb_crm
from states.StateDeleteChannel import StateDeleteChannel

router = Router()


@router.message(StateDeleteChannel.permission, F.text.in_((YES, NO)))
async def permission_delete_channel(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    if message.text == YES:
        try:
            await bot.leave_chat(data['channel_id'])
            if not ChannelRepository().delete_channel(data['channel_id']):
                raise Exception

            await state.clear()
            await message.answer(DELETE_CHANNEL_SUCCESSFUL, reply_markup=kb_crm.as_markup())

        except Exception as e:
            print(f"permission_delete_channel: {e}")
            content = Text(DELETE_CHANNEL_FAIL, "\n", Code(e))
            await message.answer(**content.as_kwargs())

        return

    await state.clear()
    await message.answer(DELETE_CHANNEL_CHANCEL, reply_markup=kb_crm.as_markup())
