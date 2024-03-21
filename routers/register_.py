from aiogram import Router, types
from aiogram.filters import Command

from constants.access import R_ADMIN
from constants.messages_ import USER_START_NO_ROLE, USER_START_ADMIN, USER_HAS_REFISTER
from data.repositories.UserRepository import UserRepository
from keyboards.crm_keyboard import kb_crm

register_router = Router()


@register_router.message(Command('start'))
async def start_handler(message: types.Message):
    user = UserRepository().get_user(message.from_user.id)

    if not user:
        UserRepository().add_user(
            message.from_user.id, message.from_user.username, message.from_user.first_name,
            message.from_user.last_name)
        await message.answer(USER_HAS_REFISTER)
        return

    if user['role'] == R_ADMIN:
        await message.answer(USER_START_ADMIN, reply_markup=kb_crm.as_markup())
        return

    # user is no admin
    await message.answer(USER_START_NO_ROLE)



