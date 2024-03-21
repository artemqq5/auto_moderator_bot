from constants.access import R_ADMIN
from constants.messages_ import USER_NOT_REGISTERED, USER_HASNT_ACCESS
from data.repositories.UserRepository import UserRepository


async def is_user_registered_admin(message) -> bool:
    user = UserRepository().get_user(message.from_user.id)
    if not user:
        await message.answer(USER_NOT_REGISTERED)
        return False

    if user['role'] != R_ADMIN:
        await message.answer(USER_HASNT_ACCESS)
        return False

    return True

